"""Tests for core agent module"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.core.agent import GeminiAgent, RateLimiter
from src.config.settings import settings
from src.utils.exceptions import GeminiAPIError


@pytest.mark.asyncio
async def test_rate_limiter_acquire_no_wait():
    """Rate limiter - bekleme gerektirmeyen durum"""
    limiter = RateLimiter(calls_per_minute=60)
    limiter.last_call_time = 0.0

    with patch('time.time', return_value=2.0):
        # İlk çağrıdan 2 saniye geçmiş, bekleme gerekmez
        await limiter.acquire()
        assert limiter.last_call_time == 2.0


@pytest.mark.asyncio
async def test_rate_limiter_acquire_with_wait():
    """Rate limiter - bekleme gerektiren durum"""
    limiter = RateLimiter(calls_per_minute=60)
    limiter.last_call_time = 0.0

    with patch('time.time', side_effect=[0.5, 0.5, 2.0]):
        # İlk çağrıdan 0.5 saniye geçmiş, bekleme gerekir
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            await limiter.acquire()
            # Minimum 1 saniye bekleme garantisi
            mock_sleep.assert_called_once()
            assert mock_sleep.call_args[0][0] >= 1.0


@pytest.mark.asyncio
async def test_rate_limiter_minimum_wait():
    """Rate limiter - minimum 1 saniye bekleme garantisi"""
    limiter = RateLimiter(calls_per_minute=120)  # 0.5 saniye interval
    limiter.last_call_time = 0.0

    with patch('time.time', side_effect=[0.3, 0.3, 2.0]):
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            await limiter.acquire()
            # 0.3 saniye geçmiş ama minimum 1 saniye bekleme
            mock_sleep.assert_called_once()
            assert mock_sleep.call_args[0][0] >= 1.0


@pytest.mark.asyncio
async def test_gemini_agent_init_success():
    """GeminiAgent başlatma - başarılı"""
    with (
        patch('google.generativeai.configure'),
        patch('google.generativeai.GenerativeModel') as mock_model
    ):
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance

        agent = GeminiAgent(api_key="test_key", model_name="test-model")

        assert agent.api_key == "test_key"
        assert agent.model_name == "test-model"
        assert agent.rate_limiter is not None


def test_gemini_agent_init_no_api_key():
    """GeminiAgent başlatma - API key yok"""
    with patch('google.generativeai.configure'):
        with patch.object(settings, 'GEMINI_API_KEY', '', create=True):
            with pytest.raises(
                ValueError,
                match=r"GEMINI_API_KEY gerekli",
            ):
                GeminiAgent(api_key=None)


@pytest.mark.asyncio
async def test_generate_with_retry_success():
    """generate_with_retry - başarılı çağrı"""
    with (
        patch('google.generativeai.configure'),
        patch('google.generativeai.GenerativeModel') as mock_model
    ):
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance

        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_model_instance.generate_content_async = AsyncMock(
            return_value=mock_response
        )

        agent = GeminiAgent(api_key="test_key")

        with patch.object(
            agent.rate_limiter, 'acquire', new_callable=AsyncMock
        ):
            result = await agent.generate_with_retry("test prompt")

            assert result == "Test response"
            mock_model_instance.generate_content_async.assert_called_once()


@pytest.mark.asyncio
async def test_generate_with_retry_empty_response():
    """generate_with_retry - boş yanıt"""
    with (
        patch('google.generativeai.configure'),
        patch('google.generativeai.GenerativeModel') as mock_model
    ):
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance

        mock_response = MagicMock()
        mock_response.text = None
        mock_response.candidates = []
        mock_model_instance.generate_content_async = AsyncMock(
            return_value=mock_response
        )

        agent = GeminiAgent(api_key="test_key")

        with patch.object(
            agent.rate_limiter, 'acquire', new_callable=AsyncMock
        ):
            with pytest.raises(GeminiAPIError, match="Bos yanit alindi"):
                await agent.generate_with_retry("test prompt")


@pytest.mark.asyncio
async def test_generate_with_retry_exception_retry():
    """generate_with_retry - exception sonrası retry"""
    with (
        patch('google.generativeai.configure'),
        patch('google.generativeai.GenerativeModel') as mock_model
    ):
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance

        # İlk çağrı exception, ikinci başarılı
        mock_response = MagicMock()
        mock_response.text = "Success"
        mock_model_instance.generate_content_async = AsyncMock(
            side_effect=[Exception("API Error"), mock_response]
        )

        agent = GeminiAgent(api_key="test_key")

        with (
            patch.object(
                agent.rate_limiter, 'acquire', new_callable=AsyncMock
            ),
            patch('asyncio.sleep', new_callable=AsyncMock)
        ):
            result = await agent.generate_with_retry(
                "test prompt", max_retries=2
            )

            assert result == "Success"
            assert mock_model_instance.generate_content_async.call_count == 2


@pytest.mark.asyncio
async def test_generate_with_retry_max_retries_exceeded():
    """generate_with_retry - maksimum retry aşıldı"""
    with (
        patch('google.generativeai.configure'),
        patch('google.generativeai.GenerativeModel') as mock_model
    ):
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance

        mock_model_instance.generate_content_async = AsyncMock(
            side_effect=Exception("API Error")
        )

        agent = GeminiAgent(api_key="test_key")

        with (
            patch.object(
                agent.rate_limiter, 'acquire', new_callable=AsyncMock
            ),
            patch('asyncio.sleep', new_callable=AsyncMock)
        ):
            with pytest.raises(GeminiAPIError, match="API hatasi"):
                await agent.generate_with_retry("test prompt", max_retries=2)


@pytest.mark.asyncio
async def test_generate_json_response_success():
    """generate_json_response - başarılı JSON parse"""
    with (
        patch('google.generativeai.configure'),
        patch('google.generativeai.GenerativeModel') as mock_model
    ):
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance

        mock_response = MagicMock()
        mock_response.text = (
            '{"result": 42, "steps": ["step1"], "confidence_score": 1.0}'
        )
        mock_model_instance.generate_content_async = AsyncMock(
            return_value=mock_response
        )

        agent = GeminiAgent(api_key="test_key")

        with patch.object(
            agent.rate_limiter, 'acquire', new_callable=AsyncMock
        ):
            result = await agent.generate_json_response("test prompt")

            assert result["result"] == 42.0
            assert result["steps"] == ["step1"]
            assert result["confidence_score"] == 1.0


@pytest.mark.asyncio
async def test_generate_json_response_json_decode_error():
    """generate_json_response - JSON decode hatası"""
    with (
        patch('google.generativeai.configure'),
        patch('google.generativeai.GenerativeModel') as mock_model
    ):
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance

        mock_response = MagicMock()
        mock_response.text = "Invalid JSON {"
        mock_model_instance.generate_content_async = AsyncMock(
            return_value=mock_response
        )

        agent = GeminiAgent(api_key="test_key")

        with patch.object(
            agent.rate_limiter, 'acquire', new_callable=AsyncMock
        ):
            result = await agent.generate_json_response("test prompt")

            # Fallback structured response
            assert result["result"] == "Invalid JSON {"
            assert result["steps"] == ["Invalid JSON {"]
            assert result["confidence_score"] == 0.95


@pytest.mark.asyncio
async def test_generate_json_response_no_json_match():
    """generate_json_response - JSON pattern bulunamadı"""
    with (
        patch('google.generativeai.configure'),
        patch('google.generativeai.GenerativeModel') as mock_model
    ):
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance

        mock_response = MagicMock()
        mock_response.text = "No JSON here"
        mock_model_instance.generate_content_async = AsyncMock(
            return_value=mock_response
        )

        agent = GeminiAgent(api_key="test_key")

        with patch.object(
            agent.rate_limiter, 'acquire', new_callable=AsyncMock
        ):
            result = await agent.generate_json_response("test prompt")

            # Fallback structured response
            assert result["result"] == "No JSON here"
            assert result["steps"] == ["No JSON here"]
            assert result["confidence_score"] == 0.95


@pytest.mark.asyncio
async def test_generate_json_response_int_to_float():
    """generate_json_response - int sonucu float'a çevirme"""
    with (
        patch('google.generativeai.configure'),
        patch('google.generativeai.GenerativeModel') as mock_model
    ):
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance

        mock_response = MagicMock()
        mock_response.text = '{"result": 42, "steps": []}'
        mock_model_instance.generate_content_async = AsyncMock(
            return_value=mock_response
        )

        agent = GeminiAgent(api_key="test_key")

        with patch.object(
            agent.rate_limiter, 'acquire', new_callable=AsyncMock
        ):
            result = await agent.generate_json_response("test prompt")

            assert result["result"] == 42.0
            assert isinstance(result["result"], float)

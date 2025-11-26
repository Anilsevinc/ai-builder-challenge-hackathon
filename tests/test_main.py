"""Tests for main.py CLI and orchestrator"""

import pytest
import asyncio  # noqa: F401
import sys  # noqa: F401
from unittest.mock import AsyncMock, MagicMock, patch
from src.main import (
    CalculatorAgent,
    interactive_mode,
    single_command_mode,
    main
)
from src.utils.exceptions import (
    SecurityViolationError,
    InvalidInputError,
    CalculationError,
)


@pytest.fixture
def mock_calculator_agent():
    """Mock CalculatorAgent fixture"""
    agent = MagicMock(spec=CalculatorAgent)
    agent.process_command = AsyncMock(return_value="✅ Sonuc: 4.0")
    return agent


@pytest.mark.asyncio
async def test_calculator_agent_init_success():
    """CalculatorAgent başlatma - başarılı"""
    with patch('src.main.settings.validate'), \
         patch('src.main.GeminiAgent') as mock_gemini, \
         patch('src.main.BasicMathModule'), \
         patch('src.main.CalculusModule'), \
         patch('src.main.LinearAlgebraModule'), \
         patch('src.main.FinancialModule'), \
         patch('src.main.EquationSolverModule'), \
         patch('src.main.GraphPlotterModule'), \
         patch('src.main.StatisticsModule'):
        mock_gemini.return_value = MagicMock()
        agent = CalculatorAgent()
        assert agent.gemini_agent is not None
        assert agent.parser is not None
        assert agent.validator is not None
        assert len(agent.modules) == 7


@pytest.mark.asyncio
async def test_calculator_agent_init_validation_error():
    """CalculatorAgent başlatma - validation hatası"""
    with patch(
        'src.main.settings.validate',
        side_effect=ValueError("Invalid settings")
    ):
        with pytest.raises(ValueError):
            CalculatorAgent()


@pytest.mark.asyncio
async def test_process_command_success():
    """process_command - başarılı işlem"""
    with patch('src.main.settings.validate'), \
         patch('src.main.GeminiAgent') as mock_gemini, \
         patch('src.main.BasicMathModule') as mock_module_class:
        mock_gemini.return_value = MagicMock()
        mock_module = MagicMock()
        mock_result = MagicMock(
            result=4.0,
            steps=["2 + 2 = 4"],
            confidence_score=1.0,
            visual_data=None,
            error=None,
        )
        mock_module.calculate = AsyncMock(return_value=mock_result)
        mock_module_class.return_value = mock_module

        agent = CalculatorAgent()
        result = await agent.process_command("2 + 2")

        assert "✅ Sonuc:" in result
        assert "4" in result.splitlines()[0]
        assert "📝 Adimlar:" in result


@pytest.mark.asyncio
async def test_process_command_security_violation():
    """process_command - güvenlik ihlali"""
    with patch('src.main.settings.validate'), \
         patch('src.main.GeminiAgent') as mock_gemini, \
         patch('src.main.BasicMathModule'):
        mock_gemini.return_value = MagicMock()
        agent = CalculatorAgent()

        with patch.object(
            agent.validator, 'sanitize_expression',
            side_effect=SecurityViolationError("Yasakli ifade")
        ):
            result = await agent.process_command("eval('malicious')")
            assert "❌ Guvenlik hatasi" in result


@pytest.mark.asyncio
async def test_process_command_invalid_input():
    """process_command - geçersiz giriş"""
    with patch('src.main.settings.validate'), \
         patch('src.main.GeminiAgent') as mock_gemini, \
         patch('src.main.BasicMathModule'):
        mock_gemini.return_value = MagicMock()
        agent = CalculatorAgent()

        with patch.object(
            agent.validator, 'sanitize_expression',
            side_effect=InvalidInputError("Bos ifade")
        ):
            result = await agent.process_command("2 + 2")
            assert "❌ Gecersiz giris" in result


@pytest.mark.asyncio
async def test_process_command_empty_input_message():
    """process_command - boş komut"""
    with patch('src.main.settings.validate'), \
         patch('src.main.GeminiAgent') as mock_gemini, \
         patch('src.main.BasicMathModule'):
        mock_gemini.return_value = MagicMock()
        agent = CalculatorAgent()

        result = await agent.process_command("")
        assert result == "Boş komut girdiniz."


@pytest.mark.asyncio
async def test_process_command_module_not_found():
    """process_command - modül bulunamadı"""
    with (
        patch('src.main.settings.validate'),
        patch('src.main.GeminiAgent') as mock_gemini,
        patch('src.main.BasicMathModule')
    ):
        mock_gemini.return_value = MagicMock()
        agent = CalculatorAgent()

        with patch.object(
            agent.parser, 'parse',
            return_value=("unknown_module", "test")
        ):
            result = await agent.process_command("!unknown test")
            assert "❌ Modul bulunamadi" in result


@pytest.mark.asyncio
async def test_process_command_calculation_error():
    """process_command - hesaplama hatası"""
    with (
        patch('src.main.settings.validate'),
        patch('src.main.GeminiAgent') as mock_gemini,
        patch('src.main.BasicMathModule') as mock_module_class
    ):
        mock_gemini.return_value = MagicMock()
        mock_module = MagicMock()
        mock_module.calculate = AsyncMock(
            side_effect=CalculationError("Hesaplama hatasi")
        )
        mock_module_class.return_value = mock_module

        agent = CalculatorAgent()
        result = await agent.process_command("2 + 2")
        assert "❌ Hesaplama hatasi" in result


@pytest.mark.asyncio
async def test_process_command_unexpected_error():
    """process_command - beklenmeyen hata"""
    with (
        patch('src.main.settings.validate'),
        patch('src.main.GeminiAgent') as mock_gemini,
        patch('src.main.BasicMathModule')
    ):
        mock_gemini.return_value = MagicMock()
        agent = CalculatorAgent()

        with patch.object(
            agent.parser, 'parse',
            side_effect=Exception("Unexpected")
        ):
            result = await agent.process_command("test")
            assert "❌ Beklenmeyen hata" in result


@pytest.mark.asyncio
async def test_process_command_error_from_module():
    """process_command - modül CalculationResult.error döndürür"""
    with (
        patch('src.main.settings.validate'),
        patch('src.main.GeminiAgent') as mock_gemini,
        patch('src.main.BasicMathModule') as mock_module_class
    ):
        mock_gemini.return_value = MagicMock()
        mock_module = MagicMock()
        error_result = MagicMock()
        error_result.error = (
            "Hatalı işlem: Eksik operand. Örnek kullanım: !basic 5 + 3"
        )
        error_result.result = ""
        error_result.steps = []
        error_result.confidence_score = 1.0
        mock_module.calculate = AsyncMock(return_value=error_result)
        mock_module_class.return_value = mock_module

        agent = CalculatorAgent()
        result = await agent.process_command("!basic 5 +")
        assert "Hatalı işlem" in result


@pytest.mark.asyncio
async def test_format_output_with_visual_data():
    """_format_output - görsel veri ile"""
    with patch('src.main.settings.validate'), \
         patch('src.main.GeminiAgent') as mock_gemini, \
         patch('src.main.BasicMathModule'):
        mock_gemini.return_value = MagicMock()
        agent = CalculatorAgent()

        result_mock = MagicMock()
        result_mock.result = 4.0
        result_mock.steps = ["step1"]
        result_mock.confidence_score = 0.9
        result_mock.visual_data = {"plot_paths": {"png": "/path/to/plot.png"}}
        result_mock.error = None

        output = agent._format_output(result_mock)

        assert "✅ Sonuc:" in output
        assert "4" in output.splitlines()[0]
        assert "📝 Adimlar:" in output
        assert "⚠️  Guven Skoru: 0.90" in output
        assert "📊 Grafik: /path/to/plot.png" in output


def test_format_output_with_error():
    """_format_output - hata mesajı"""
    with (
        patch('src.main.settings.validate'),
        patch('src.main.GeminiAgent') as mock_gemini,
        patch('src.main.BasicMathModule')
    ):
        mock_gemini.return_value = MagicMock()
        agent = CalculatorAgent()

        result_mock = MagicMock()
        result_mock.error = (
            "Hatalı işlem: Eksik operand. Örnek kullanım: !basic 5 + 3"
        )
        result_mock.result = ""
        result_mock.steps = []
        output = agent._format_output(result_mock)

        assert output == (
            "Hatalı işlem: Eksik operand. Örnek kullanım: !basic 5 + 3"
        )


@pytest.mark.asyncio
async def test_single_command_mode():
    """single_command_mode testi"""
    with patch('src.main.CalculatorAgent') as mock_agent_class:
        mock_agent = MagicMock()
        mock_agent.process_command = AsyncMock(return_value="✅ Sonuc: 4.0")
        mock_agent_class.return_value = mock_agent

        with patch('builtins.print') as mock_print:
            await single_command_mode("2 + 2")
            mock_print.assert_called_once_with("✅ Sonuc: 4.0")


@pytest.mark.asyncio
async def test_single_command_mode_no_result():
    """single_command_mode - sonuç yok"""
    with patch('src.main.CalculatorAgent') as mock_agent_class:
        mock_agent = MagicMock()
        mock_agent.process_command = AsyncMock(return_value=None)
        mock_agent_class.return_value = mock_agent

        with patch('builtins.print') as mock_print:
            await single_command_mode("test")
            mock_print.assert_not_called()


def test_main_with_args():
    """main - komut satırı argümanları ile"""
    with (
        patch('sys.argv', ['main.py', '2', '+', '2']),
        patch('asyncio.run') as mock_run
    ):
        main()
        mock_run.assert_called_once()
        # single_command_mode çağrıldığını kontrol et
        call_args = mock_run.call_args[0][0]
        assert call_args is not None


def test_main_without_args():
    """main - argüman olmadan"""
    with (
        patch('sys.argv', ['main.py']),
        patch('asyncio.run') as mock_run
    ):
        main()
        mock_run.assert_called_once()
        # interactive_mode çağrıldığını kontrol et
        call_args = mock_run.call_args[0][0]
        assert call_args is not None


@pytest.mark.asyncio
async def test_interactive_mode_quit():
    """interactive_mode - quit komutu"""
    with patch('src.main.CalculatorAgent') as mock_agent_class:
        mock_agent = MagicMock()
        mock_agent.process_command = AsyncMock()
        mock_agent_class.return_value = mock_agent

        with patch('builtins.input', side_effect=['quit']), \
             patch('builtins.print') as mock_print:
            await interactive_mode()
            mock_print.assert_any_call("Gule gule!")


@pytest.mark.asyncio
async def test_interactive_mode_empty_input():
    """interactive_mode - boş giriş"""
    with patch('src.main.CalculatorAgent') as mock_agent_class:
        mock_agent = MagicMock()
        mock_agent.process_command = AsyncMock()
        mock_agent_class.return_value = mock_agent

        with patch('builtins.input', side_effect=['', 'quit']), \
             patch('builtins.print'):
            await interactive_mode()
            # Boş input için process_command çağrılmamalı
            assert mock_agent.process_command.call_count == 0


@pytest.mark.asyncio
async def test_interactive_mode_keyboard_interrupt():
    """interactive_mode - KeyboardInterrupt"""
    with patch('src.main.CalculatorAgent') as mock_agent_class:
        mock_agent = MagicMock()
        mock_agent.process_command = AsyncMock()
        mock_agent_class.return_value = mock_agent

        with patch('builtins.input', side_effect=KeyboardInterrupt()), \
             patch('builtins.print') as mock_print:
            await interactive_mode()
            mock_print.assert_any_call("\n\nGule gule!")

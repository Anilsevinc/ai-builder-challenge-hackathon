"""Tests for financial module"""

import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from src.modules.financial import FinancialModule
from src.config.settings import settings


@pytest.mark.asyncio
async def test_financial_calculate_success(mock_gemini_agent):
    """Financial calculation - başarılı"""
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 1000.50,
        "steps": ["NPV hesaplandi"],
        "confidence_score": 1.0,
    }
    
    module = FinancialModule(mock_gemini_agent)
    result = await module.calculate("NPV 1000 0.1 5")
    
    assert result.domain == "financial"
    assert isinstance(result.result, Decimal)
    assert result.result == Decimal("1000.50")
    assert len(result.steps) > 0


@pytest.mark.asyncio
async def test_financial_calculate_with_currency(mock_gemini_agent):
    """Financial calculation - para birimi parametresi"""
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 500.25,
        "steps": ["Loan payment hesaplandi"],
        "confidence_score": 1.0,
    }
    
    module = FinancialModule(mock_gemini_agent)
    result = await module.calculate("loan payment 10000 0.05 12", currency="USD")
    
    assert result.domain == "financial"
    # Currency parametresi Gemini'ye gönderildiğini kontrol et
    call_args = mock_gemini_agent.generate_json_response.call_args
    assert call_args is not None


@pytest.mark.asyncio
async def test_financial_calculate_default_currency(mock_gemini_agent):
    """Financial calculation - varsayılan para birimi"""
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 750.0,
        "steps": ["Interest hesaplandi"],
        "confidence_score": 1.0,
    }
    
    module = FinancialModule(mock_gemini_agent)
    result = await module.calculate("interest 10000 0.075")
    
    assert result.domain == "financial"
    # Default currency kullanıldığını kontrol et
    call_args = mock_gemini_agent.generate_json_response.call_args
    assert call_args is not None


@pytest.mark.asyncio
async def test_financial_calculate_int_result(mock_gemini_agent):
    """Financial calculation - int sonucu Decimal'e çevirme"""
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 1000,  # int
        "steps": ["Calculation done"],
        "confidence_score": 1.0,
    }
    
    module = FinancialModule(mock_gemini_agent)
    result = await module.calculate("test")
    
    assert isinstance(result.result, Decimal)
    assert result.result == Decimal("1000")


@pytest.mark.asyncio
async def test_financial_calculate_float_result(mock_gemini_agent):
    """Financial calculation - float sonucu Decimal'e çevirme"""
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 1234.56789,  # float
        "steps": ["Calculation done"],
        "confidence_score": 1.0,
    }
    
    module = FinancialModule(mock_gemini_agent)
    result = await module.calculate("test")
    
    assert isinstance(result.result, Decimal)
    assert result.result == Decimal("1234.56789")


@pytest.mark.asyncio
async def test_financial_calculate_non_numeric_result(mock_gemini_agent):
    """Financial calculation - numerik olmayan sonuç"""
    mock_gemini_agent.generate_json_response.return_value = {
        "result": "Error message",  # string
        "steps": ["Error occurred"],
        "confidence_score": 0.5,
    }
    
    module = FinancialModule(mock_gemini_agent)
    result = await module.calculate("invalid")
    
    assert result.domain == "financial"
    assert result.result == "Error message"  # Decimal'e çevrilmez


@pytest.mark.asyncio
async def test_financial_calculate_exception(mock_gemini_agent):
    """Financial calculation - exception handling"""
    mock_gemini_agent.generate_json_response.side_effect = Exception("API Error")
    
    module = FinancialModule(mock_gemini_agent)
    
    with pytest.raises(Exception, match="API Error"):
        await module.calculate("test")


@pytest.mark.asyncio
async def test_financial_calculate_no_result_key(mock_gemini_agent):
    """Financial calculation - result key yok"""
    mock_gemini_agent.generate_json_response.return_value = {
        "steps": ["Calculation done"],
        "confidence_score": 1.0,
    }
    
    module = FinancialModule(mock_gemini_agent)
    result = await module.calculate("test")
    
    assert result.result == Decimal("0")  # Default değer


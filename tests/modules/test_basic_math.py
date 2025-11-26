"""Tests for basic math module"""

import pytest
from src.modules.basic_math import BasicMathModule


@pytest.mark.asyncio
async def test_basic_addition(mock_gemini_agent):
    """Temel toplama testi"""
    # Mock'u "2 + 2" için doğru sonuç döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 4.0,
        "steps": ["2 + 2 = 4"],
        "confidence_score": 1.0,
    }

    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")

    assert result is not None
    assert result.domain == "basic_math"
    assert result.confidence_score == 1.0
    assert result.result == 4.0
    assert len(result.steps) > 0


@pytest.mark.asyncio
async def test_basic_multiplication(mock_gemini_agent):
    """Çarpma testi"""
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 12.0,
        "steps": ["3 * 4 = 12"],
        "confidence_score": 1.0,
    }

    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("3 * 4")

    assert result is not None
    assert result.domain == "basic_math"
    assert result.result == 12.0
    assert len(result.steps) > 0
    assert result.confidence_score == 1.0


@pytest.mark.asyncio
async def test_basic_math_invalid_characters(mock_gemini_agent):
    """Geçersiz karakterler engellenir"""
    module = BasicMathModule(mock_gemini_agent)

    result = await module.calculate(
        "import('os').system('rm -rf /')"
    )

    assert result.error == "Geçersiz veya yasaklı ifade girdiniz."
    assert result.result == ""
    mock_gemini_agent.generate_json_response.assert_not_called()


@pytest.mark.asyncio
async def test_basic_math_missing_operand(mock_gemini_agent):
    """Eksik operand senaryosu"""
    module = BasicMathModule(mock_gemini_agent)

    result = await module.calculate("5 +")

    assert result.error == (
        "Hatalı işlem: Eksik operand. Örnek kullanım: !basic 5 + 3"
    )
    assert result.result == ""
    mock_gemini_agent.generate_json_response.assert_not_called()

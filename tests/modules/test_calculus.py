"""Tests for calculus module"""

import pytest
from src.modules.calculus import CalculusModule
from src.utils.exceptions import InvalidInputError


@pytest.mark.asyncio
async def test_calculus_derivative_polynomial(mock_gemini_agent):
    """Polinom turev testi"""
    # Mock'u "derivative x^3 at x=2" için doğru sonuç döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 12.0,
        "steps": ["d/dx(x^3) = 3x^2", "3x^2 at x=2 = 3 * 4 = 12"],
        "confidence_score": 1.0,
    }
    
    module = CalculusModule(mock_gemini_agent)
    result = await module.calculate("derivative x^3 at x=2")
    
    assert result is not None
    assert result.domain == "calculus"
    assert len(result.steps) >= 1
    assert result.result == 12.0
    assert result.confidence_score == 1.0


@pytest.mark.asyncio
async def test_calculus_invalid_input(mock_gemini_agent):
    """Gecersiz giris testi"""
    module = CalculusModule(mock_gemini_agent)
    
    with pytest.raises(InvalidInputError):
        await module.calculate("")


@pytest.mark.asyncio
async def test_calculus_integral(mock_gemini_agent):
    """Integral testi"""
    # Mock'u "integral x^2 from 0 to 1" için doğru sonuç döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 1/3,
        "steps": ["∫[0 to 1] x^2 dx", "= [x^3/3][0 to 1]", "= 1/3 - 0 = 1/3"],
        "confidence_score": 1.0,
    }
    
    module = CalculusModule(mock_gemini_agent)
    result = await module.calculate("integral x^2 from 0 to 1")
    
    assert result is not None
    assert result.domain == "calculus"
    assert abs(result.result - 1/3) < 0.0001  # Float karşılaştırması için tolerance
    assert len(result.steps) > 0
    assert result.confidence_score == 1.0


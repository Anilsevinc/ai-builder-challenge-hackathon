"""Tests for linear algebra module"""

import pytest
from src.modules.linear_algebra import LinearAlgebraModule


@pytest.mark.asyncio
async def test_matrix_multiplication(mock_gemini_agent):
    """Matris carpimi testi"""
    # Mock'u matris çarpımı için doğru sonuç döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": [[17], [39]],
        "steps": [
            "[[1,2],[3,4]] * [[5],[6]]",
            "= [[1*5 + 2*6], [3*5 + 4*6]]",
            "= [[17], [39]]"
        ],
        "confidence_score": 1.0,
    }
    
    module = LinearAlgebraModule(mock_gemini_agent)
    result = await module.calculate("[[1,2],[3,4]] * [[5],[6]]")
    
    assert result is not None
    assert result.domain == "linear_algebra"
    assert result.result == [[17], [39]]
    assert len(result.steps) > 0
    assert result.confidence_score == 1.0


@pytest.mark.asyncio
async def test_determinant(mock_gemini_agent):
    """Determinant testi"""
    # Mock'u determinant için doğru sonuç döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": -2.0,
        "steps": [
            "det([[1,2],[3,4]])",
            "= 1*4 - 2*3",
            "= 4 - 6 = -2"
        ],
        "confidence_score": 1.0,
    }
    
    module = LinearAlgebraModule(mock_gemini_agent)
    result = await module.calculate("determinant [[1,2],[3,4]]")
    
    assert result is not None
    assert result.domain == "linear_algebra"
    assert result.result == -2.0
    assert len(result.steps) > 0
    assert result.confidence_score == 1.0


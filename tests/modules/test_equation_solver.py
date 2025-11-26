"""Tests for equation solver module"""

import pytest
from unittest.mock import AsyncMock
from src.modules.equation_solver import EquationSolverModule
from src.utils.exceptions import InvalidInputError


@pytest.mark.asyncio
async def test_equation_solver_linear(mock_gemini_agent):
    """Equation solver - linear equation"""
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 2.0,
        "steps": ["2x + 4 = 0", "x = -2"],
        "confidence_score": 1.0,
    }
    
    module = EquationSolverModule(mock_gemini_agent)
    result = await module.calculate("2x + 4 = 0")
    
    assert result.domain == "equation_solver"
    assert result.result == 2.0
    assert len(result.steps) > 0


@pytest.mark.asyncio
async def test_equation_solver_quadratic(mock_gemini_agent):
    """Equation solver - quadratic equation"""
    mock_gemini_agent.generate_json_response.return_value = {
        "result": [1.0, 2.0],
        "steps": ["x^2 - 3x + 2 = 0", "x = 1 or x = 2"],
        "confidence_score": 1.0,
    }
    
    module = EquationSolverModule(mock_gemini_agent)
    result = await module.calculate("x^2 - 3x + 2 = 0")
    
    assert result.domain == "equation_solver"
    assert result.result == [1.0, 2.0]
    assert len(result.steps) > 0


@pytest.mark.asyncio
async def test_equation_solver_differential(mock_gemini_agent):
    """Equation solver - differential equation"""
    mock_gemini_agent.generate_json_response.return_value = {
        "result": "y = Ce^x",
        "steps": ["dy/dx = y", "y = Ce^x"],
        "confidence_score": 0.9,
    }
    
    module = EquationSolverModule(mock_gemini_agent)
    result = await module.calculate("dy/dx = y")
    
    assert result.domain == "equation_solver"
    assert result.result == "y = Ce^x"
    assert result.confidence_score == 0.9


@pytest.mark.asyncio
async def test_equation_solver_system_of_equations(mock_gemini_agent):
    """Equation solver - system of equations"""
    mock_gemini_agent.generate_json_response.return_value = {
        "result": {"x": 1.0, "y": 2.0},
        "steps": ["x + y = 3", "x - y = -1", "x = 1, y = 2"],
        "confidence_score": 1.0,
    }
    
    module = EquationSolverModule(mock_gemini_agent)
    result = await module.calculate("x + y = 3, x - y = -1")
    
    assert result.domain == "equation_solver"
    assert isinstance(result.result, dict)
    assert result.result["x"] == 1.0
    assert result.result["y"] == 2.0


@pytest.mark.asyncio
async def test_equation_solver_exception(mock_gemini_agent):
    """Equation solver - exception handling"""
    mock_gemini_agent.generate_json_response.side_effect = Exception("API Error")
    
    module = EquationSolverModule(mock_gemini_agent)
    
    with pytest.raises(Exception, match="API Error"):
        await module.calculate("invalid equation")


@pytest.mark.asyncio
async def test_equation_solver_invalid_input(mock_gemini_agent):
    """Equation solver - geçersiz giriş"""
    module = EquationSolverModule(mock_gemini_agent)
    
    with pytest.raises(InvalidInputError):
        await module.calculate("")  # Boş ifade


"""Integration tests for Calculator Agent"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.main import CalculatorAgent
from src.utils.exceptions import SecurityViolationError


@pytest.mark.asyncio
async def test_basic_math_integration(mock_gemini_agent):
    """Temel matematik entegrasyon testi"""
    # Not: Bu test mock kullanir, gercek API cagrisi yapmaz
    # Mock'u doğru sonuç döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 4.0,
        "steps": ["2 + 2 = 4"],
        "confidence_score": 1.0,
    }

    from src.modules.basic_math import BasicMathModule

    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")

    assert result is not None
    assert result.domain == "basic_math"
    assert len(result.steps) > 0
    assert result.result == 4.0


@pytest.mark.asyncio
async def test_financial_integration(mock_gemini_agent):
    """Finansal modül entegrasyon testi"""
    from decimal import Decimal
    from src.modules.financial import FinancialModule

    mock_gemini_agent.generate_json_response.return_value = {
        "result": 1000.50,
        "steps": ["NPV hesaplandi: 1000.50"],
        "confidence_score": 1.0,
    }

    module = FinancialModule(mock_gemini_agent)
    result = await module.calculate("NPV 1000 0.1 5", currency="TRY")

    assert result is not None
    assert result.domain == "financial"
    assert isinstance(result.result, Decimal)
    assert result.result == Decimal("1000.50")


@pytest.mark.asyncio
async def test_graph_plotter_integration(mock_gemini_agent, tmp_path):
    """Grafik plotter entegrasyon testi"""
    from src.modules.graph_plotter import GraphPlotterModule

    mock_gemini_agent.generate_json_response.return_value = {
        "result": "Grafik olusturuldu",
        "steps": ["Plot created"],
        "visual_data": {
            "plot_type": "2d",
            "x_range": [-10, 10]
        },
        "confidence_score": 1.0,
    }

    module = GraphPlotterModule(mock_gemini_agent)
    module.cache_dir = tmp_path

    with patch('matplotlib.pyplot.savefig'), \
         patch('matplotlib.pyplot.close'), \
         patch('matplotlib.pyplot.figure'), \
         patch('matplotlib.pyplot.plot'), \
         patch('matplotlib.pyplot.grid'), \
         patch('matplotlib.pyplot.xlabel'), \
         patch('matplotlib.pyplot.ylabel'), \
         patch('matplotlib.pyplot.title'):
        result = await module.calculate("x^2")

        assert result is not None
        assert result.domain == "graph_plotter"
        assert result.visual_data is not None
        assert "plot_paths" in result.visual_data


@pytest.mark.asyncio
async def test_graph_plotter_cache_integration(mock_gemini_agent, tmp_path):
    """Grafik plotter cache entegrasyon testi"""
    from src.modules.graph_plotter import GraphPlotterModule

    module = GraphPlotterModule(mock_gemini_agent)
    module.cache_dir = tmp_path
    module.plot_cache["x^2"] = str(tmp_path / "cached.png")

    result = await module.calculate("x^2")

    assert result is not None
    assert result.domain == "graph_plotter"
    assert "cache" in result.result.lower()
    # Cache hit olduğu için Gemini çağrısı yapılmamalı
    assert not mock_gemini_agent.generate_json_response.called


@pytest.mark.asyncio
async def test_security_validation():
    """Guvenlik dogrulama testi"""
    from src.core.validator import InputValidator

    validator = InputValidator()

    # Yasakli ifade testi
    with pytest.raises(SecurityViolationError):
        validator.sanitize_expression("eval('malicious code')")

    # Gecerli ifade testi
    assert validator.sanitize_expression("2 + 2") == "2 + 2"


@pytest.mark.asyncio
async def test_command_parsing():
    """Komut parsing testi"""
    from src.core.parser import CommandParser

    parser = CommandParser()

    # Prefix testi
    module, expr = parser.parse("!calculus derivative x^2")
    assert module == "calculus"
    assert "derivative" in expr

    # Dogal dil testi
    module, expr = parser.parse("solve 2x + 3 = 0")
    assert module == "equation_solver" or module == "basic_math"


@pytest.mark.asyncio
async def test_calculator_agent_full_flow(mock_gemini_agent):
    """CalculatorAgent tam akış testi"""
    with patch('src.main.settings.validate'), \
         patch('src.main.GeminiAgent', return_value=mock_gemini_agent), \
         patch('src.main.BasicMathModule') as mock_module_class:
        mock_module = mock_module_class.return_value
        result_mock = MagicMock(
            result=4.0,
            steps=["2 + 2 = 4"],
            confidence_score=1.0,
            visual_data=None,
            error=None,
        )
        mock_module.calculate = AsyncMock(return_value=result_mock)

        agent = CalculatorAgent()
        result = await agent.process_command("2 + 2")

        assert "✅ Sonuc:" in result
        assert "4" in result.splitlines()[0]
        assert "📝 Adimlar:" in result

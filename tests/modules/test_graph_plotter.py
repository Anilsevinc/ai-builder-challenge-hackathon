"""Tests for graph plotter module"""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch
from src.modules.graph_plotter import GraphPlotterModule
from src.utils.exceptions import CalculationError


@pytest.mark.asyncio
async def test_graph_plotter_calculate_cache_hit(mock_gemini_agent, tmp_path):
    """Graph plotter - cache hit durumu"""
    with patch('src.modules.graph_plotter.Path', return_value=tmp_path):
        module = GraphPlotterModule(mock_gemini_agent)
        module.cache_dir = tmp_path
        module.plot_cache["x^2"] = str(tmp_path / "cached.png")

        result = await module.calculate("x^2")

        assert result.domain == "graph_plotter"
        assert "cache" in result.result.lower()
        assert result.visual_data is not None


@pytest.mark.asyncio
async def test_graph_plotter_calculate_cache_miss(mock_gemini_agent, tmp_path):
    """Graph plotter - cache miss durumu"""
    with patch('src.modules.graph_plotter.Path', return_value=tmp_path):
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

        with patch.object(
            module, '_create_plot', new_callable=AsyncMock
        ) as mock_plot:
            mock_plot.return_value = {"png": str(tmp_path / "plot.png")}

            result = await module.calculate("x^2")

            assert result.domain == "graph_plotter"
            assert mock_plot.called
            assert "x^2" in module.plot_cache


@pytest.mark.asyncio
async def test_graph_plotter_create_plot_2d(mock_gemini_agent, tmp_path):
    """Graph plotter - 2D plot oluşturma"""
    module = GraphPlotterModule(mock_gemini_agent)
    module.cache_dir = tmp_path

    visual_data = {
        "plot_type": "2d",
        "x_range": [-5, 5]
    }

    with patch('matplotlib.pyplot.savefig'), \
         patch('matplotlib.pyplot.close'), \
         patch('matplotlib.pyplot.figure'), \
         patch('matplotlib.pyplot.plot'), \
         patch('matplotlib.pyplot.grid'), \
         patch('matplotlib.pyplot.xlabel'), \
         patch('matplotlib.pyplot.ylabel'), \
         patch('matplotlib.pyplot.title'):
        result = await module._create_plot(visual_data, "x^2")

        assert "png" in result
        assert Path(result["png"]).suffix == ".png"


@pytest.mark.asyncio
async def test_graph_plotter_create_plot_3d(mock_gemini_agent, tmp_path):
    """Graph plotter - 3D plot (placeholder)"""
    module = GraphPlotterModule(mock_gemini_agent)
    module.cache_dir = tmp_path

    visual_data = {
        "plot_type": "3d",
        "x_range": [-10, 10]
    }

    with patch.object(module, '_plot_2d', new_callable=AsyncMock) as mock_2d:
        mock_2d.return_value = {"png": str(tmp_path / "plot.png")}

        result = await module._create_plot(visual_data, "x^2 + y^2")

        assert mock_2d.called
        assert "png" in result


@pytest.mark.asyncio
async def test_graph_plotter_create_plot_parametric(
    mock_gemini_agent, tmp_path
):
    """Graph plotter - parametrik plot"""
    module = GraphPlotterModule(mock_gemini_agent)
    module.cache_dir = tmp_path

    visual_data = {
        "plot_type": "parametric",
        "x_range": [-10, 10]
    }

    with patch.object(module, '_plot_2d', new_callable=AsyncMock) as mock_2d:
        mock_2d.return_value = {"png": str(tmp_path / "plot.png")}

        result = await module._create_plot(visual_data, "parametric")

        assert mock_2d.called
        assert result is not None


@pytest.mark.asyncio
async def test_graph_plotter_create_plot_polar(mock_gemini_agent, tmp_path):
    """Graph plotter - polar plot"""
    module = GraphPlotterModule(mock_gemini_agent)
    module.cache_dir = tmp_path

    visual_data = {
        "plot_type": "polar",
        "x_range": [-10, 10]
    }

    with patch.object(module, '_plot_2d', new_callable=AsyncMock) as mock_2d:
        mock_2d.return_value = {"png": str(tmp_path / "plot.png")}

        result = await module._create_plot(visual_data, "polar")

        assert mock_2d.called
        assert result is not None


@pytest.mark.asyncio
async def test_graph_plotter_create_plot_default(mock_gemini_agent, tmp_path):
    """Graph plotter - default plot type"""
    module = GraphPlotterModule(mock_gemini_agent)
    module.cache_dir = tmp_path

    visual_data = {
        "plot_type": "unknown",
        "x_range": [-10, 10]
    }

    with patch.object(module, '_plot_2d', new_callable=AsyncMock) as mock_2d:
        mock_2d.return_value = {"png": str(tmp_path / "plot.png")}

        result = await module._create_plot(visual_data, "test")
        assert result is not None

        assert mock_2d.called


@pytest.mark.asyncio
async def test_graph_plotter_plot_2d_exception(mock_gemini_agent, tmp_path):
    """Graph plotter - 2D plot exception handling"""
    module = GraphPlotterModule(mock_gemini_agent)
    module.cache_dir = tmp_path

    visual_data = {
        "plot_type": "2d",
        "x_range": [-10, 10]
    }

    with patch(
        'matplotlib.pyplot.savefig',
        side_effect=Exception("Plot error")
    ):
        with pytest.raises(CalculationError, match="Grafik olusturulamadi"):
            await module._plot_2d(visual_data, "x^2", [-10, 10])


def test_graph_plotter_load_cached_result(mock_gemini_agent):
    """Graph plotter - cache'den yükleme"""
    module = GraphPlotterModule(mock_gemini_agent)

    cached_path = "/path/to/cached.png"
    result = module._load_cached_result(cached_path)

    assert result.domain == "graph_plotter"
    assert "cache" in result.result.lower()
    assert result.visual_data["plot_paths"]["png"] == cached_path


@pytest.mark.asyncio
async def test_graph_plotter_calculate_exception(
    mock_gemini_agent, tmp_path
):
    """Graph plotter - calculate exception handling"""
    with patch('src.modules.graph_plotter.Path', return_value=tmp_path):
        mock_gemini_agent.generate_json_response.side_effect = Exception(
            "API Error"
        )

        module = GraphPlotterModule(mock_gemini_agent)
        module.cache_dir = tmp_path

        with pytest.raises(Exception, match="API Error"):
            await module.calculate("x^2")

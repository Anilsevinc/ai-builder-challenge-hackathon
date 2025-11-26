"""Tests for statistics module"""

import pytest
from src.modules.statistics import StatisticsModule


@pytest.mark.asyncio
async def test_statistics_mean(mock_gemini_agent):
    """Ortalama hesaplama testi"""
    # Mock'u "mean [1,2,3,4,5]" için doğru sonuç döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 3.0,
        "steps": [
            "Veri seti: [1, 2, 3, 4, 5]",
            "Ortalama = (1 + 2 + 3 + 4 + 5) / 5",
            "Ortalama = 15 / 5 = 3.0"
        ],
        "confidence_score": 1.0,
        "metadata": {
            "statistic_type": "mean",
            "sample_size": 5,
            "data_points": 5
        }
    }

    module = StatisticsModule(mock_gemini_agent)
    result = await module.calculate("mean [1,2,3,4,5]")

    assert result is not None
    assert result.domain == "statistics"
    assert result.confidence_score == 1.0
    assert result.result == 3.0
    assert len(result.steps) > 0
    assert result.metadata is not None
    assert result.metadata.get("statistic_type") == "mean"


@pytest.mark.asyncio
async def test_statistics_std_dev(mock_gemini_agent):
    """Standart sapma hesaplama testi"""
    # Mock'u "std dev [10,20,30,40,50]" için doğru sonuç
    # döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 15.811388300841896,  # Yaklaşık değer
        "steps": [
            "Veri seti: [10, 20, 30, 40, 50]",
            "Ortalama = 30",
            "Varyans = ((10-30)^2 + (20-30)^2 + (30-30)^2 + "
            "(40-30)^2 + (50-30)^2) / 5",
            "Varyans = 200",
            "Standart sapma = sqrt(200) ≈ 14.14"
        ],
        "confidence_score": 1.0,
        "metadata": {
            "statistic_type": "std_dev",
            "sample_size": 5,
            "data_points": 5
        }
    }

    module = StatisticsModule(mock_gemini_agent)
    result = await module.calculate("std dev [10,20,30,40,50]")

    assert result is not None
    assert result.domain == "statistics"
    assert result.confidence_score == 1.0
    assert isinstance(result.result, (int, float))
    assert len(result.steps) > 0
    assert result.metadata is not None
    assert result.metadata.get("statistic_type") == "std_dev"


@pytest.mark.asyncio
async def test_statistics_correlation(mock_gemini_agent):
    """Korelasyon hesaplama testi"""
    # Mock'u korelasyon için doğru sonuç döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 1.0,  # Mükemmel pozitif korelasyon
        "steps": [
            "X veri seti: [1, 2, 3, 4, 5]",
            "Y veri seti: [2, 4, 6, 8, 10]",
            "Pearson korelasyon katsayisi hesaplaniyor...",
            "r = 1.0 (Mukemmel pozitif korelasyon)"
        ],
        "confidence_score": 1.0,
        "metadata": {
            "statistic_type": "correlation",
            "sample_size": 5,
            "data_points": 5
        }
    }

    module = StatisticsModule(mock_gemini_agent)
    result = await module.calculate("correlation [1,2,3,4,5] [2,4,6,8,10]")

    assert result is not None
    assert result.domain == "statistics"
    assert result.confidence_score == 1.0
    assert isinstance(result.result, (int, float))
    assert -1.0 <= result.result <= 1.0  # Korelasyon -1 ile 1 arasında olmalı
    assert len(result.steps) > 0
    assert result.metadata is not None
    assert result.metadata.get("statistic_type") == "correlation"


@pytest.mark.asyncio
async def test_statistics_z_score(mock_gemini_agent):
    """Z-score hesaplama testi"""
    # Mock'u "z-score 75 mean=70 std=5" için doğru sonuç
    # döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 1.0,
        "steps": [
            "Z-score formulu: z = (x - μ) / σ",
            "z = (75 - 70) / 5",
            "z = 5 / 5 = 1.0",
            "Bu deger ortalamadan 1 standart sapma yukarida"
        ],
        "confidence_score": 1.0,
        "metadata": {
            "statistic_type": "z-score",
            "mean": 70.0,
            "std_dev": 5.0
        }
    }

    module = StatisticsModule(mock_gemini_agent)
    result = await module.calculate("z-score 75 mean=70 std=5")

    assert result is not None
    assert result.domain == "statistics"
    assert result.confidence_score == 1.0
    assert result.result == 1.0
    assert len(result.steps) > 0
    assert result.metadata is not None
    assert result.metadata.get("statistic_type") == "z-score"


@pytest.mark.asyncio
async def test_statistics_median(mock_gemini_agent):
    """Medyan hesaplama testi"""
    # Mock'u "median [10,20,30,40,50]" için doğru sonuç
    # döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 30.0,
        "steps": [
            "Veri seti: [10, 20, 30, 40, 50]",
            "Siralanmis veri: [10, 20, 30, 40, 50]",
            "Ornek boyutu: 5 (tek sayi)",
            "Medyan = (n+1)/2. eleman = 3. eleman = 30"
        ],
        "confidence_score": 1.0,
        "metadata": {
            "statistic_type": "median",
            "sample_size": 5,
            "data_points": 5
        }
    }

    module = StatisticsModule(mock_gemini_agent)
    result = await module.calculate("median [10,20,30,40,50]")

    assert result is not None
    assert result.domain == "statistics"
    assert result.confidence_score == 1.0
    assert result.result == 30.0
    assert len(result.steps) > 0
    assert result.metadata is not None
    assert result.metadata.get("statistic_type") == "median"

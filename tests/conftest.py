"""Pytest configuration and fixtures"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.core.agent import GeminiAgent


@pytest.fixture
def mock_gemini_agent():
    """Mock Gemini agent fixture
    
    NOT: Her test kendi mock'unu yapılandırmalı (return_value override etmeli).
    Bu default değerler sadece fallback olarak kullanılır.
    """
    agent = MagicMock(spec=GeminiAgent)
    agent.generate_json_response = AsyncMock(
        return_value={
            "result": 0.0,  # Nötr default değer - her test kendi değerini set etmeli
            "steps": [],
            "confidence_score": 1.0,
            # domain kaldırıldı - her modül kendi domain'ini set ediyor
        }
    )
    return agent


@pytest.fixture
def sample_expression():
    """Ornek ifade fixture"""
    return "2 + 2"


@pytest.fixture
def sample_calculus_expression():
    """Ornek kalkulus ifadesi"""
    return "derivative x^2 at x=2"


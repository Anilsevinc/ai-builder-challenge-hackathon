"""Tests for settings configuration"""

import os
import pytest
from unittest.mock import patch
from src.config import reload_settings


def test_settings_default_values():
    """Settings - varsayılan değerler"""
    with patch.dict(os.environ, {}, clear=True):
        with patch('src.config.settings.load_dotenv'):
            settings_module = reload_settings()
        settings = settings_module.Settings()
        assert settings.GEMINI_MODEL == "gemini-2.5-flash"
        assert settings.RATE_LIMIT_CALLS_PER_MINUTE == 60
        assert settings.TEMPERATURE == 0.1
        assert settings.TOP_P == 0.95
        assert settings.MAX_OUTPUT_TOKENS == 2048
        assert settings.MAX_RETRIES == 3
        assert settings.DEFAULT_CURRENCY == "TRY"


def test_settings_validate_success():
    """Settings - validation başarılı"""
    with patch.dict(
        os.environ, {'GEMINI_API_KEY': 'valid_api_key'}, clear=True
    ):
        with patch('src.config.settings.load_dotenv'):
            settings_module = reload_settings()
        settings = settings_module.Settings()
        assert settings.validate() is True


def test_settings_validate_empty_api_key():
    """Settings - validation: boş API key"""
    with patch.dict(os.environ, {'GEMINI_API_KEY': ''}, clear=True):
        with patch('src.config.settings.load_dotenv'):
            settings_module = reload_settings()
        settings = settings_module.Settings()
        with pytest.raises(
            ValueError,
            match=r"GEMINI_API_KEY environment variable gerekli",
        ):
            settings.validate()


def test_settings_validate_placeholder_api_key():
    """Settings - validation: placeholder API key"""
    with patch.dict(
        os.environ,
        {'GEMINI_API_KEY': 'your_gemini_api_key'},
        clear=True
    ):
        with patch('src.config.settings.load_dotenv'):
            settings_module = reload_settings()
        settings = settings_module.Settings()
        with pytest.raises(
            ValueError,
            match=r"GECERSIZ API KEY: Placeholder deger kullanilamaz",
        ):
            settings.validate()


def test_settings_environment_variables():
    """Settings - environment variable'larından yükleme"""
    with patch.dict(os.environ, {
        'GEMINI_API_KEY': 'test_key',
        'GEMINI_MODEL': 'test-model',
        'RATE_LIMIT_CALLS_PER_MINUTE': '30',
        'TEMPERATURE': '0.5',
        'TOP_P': '0.9',
        'MAX_OUTPUT_TOKENS': '1024',
        'MAX_RETRIES': '5',
        'DEFAULT_CURRENCY': 'USD',
    }, clear=True):
        with patch('src.config.settings.load_dotenv'):
            settings_module = reload_settings()
        settings = settings_module.Settings()
        assert settings.GEMINI_API_KEY == 'test_key'
        assert settings.GEMINI_MODEL == 'test-model'
        assert settings.RATE_LIMIT_CALLS_PER_MINUTE == 30
        assert settings.TEMPERATURE == 0.5
        assert settings.TOP_P == 0.9
        assert settings.MAX_OUTPUT_TOKENS == 1024
        assert settings.MAX_RETRIES == 5
        assert settings.DEFAULT_CURRENCY == 'USD'

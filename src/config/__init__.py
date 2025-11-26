"""Configuration module for Calculator Agent"""

import importlib

from . import settings as settings_module
from .settings import settings

__all__ = ['settings', 'reload_settings']


def reload_settings():
    """Reload settings module (useful for tests that mutate env)."""
    return importlib.reload(settings_module)

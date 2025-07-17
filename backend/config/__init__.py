"""
Configuration module for AI Job Hunt system
"""

from .settings import settings, Settings, OllamaSettings, OpenAISettings, DatabaseSettings

__all__ = [
    'settings',
    'Settings',
    'OllamaSettings',
    'OpenAISettings',
    'DatabaseSettings'
]

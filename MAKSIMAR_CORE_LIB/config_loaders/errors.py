from __future__ import annotations


class ConfigLoaderError(RuntimeError):
    """Base error for config loader layer."""


class ConfigDiscoveryError(ConfigLoaderError):
    """Raised when config discovery fails."""


class ConfigLoadError(ConfigLoaderError):
    """Raised when one config file cannot be loaded."""


class ConfigValidationError(ConfigLoaderError):
    """Raised when config validation fails critically."""

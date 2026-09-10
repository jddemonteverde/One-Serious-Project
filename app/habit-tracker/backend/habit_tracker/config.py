"""Application configuration resolved from environment variables.

Configuration is read from the process environment so the same source tree can
run in any environment without code changes. No environment-specific value is
hardcoded; every setting has a development-safe default that an operator can
override.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

SERVICE_NAME = "one-serious-project-api"

DEFAULT_APP_ENV = "local"
DEFAULT_APP_HOST = "127.0.0.1"
DEFAULT_APP_PORT = 8000
DEFAULT_LOG_LEVEL = "INFO"

SUPPORTED_LOG_LEVELS = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG")

MIN_PORT = 1
MAX_PORT = 65535


class ConfigurationError(RuntimeError):
    """Raised when the environment supplies an unusable configuration value."""


@dataclass(frozen=True)
class Settings:
    """Resolved application settings."""

    service_name: str
    app_env: str
    host: str
    port: int
    log_level: str


def load_settings(environ: Mapping[str, str] | None = None) -> Settings:
    """Build Settings from the environment.

    Args:
        environ: Environment mapping to read. Defaults to ``os.environ``.

    Raises:
        ConfigurationError: If a supplied value cannot be used.
    """
    source = os.environ if environ is None else environ

    return Settings(
        service_name=SERVICE_NAME,
        app_env=_read_non_empty(source, "APP_ENV", DEFAULT_APP_ENV),
        host=_read_non_empty(source, "APP_HOST", DEFAULT_APP_HOST),
        port=_read_port(source, "APP_PORT", DEFAULT_APP_PORT),
        log_level=_read_log_level(source, "LOG_LEVEL", DEFAULT_LOG_LEVEL),
    )


def _read_non_empty(source: Mapping[str, str], name: str, default: str) -> str:
    value = source.get(name, default).strip()
    if not value:
        raise ConfigurationError(f"{name} must not be empty.")
    return value


def _read_port(source: Mapping[str, str], name: str, default: int) -> int:
    raw = source.get(name, str(default)).strip()
    try:
        port = int(raw)
    except ValueError:
        raise ConfigurationError(f"{name} must be an integer, got {raw!r}.") from None

    if not MIN_PORT <= port <= MAX_PORT:
        raise ConfigurationError(
            f"{name} must be between {MIN_PORT} and {MAX_PORT}, got {port}."
        )
    return port


def _read_log_level(source: Mapping[str, str], name: str, default: str) -> str:
    level = source.get(name, default).strip().upper()
    if level not in SUPPORTED_LOG_LEVELS:
        supported = ", ".join(SUPPORTED_LOG_LEVELS)
        raise ConfigurationError(f"{name} must be one of: {supported}. Got {level!r}.")
    return level

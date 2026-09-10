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
DEFAULT_CORS_ALLOWED_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"

DEFAULT_DB_HOST = "127.0.0.1"
DEFAULT_DB_PORT = 5432
DEFAULT_DB_NAME = "osp_habit_tracker"
DEFAULT_DB_USER = "osp"
DEFAULT_DB_PASSWORD = ""

SUPPORTED_LOG_LEVELS = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG")

MIN_PORT = 1
MAX_PORT = 65535


class ConfigurationError(RuntimeError):
    """Raised when the environment supplies an unusable configuration value."""


@dataclass(frozen=True)
class Settings:
    """Resolved application settings.

    ``db_password`` is a secret. ``__repr__`` is overridden so that logging or
    printing a Settings object cannot leak it.
    """

    service_name: str
    app_env: str
    host: str
    port: int
    log_level: str
    cors_allowed_origins: tuple[str, ...]
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    def __repr__(self) -> str:
        """Render without the password, so log output can never expose it."""
        return (
            f"Settings(service_name={self.service_name!r}, app_env={self.app_env!r}, "
            f"host={self.host!r}, port={self.port}, log_level={self.log_level!r}, "
            f"cors_allowed_origins={self.cors_allowed_origins!r}, "
            f"db_host={self.db_host!r}, db_port={self.db_port}, "
            f"db_name={self.db_name!r}, db_user={self.db_user!r}, "
            "db_password='***')"
        )


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
        cors_allowed_origins=_read_origins(
            source, "CORS_ALLOWED_ORIGINS", DEFAULT_CORS_ALLOWED_ORIGINS
        ),
        db_host=_read_non_empty(source, "DB_HOST", DEFAULT_DB_HOST),
        db_port=_read_port(source, "DB_PORT", DEFAULT_DB_PORT),
        db_name=_read_non_empty(source, "DB_NAME", DEFAULT_DB_NAME),
        db_user=_read_non_empty(source, "DB_USER", DEFAULT_DB_USER),
        db_password=source.get("DB_PASSWORD", DEFAULT_DB_PASSWORD),
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


def _read_origins(
    source: Mapping[str, str], name: str, default: str
) -> tuple[str, ...]:
    """Parse a comma-separated origin list.

    An empty value is valid and disables cross-origin requests entirely, which
    is the correct setting when a reverse proxy serves the API and the frontend
    from one origin.
    """
    raw = source.get(name, default)
    origins = tuple(origin.strip() for origin in raw.split(",") if origin.strip())

    for origin in origins:
        if not origin.startswith(("http://", "https://")):
            raise ConfigurationError(
                f"{name} entries must start with http:// or https://, got {origin!r}."
            )
    return origins

"""FastAPI application entry point for the One Serious Project API.

The service is intentionally small. Its purpose is to provide a realistic
workload for the platform, delivery, and reliability milestones that follow.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from habit_tracker import habits
from habit_tracker.config import Settings, load_settings
from habit_tracker.storage import HabitStore

API_VERSION = "0.1.0"

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"

logger = logging.getLogger(__name__)


class ServiceStatus(BaseModel):
    """Service identity and running state returned by the root endpoint."""

    service: str
    status: str
    environment: str


def configure_logging(log_level: str) -> None:
    """Apply the configured log level to the root logger."""
    logging.basicConfig(level=log_level, format=LOG_FORMAT)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the FastAPI application.

    Args:
        settings: Settings to use. Loaded from the environment when omitted.
    """
    resolved = load_settings() if settings is None else settings
    configure_logging(resolved.log_level)

    application = FastAPI(
        title="One Serious Project API",
        description="Service API for One Serious Project.",
        version=API_VERSION,
    )
    application.state.settings = resolved
    application.state.habit_store = HabitStore()

    if resolved.cors_allowed_origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=list(resolved.cors_allowed_origins),
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @application.get("/", response_model=ServiceStatus, tags=["service"])
    def read_service_status() -> ServiceStatus:
        """Identify the service and report that it is running."""
        return ServiceStatus(
            service=resolved.service_name,
            status="running",
            environment=resolved.app_env,
        )

    application.include_router(habits.router)

    logger.info(
        "Application created service=%s environment=%s",
        resolved.service_name,
        resolved.app_env,
    )
    return application


app = create_app()

"""Console entry point that serves the API with ``python -m habit_tracker``.

The runner is separate from :mod:`habit_tracker.main` so that starting the server does not
build a second, discarded application instance: uvicorn imports ``habit_tracker.main``
itself using the import string below.
"""

from __future__ import annotations

import uvicorn

from habit_tracker.config import load_settings

APP_IMPORT_STRING = "habit_tracker.main:app"


def main() -> None:
    """Run the API using the configured host, port, and log level."""
    settings = load_settings()
    uvicorn.run(
        APP_IMPORT_STRING,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from logging import Logger
from pathlib import Path
from typing import Optional, Union

_DEFAULT_FORMAT = "%(asctime)s %(levelname)s %(name)s [run_id=%(run_id)s stage=%(stage)s elapsed_ms=%(elapsed_ms)s] %(message)s"


class _RunIdFilter(logging.Filter):
    def __init__(self, run_id: Optional[str] = None) -> None:
        super().__init__()
        self._run_id = run_id or "-"

    def filter(self, record: logging.LogRecord) -> bool:  # type: ignore[override]
        if not hasattr(record, "run_id") or record.run_id is None:
            record.run_id = self._run_id
        if not hasattr(record, "stage") or record.stage is None:
            record.stage = "-"
        if not hasattr(record, "elapsed_ms") or record.elapsed_ms is None:
            record.elapsed_ms = "-"
        return True


def setup_logging(
    log_file: Optional[Union[str, Path]] = None,
    level: Union[str, int] = "INFO",
    run_id: Optional[str] = None,
    fmt: str = _DEFAULT_FORMAT,
) -> None:
    """Configure root logging with optional file output and run_id injection."""

    log_level = logging.getLevelName(level) if isinstance(level, str) else level
    logging.root.handlers.clear()
    logging.root.setLevel(log_level)

    formatter = logging.Formatter(fmt)
    run_filter = _RunIdFilter(run_id)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(run_filter)
    logging.root.addHandler(stream_handler)

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(run_filter)
        logging.root.addHandler(file_handler)


def get_logger(name: str) -> Logger:
    """Return a module-specific logger (setup_logging should be called once)."""

    return logging.getLogger(name)


@contextmanager
def log_timing(logger: Logger, stage: str, run_id: Optional[str] = None):
    start = time.perf_counter()
    try:
        yield
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "stage completed",
            extra={"stage": stage, "elapsed_ms": elapsed_ms, "run_id": run_id},
        )
    except Exception:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        logger.exception(
            "stage failed",
            extra={"stage": stage, "elapsed_ms": elapsed_ms, "run_id": run_id},
        )
        raise

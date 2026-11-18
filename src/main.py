"""The entry point. It reads the configuration, starts the server, and stops it on a signal."""

from __future__ import annotations

import json
import logging
import signal
import sys
import threading
from datetime import UTC, datetime
from typing import ClassVar, override

import config
import server

logger = logging.getLogger(__name__)


class JsonFormatter(logging.Formatter):
    """Writes one JSON object per line, with the time, the level, the message, and the fields."""

    LEVELS: ClassVar[dict[str, str]] = {"WARNING": "WARN", "CRITICAL": "ERROR"}

    @override
    def format(self, record: logging.LogRecord) -> str:
        """Format one record."""
        entry: dict[str, object] = {
            "time": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": self.LEVELS.get(record.levelname, record.levelname),
            "msg": record.getMessage(),
        }
        entry.update(getattr(record, "fields", {}))
        return json.dumps(entry, separators=(",", ":"))


def main() -> int:
    """Serve until SIGINT or SIGTERM, then let the open requests finish. Return the exit code."""
    try:
        cfg = config.from_env()
    except config.ConfigError as error:
        _ = sys.stderr.write(f"{error}\n")
        return 1

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=cfg.log_level, handlers=[handler])

    httpd = server.make_server(cfg.port)
    stop = threading.Event()
    for signum in (signal.SIGINT, signal.SIGTERM):
        _ = signal.signal(signum, lambda *_: stop.set())

    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()
    logger.info("listening", extra={"fields": {"port": cfg.port}})

    _ = stop.wait()
    httpd.shutdown()
    httpd.server_close()
    thread.join()
    logger.info("stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())

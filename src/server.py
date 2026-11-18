"""The HTTP routes of the app."""

from __future__ import annotations

import logging
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import override
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)

HEALTH_BODY = b'{"status":"ok"}'


class Handler(BaseHTTPRequestHandler):
    """Answers `GET /health`, and 404 to every other path."""

    def do_GET(self) -> None:
        """Answer one GET request."""
        path = urlsplit(self.path).path
        status, body = (HTTPStatus.OK, HEALTH_BODY) if path == "/health" else (HTTPStatus.NOT_FOUND, b"")
        self.send_response(status)
        if path == "/health":
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        _ = self.wfile.write(body)
        logger.debug("request", extra={"fields": {"method": "GET", "path": path, "status": status.value}})

    @override
    def log_message(self, format: str, *args: object) -> None:
        """Leave the request log to the debug line of `do_GET`."""


class Server(ThreadingHTTPServer):
    """A server that waits for the open requests when it closes."""

    daemon_threads = False
    block_on_close = True


def make_server(port: int) -> Server:
    """Bind a server to `port` on every address. Port 0 picks a free port."""
    return Server(("", port), Handler)

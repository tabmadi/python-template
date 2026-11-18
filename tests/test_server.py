"""Tests for the HTTP routes."""

import threading
import urllib.error
import urllib.request
from collections.abc import Iterator
from http import HTTPStatus

import pytest

import server


@pytest.fixture
def base_url() -> Iterator[str]:
    """Serve on a free port for one test."""
    httpd = server.make_server(0)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()
    httpd.server_close()
    thread.join()


def test_health(base_url: str) -> None:
    """`GET /health` answers 200 with the status."""
    with urllib.request.urlopen(f"{base_url}/health") as response:  # noqa: S310 - the URL is the local test server.
        assert response.status == HTTPStatus.OK
        assert response.read() == b'{"status":"ok"}'


@pytest.mark.parametrize("path", ["/missing", "/"])
def test_unknown_path(base_url: str, path: str) -> None:
    """Every other path answers 404."""
    with pytest.raises(urllib.error.HTTPError) as error:
        urllib.request.urlopen(f"{base_url}{path}")  # noqa: S310 - the URL is the local test server.
    assert error.value.code == HTTPStatus.NOT_FOUND

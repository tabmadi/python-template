"""Tests for the application entry point."""

import logging
from typing import TYPE_CHECKING

from main import main

if TYPE_CHECKING:
    import pytest


def test_main_logs_a_greeting(caplog: pytest.LogCaptureFixture) -> None:
    """`main()` logs one greeting at INFO."""
    with caplog.at_level(logging.INFO):
        main()

    assert caplog.messages == ["Hello world!"]

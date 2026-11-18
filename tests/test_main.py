"""Tests for the application entry point."""

import logging

import pytest

from main import main


def test_main_logs_a_greeting(caplog: pytest.LogCaptureFixture) -> None:
    """`main()` logs one greeting at INFO."""
    with caplog.at_level(logging.INFO):
        main()

    assert caplog.messages == ["Hello world!"]

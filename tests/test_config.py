"""Tests for the configuration."""

import logging

import pytest

import config


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ({}, config.Config(port=config.DEFAULT_PORT, log_level=logging.INFO)),
        ({"PORT": "", "LOG_LEVEL": ""}, config.Config(port=config.DEFAULT_PORT, log_level=logging.INFO)),
        ({"PORT": "9000", "LOG_LEVEL": "DEBUG"}, config.Config(port=9000, log_level=logging.DEBUG)),
    ],
    ids=["defaults", "empty values take the defaults", "overrides"],
)
def test_load(env: dict[str, str], expected: config.Config) -> None:
    """A valid environment gives its configuration."""
    assert config.load(env) == expected


@pytest.mark.parametrize(
    "env",
    [{"PORT": "abc"}, {"PORT": "70000"}, {"LOG_LEVEL": "loud"}],
    ids=["port is not a number", "port is out of range", "unknown log level"],
)
def test_load_rejects(env: dict[str, str]) -> None:
    """A bad value stops the load with an error that names the variable."""
    with pytest.raises(config.ConfigError, match=next(iter(env))):
        _ = config.load(env)

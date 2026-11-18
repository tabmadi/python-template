"""Read the configuration from the environment and check it. No other module reads the environment."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

PORT = "PORT"
LOG_LEVEL = "LOG_LEVEL"
DEFAULT_PORT = 8080
MAX_PORT = 65535
PORT_RULE = f"a number from 1 to {MAX_PORT}"
LOG_LEVEL_RULE = "debug, info, warn, or error"
LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "error": logging.ERROR,
}


class ConfigError(ValueError):
    """A configuration value that the app cannot start with."""

    def __init__(self, name: str, rule: str, value: str) -> None:
        """Name the variable, the rule it breaks, and its value."""
        super().__init__(f'invalid configuration: {name} must be {rule}, not "{value}"')


@dataclass(frozen=True, slots=True)
class Config:
    """The checked configuration of the app."""

    port: int = DEFAULT_PORT
    log_level: int = logging.INFO


def from_env() -> Config:
    """Read the configuration from the environment of the process."""
    return load(os.environ)


def load(env: Mapping[str, str]) -> Config:
    """Read the configuration from `env`. An unset or empty variable takes its default."""
    port = DEFAULT_PORT
    value = env.get(PORT, "")
    if value != "":
        port = int(value) if value.isascii() and value.isdigit() else 0
        if not 1 <= port <= MAX_PORT:
            raise ConfigError(PORT, PORT_RULE, value)

    log_level = logging.INFO
    value = env.get(LOG_LEVEL, "")
    if value != "":
        if value.lower() not in LEVELS:
            raise ConfigError(LOG_LEVEL, LOG_LEVEL_RULE, value)
        log_level = LEVELS[value.lower()]

    return Config(port=port, log_level=log_level)

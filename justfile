# Every task, per ADR-0103. A recipe that calls a tool runs only inside the dev shell of flake.nix.

set shell := ["bash", "-euo", "pipefail", "-c"]

import? 'template/justfile'

# List the recipes
default:
    @just --list

# Build the dev shell, install the locked environment, and install the git hooks
setup:
    nix develop --command uv sync --locked

# Run the app
run: in-shell
    uv run python src/main.py

# Run the tests
test: in-shell
    uv run pytest

# ruff with every rule, the ruff format check, and the pyrefly type check
lint-py: in-shell
    ruff check --config .config/ruff.toml .
    ruff format --config .config/ruff.toml --check .
    pyrefly check --python-interpreter-path .venv/bin/python

# Prose, comments, and ADRs, per ADR-0001
lint-prose: in-shell
    tablint check

# Markdown structure and formatting, per ADR-0001
lint-md: in-shell
    rumdl check .

# Scan the working tree for committed secrets
lint-secrets: in-shell
    gitleaks dir . --no-banner

# JSON, JSONC, TOML, and YAML format, per ADR-0104
lint-data: in-shell
    dprint check

# Nix format, per ADR-0104
lint-nix: in-shell
    nixfmt --check $(git ls-files '*.nix')

# justfile format, per ADR-0104
lint-just:
    just --fmt --check

# Run every linter
lint: lint-py lint-prose lint-md lint-secrets lint-data lint-nix lint-just

# Apply every formatter and every safe lint fix
format: in-shell
    ruff check --config .config/ruff.toml --fix .
    ruff format --config .config/ruff.toml .
    rumdl check --fix .
    nixfmt $(git ls-files '*.nix')
    dprint fmt
    just --fmt

# The fast gate: run it before you finish a change
check: lint test

# Run exactly what CI runs: every check of flake.nix, in the Nix sandbox
ci:
    nix flake check --print-build-logs

# Push what CI built to the binary cache, per ADR-0101. Without NIX_CACHE_URL it does nothing
cache-push: in-shell
    nix-cache-push

[private]
in-shell:
    @test -n "${IN_NIX_SHELL:-}" || { echo "Enter the dev shell first: run nix develop, or allow direnv." >&2; exit 1; }

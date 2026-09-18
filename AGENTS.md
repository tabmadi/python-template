# Agent guide

Tool-agnostic guide for any coding agent (Codex, Cursor, Claude Code, or another) working in this repo. `AGENTS.md` is the one standard: an agent either reads it or it does not — the repo carries no per-tool shim files (`CLAUDE.md`, `.cursor/rules/`, etc.). A tool that ignores `AGENTS.md` is a limitation of that tool, not something the repo works around.

## The one rule that outranks this file

**Humans are the first developers. [README.md](README.md) outranks this file.** It is the human-facing description of what this template provides and how to use it. This file holds only agent-specific operational hints: how to navigate, build, and run the repo.

## What this repo is

A Python application template using the `src` layout, `uv` for dependency resolution, `ruff` for lint and format, and `pyrefly` for type checking. The sample code is a demonstration seam, not a feature set.

- **Everything here is inherited wholesale** by every project generated from it. A dependency added here is a dependency every generated project carries, so add one only when the template itself needs it.
- Application code lives under `src/`. Nothing is imported from the repository root.
- `pyproject.toml` is the single source of truth for dependencies and tool configuration. There is no `requirements.txt`, no `setup.py`, and no per-tool dotfile.
- `uv.lock` is committed and authoritative. Change dependencies through `uv add` / `uv remove`, never by hand-editing the lock file.

## Working in the repo

- The task runner is `mise` (root `mise.toml`); commands are `mise run <task>`. `mise run setup` installs the git hooks.
- Tools are pinned and installed by `mise`; a shell with mise inactive resolves a bare tool call (`python`, `uv`, `ruff`, …) from `PATH`, at an unpinned version. `mise run <task>` activates the toolchain for that task's duration, a bare tool call does not.
- Run anything Python through `uv run`, which resolves the locked environment. A bare `python script.py` uses whatever interpreter `PATH` offers and a different dependency set.
- `mise run act` replays the pull request workflow locally with [act](https://github.com/nektos/act). It reads secrets from `.env` — copy `.env.example` first.
- Before finishing a change, run `mise run check` to format, lint, typecheck, and test; `mise run format` / `lint` / `typecheck` / `test` run each individually.

## Conventions

- **`ruff` is the arbiter**, and it runs with `select = ["ALL"]`. Every rule is on unless [pyproject.toml](pyproject.toml) names it in `ignore`, with a comment saying why.
- Never silence a rule with a bare `# noqa`. Fix the code, or annotate the single line with the specific rule code and a reason. A rule that is wrong for the whole project belongs in the `ignore` list, with its justification.
- **Type hints are mandatory** on every function signature; `pyrefly` checks them in `mise run typecheck`.
- Docstrings follow the ruff `D` rules — every module, class, and public function has one.
- Tests use `pytest` and live in `tests/`, mirroring the `src/` layout.

## Commits

- **Conventional Commits, enforced.** `cog verify` runs on `commit-msg` and `cog check` on `pre-push`, so a malformed message is rejected locally before CI sees it.
- Commit messages are a title only — no body, no footer.
- Never push unless asked to.

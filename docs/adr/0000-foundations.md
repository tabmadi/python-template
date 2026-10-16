# ADR-0000: Foundations

**Status:** Accepted
**Decides:** What this repo is, its layout, its Python conventions, and the ADR process itself.

## Context

A Python project starts with the same choices every time: the layout, the package manager, the linter set, and the type checker. Each has several popular answers, and a mix of them costs time on every project. A template makes these choices once, so a new project starts at its first feature.

## Decision

This repo is a Python application template. It starts from [github-project-template](https://github.com/tabmadi/github-project-template) and adds the Python toolchain. The sample code shows the structure. It is not a feature set.

| Path | Holds |
| --- | --- |
| `src/` | The application code. Nothing is imported from the repo root |
| `tests/` | The pytest tests, in the same layout as `src/` |
| `pyproject.toml` | The dependencies and every tool config |
| `uv.lock` | The locked dependency set. It is committed |

**`pyproject.toml` is the one config file.** There is no `requirements.txt`, no `setup.py`, and no per-tool config file.

**`uv` owns the environment.** Python code runs through `uv run`, which uses the locked environment. A bare `python` call uses the interpreter on `PATH` and a different dependency set.

**Every decision is an ADR.** An ADR states what is true of the repo. It is law, not a plan. Planned work lives in an untracked `*.local.md` file.

## Consequences

A dependency added here is a dependency of every generated project. So the template adds one only when the template itself needs it.

A generated project inherits these ADRs. So an ADR is written for the engineer who maintains the project. Selection guidance belongs in the root `README.md`.

## Rules

- Application code lives under `src/`. Tests live under `tests/`.
- Dependencies change through `uv add` and `uv remove`. `uv.lock` is never edited by hand.
- A test-only dependency is in the `dev` dependency group.
- Every function signature has type hints. `(CI: lint:py)`
- Every module, class, and public function has a docstring. `(CI: lint:py)`
- A `# noqa` names one rule and gives a reason. A rule that is wrong for the whole project is in the `ignore` list of `pyproject.toml`, with a reason. `(CI: lint:py)`
- Every ADR carries a `Status`, a one-sentence `Decides` line, and a flat `Rules` section.
- Planned work lives in an untracked `*.local.md` file. No committed file links to one.

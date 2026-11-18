# ADR-0000: Foundations

- **Status:** Accepted
- **Decides:** What this repo is, its layout, its Python conventions, the recipe contract, and how ADRs work.

## Context

A Python project makes the same choices every time: the layout, the package manager, the linter and formatter, the type checker, and the test runner. This repo writes them down once, so each change starts at the feature.

A repo without written decisions loses the reason for each choice. The next engineer removes a check that has a reason, or adds a second tool for a job that one tool already does.

A repo also needs fixed entry points. An engineer or a coding agent that knows the name of the gate runs it without reading every file first.

## Decision

This repo is a Python application.

| Path | Holds |
| --- | --- |
| `src/` | The application code. Nothing is imported from the repo root |
| `tests/` | The pytest tests, in the same layout as `src/` |
| `pyproject.toml` | The project, its dependencies, and the pytest settings |
| `uv.lock` | The locked dependency set |

**`uv` owns the environment.** Python code runs through `uv run`, which uses the locked environment. A bare `python` call outside it has a different dependency set.

**The recipe names are a contract.** The recipes `setup`, `format`, `lint`, `test`, `check`, and `ci` always exist, per [ADR-0100](0100-toolchain.md). Their names do not change.

**Every decision is an ADR.** An ADR states a rule as true now. A gap between an ADR and the code is a defect in the code.

**An ADR has a fixed shape.** It has a `Status`, a one-sentence `Decides` line, and the sections `Context`, `Decision`, `Consequences`, and `Rules`. The `Rules` section is a flat list, so a grep over all ADRs finds every convention.

**Inside this repo, an ADR links only to other ADRs.** A README or a guide moves, and the ADR outlives it. A link to a published standard is allowed.

## Consequences

An ADR is for the engineer who maintains the repo. The root `README.md` helps a reader choose the repo and start.

The Python line is in two places: the dev shell of `flake.nix` and `requires-python` in `pyproject.toml`. A change updates both.

## Rules

- Application code lives under `src/`. Tests live under `tests/`.
- Dependencies change through `uv add` and `uv remove`. `uv.lock` is never edited by hand.
- A test-only dependency is in the `dev` dependency group.
- Every function signature has type hints. `(CI: lint-py)`
- Every module, class, and public function has a docstring. `(CI: lint-py)`
- A `# noqa` names one rule and gives a reason. A rule that is wrong for the whole project is in the `ignore` list of `.config/ruff.toml`, with a reason. `(CI: lint-py)`
- Every ADR has a `Status`, a one-sentence `Decides` line, and a flat `Rules` section.
- Inside this repo, an ADR links only to other ADRs.
- The recipes `setup`, `format`, `lint`, `test`, `check`, and `ci` exist, and their names do not change.

# ADR-0100: Toolchain

**Status:** Accepted
**Decides:** The pinned toolchain, the task surface, what runs at commit and push time, and how the pins stay current.

## Context

The value of a template is that its tool choices are made and reproducible. Three failures matter. The first is a tool that resolves from `$PATH`, at the version the machine has. The second is a check that only CI runs, which every local commit passes. The third is a pin that nobody updates.

## Decision

`mise` pins every tool and is the only command surface. A command is `mise run <task>`.

| Tool | Owns |
| --- | --- |
| python | The interpreter |
| uv | The environment, the lock file, and running code |
| ruff | Lint and format, with every rule enabled |
| pyrefly | Type checking |
| pytest | Tests, as a `dev` dependency |
| lefthook | Git hooks |
| cocogitto | Commit message shape |
| rumdl | Markdown style |
| gitleaks | Secret scanning |
| Renovate | Updates to the pins |

`ruff` is both the linter and the formatter. It runs with `select = ["ALL"]`, and `pyproject.toml` disables each exception by code with a reason. The line length is 120.

A hook has no active mise shell, so each hook command runs its tool through `mise x` or a `mise` task. The `pre-commit` hook runs `ruff`, `pyrefly`, `rumdl`, and `gitleaks`. The `pre-push` hook runs `cog check` on the commits that the push adds, and `mise run ci`.

The CI workflow runs `mise run ci` on every push to `master` and on every pull request. On a pull request, it also verifies the title with `cog`. Renovate opens a pull request for a new tool, package, or Action version, and the CI gate decides.

## Consequences

`ruff` with every rule enabled is strict. A new rule in an update can fail the gate on unchanged code, and the fix is a code change or a named exception.

Renovate needs the Renovate GitHub app on the repository. Without it, the pins go stale.

## Rules

- Every tool is pinned in `.mise.toml`. No tool is resolved from `$PATH`.
- Every command is a `mise` task with a `description`. A CI workflow step calls a task, never a tool directly.
- A git hook runs every tool through `mise x` or a `mise` task.
- A ruff rule is disabled by code with a reason in `pyproject.toml`. `(CI: lint:py)`
- Commit messages and pull request titles follow Conventional Commits with the type set in `cog.toml`. `(ref: Conventional Commits 1.0.0)`
- `mise run check` passes before a change is finished.
- A workflow never puts event text, such as a pull request title, directly into a `run` script.

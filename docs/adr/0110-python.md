# ADR-0110: Python

- **Status:** Accepted
- **Decides:** uv, ruff, pyrefly, and pytest are the Python tools, and uv2nix builds the environment of `uv.lock` for the checks.

## Context

The shared toolchain of [ADR-0100](0100-toolchain.md) holds no language. This ADR adds the tools of Python: the environment and the lock, the linter and the formatter, the type checker, the test runner, and how Nix builds the locked environment.

A Python wheel with native code links against system libraries. A Python from Nix does not give it the libraries that a usual Linux system has.

## Decision drivers

1. **One lock.** One lock file pins the whole environment, with the hash of each package.
2. **Few tools.** One tool for several jobs where it can.
3. **Fast.** A check that runs on each commit finishes in seconds.
4. **Strict.** The type checker follows the typing specification closely.
5. **Maintained.** The project is active.

## Considered options

### The environment and the lock

| Option | 1 One lock | 2 Few tools | Verdict |
| --- | --- | --- | --- |
| pip with pip-tools | `requirements.txt` per group | pip, pip-tools, and venv | Rejected on driver 2 |
| Poetry | `poetry.lock` | One tool | Rejected. Its Nix bridge poetry2nix has no maintainer, and its author points to uv2nix |
| PDM | `pdm.lock` | One tool | Rejected. A smaller user base than uv for the same model |
| **uv** | **`uv.lock`, one file for every platform** | **One tool: environment, lock, Python runs, and tools** | **Chosen** |

Sources:

- [uv](https://docs.astral.sh/uv/), [Poetry](https://python-poetry.org/), [PDM](https://pdm-project.org/).
- poetry2nix looks for a maintainer, and points to uv2nix: [poetry2nix](https://github.com/nix-community/poetry2nix).

### The linter and the formatter

| Option | 2 Few tools | 3 Fast | Verdict |
| --- | --- | --- | --- |
| flake8, isort, and black | Three tools and three configs | Python speed | Rejected on drivers 2 and 3 |
| pylint and black | Two tools | Slow on a large project | Rejected on drivers 2 and 3 |
| **ruff with every rule** | **One tool. It implements the rules of flake8, isort, and many plugins, and formats like black** | **Yes, written in Rust** | **Chosen** |

Sources:

- [ruff rules](https://docs.astral.sh/ruff/rules/), [ruff formatter](https://docs.astral.sh/ruff/formatter/).

### The type checker

| Option | 3 Fast | 4 Strict | 2 Few tools | 5 Maintained | Verdict |
| --- | --- | --- | --- | --- | --- |
| mypy | Seconds on a mid-size project, faster with its parallel mode | 58 to 77 percent of the conformance tests | A Python package | Yes | Rejected on drivers 3 and 4 |
| basedpyright | Several times slower than pyrefly | 94 to 98 percent, with an `all` mode of extra rules | Runs on Node.js, 227 MiB with its runtime | Yes | Rejected. It equals pyrefly on conformance and carries a second runtime. It stays the choice for a repo that wants its extra rules |
| ty | Fast | 53 to 82 percent | One binary | Beta | Rejected on drivers 4 and 5 |
| **pyrefly** | **The fastest** | **88 to 98 percent, with an `all` preset** | **One binary, 83 MiB** | **Stable since 1.0.0 in May 2026** | **Chosen** |

Each percentage is the range of published runs of the conformance suite of the typing specification. A run measures one version of each checker, so the newer runs rate pyrefly higher.

Sources:

- The March 2026 run: pyright 97.8, pyrefly 87.8, mypy 58.3, and ty 53.2 percent: [Typing spec conformance comparison](https://docs.bswen.com/blog/2026-03-17-python-type-checker-conformance-comparison/).
- A July 2026 run by another type checker, Basilisk: pyrefly 97.9, pyright 96.8, ty 82.3, and mypy 77.3 percent: [Basilisk comparison](https://www.basilisk-python.dev/docs/comparison/).
- The comparison page of pyrefly: [pyrefly compared with mypy and pyright](https://pyrefly.org/en/docs/compare/).
- Speed: [Pyrefly speed and memory comparison](https://pyrefly.org/blog/speed-and-memory-comparison/).
- [basedpyright](https://docs.basedpyright.com/), and Zed has pyrefly built in, beside its default basedpyright: [Zed Python docs](https://zed.dev/docs/languages/python).

### The environment in Nix

| Option | 1 One lock | 5 Maintained | Verdict |
| --- | --- | --- | --- |
| The Python packages of `nixpkgs` | No. The versions of `nixpkgs`, not of `uv.lock` | Yes | Rejected on driver 1 |
| poetry2nix | Needs Poetry | No maintainer | Rejected |
| **uv2nix** | **Yes. It reads `uv.lock`** | **Yes** | **Chosen** |

Sources:

- [uv2nix](https://github.com/pyproject-nix/uv2nix).

## Decision

uv owns the virtual environment in `.venv/`, and the dev shell holds its Python. uv uses that Python and never downloads one, through `UV_PYTHON` and `UV_PYTHON_DOWNLOADS=never` in `tabnix.env`.

A wheel with native code links against the C++ runtime and zlib. The dev shell puts both on `LD_LIBRARY_PATH`, so a wheel such as `numpy` loads.

The Python line is 3.15: `flake.nix` takes `python315`, and `requires-python` in `pyproject.toml` names the same line.

pyrefly runs with its `all` preset, set in `[tool.pyrefly]` of `pyproject.toml`. Both the check and the language server of Zed read it there. Without a config, pyrefly falls back to its lenient `basic` preset, and Zed shows no type errors.

ruff is both the linter and the formatter. `.config/ruff.toml` enables every rule and ignores each exception by name with a reason. Every recipe, check, hook, and Zed setting passes `--config .config/ruff.toml`. pytest reads its settings from `pyproject.toml`, beside the project it tests.

| File type | Formatter |
| --- | --- |
| Python | ruff, with four spaces, per PEP 8 |

The checks need the locked environment, and the Nix sandbox has no network. So uv2nix builds the environment of `uv.lock` from the hashes in the lock. `uv.lock` is the only lock file.

## Consequences

- ruff with every rule is strict. A new rule in a lock update can fail the gate on unchanged code, and the fix is a code change or a named exception.
- pyrefly has no counterpart for some extra rules of basedpyright, such as `reportAny`.
- A wheel with native code that needs a library beyond the C++ runtime and zlib needs that library in `tabnix.env` too.

## Rules

- A ruff rule is ignored by name with a reason in `.config/ruff.toml`. `(CI: lint-py)`
- `requires-python` and `flake.nix` name the same Python line. `(CI: lint-prose)`
- Python code runs through `uv run`, or in the checks through the environment of uv2nix.
- `uv.lock` is the only lock file.
- pyrefly runs with the `all` preset of `pyproject.toml`. `(CI: lint-py)`

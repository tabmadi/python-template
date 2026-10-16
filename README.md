# Python Template

A template for a Python application. It uses the `src` layout, `uv` for the environment and the lock file, `ruff` with every rule enabled, and `pyrefly` for type checks. It starts from [github-project-template](https://github.com/tabmadi/github-project-template), so it has the same hooks, CI gate, and documentation convention.

## Stack

| Tool | Owns |
| --- | --- |
| [Python](https://www.python.org) | The interpreter |
| [uv](https://docs.astral.sh/uv/) | The environment, the lock file, and running code |
| [ruff](https://docs.astral.sh/ruff/) | Lint and format |
| [pyrefly](https://pyrefly.org) | Type checks |
| [pytest](https://docs.pytest.org) | Tests |
| [mise](https://mise.jdx.dev) | Tool versions and tasks |
| [lefthook](https://github.com/evilmartians/lefthook) | Git hooks |
| [cocogitto](https://docs.cocogitto.io) | Conventional Commits checks |
| [rumdl](https://github.com/rvben/rumdl) | Markdown lint |
| [gitleaks](https://github.com/gitleaks/gitleaks) | Secret scan |
| [Renovate](https://docs.renovatebot.com) | Updates to the pinned versions |

## Getting started

1. Install [mise](https://mise.jdx.dev/getting-started.html).
2. Clone the repo and install the tools, dependencies, and hooks:

   ```bash
   git clone git@github.com:tabmadi/python-template.git
   cd python-template
   mise install
   mise run setup
   ```

3. Run the app:

   ```bash
   mise run run
   ```

## Tasks

| Task | Does |
| --- | --- |
| `mise run setup` | Installs the locked dependencies and the git hooks |
| `mise run run` | Runs the app |
| `mise run format` | Applies every formatter and every safe lint fix |
| `mise run lint` | Runs `lint:py`, `lint:md`, and `lint:secrets` |
| `mise run test` | Runs the tests |
| `mise run check` | Runs `lint` and `test`. Run it before you finish a change |
| `mise run ci` | Runs exactly what CI runs. The `pre-push` hook runs it too |

## Layout

```text
.
├── src/main.py       The entry point
├── tests/            The pytest tests
├── docs/adr/         The decisions: foundations, doc conventions, toolchain
├── pyproject.toml    The dependencies and every tool config
├── uv.lock           The locked dependency set
├── .mise.toml        Tool pins and tasks
└── .lefthook.yml     Git hooks
```

## Using this template

1. Create a repository from this template on GitHub.
2. Change `name` and `description` in `pyproject.toml`.
3. Replace `src/main.py` and its test with your own code.
4. Update the contacts in `SECURITY.md` and the copyright line in `LICENSE`.
5. Install the [Renovate app](https://github.com/apps/renovate) on the new repository.

## Decisions

The ADRs in [docs/adr](docs/adr/README.md) record every decision and the reason for it. [ADR-0001](docs/adr/0001-documentation-conventions.md) is the house style for all text.

## Contributing

Follow the [Code of Conduct](CODE_OF_CONDUCT.md). Commit messages follow [Conventional Commits](https://www.conventionalcommits.org), and the `commit-msg` hook checks them. Run `mise run check` before you open a pull request.

## Security

To report a vulnerability, follow [SECURITY.md](SECURITY.md).

## License

Apache License 2.0. See [LICENSE](LICENSE).

# Contributing to Password-Hash-Tool

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/Password-Hash-Tool.git
   cd Password-Hash-Tool
   ```
3. Create a virtual environment and install dev dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Make your changes
3. Run lint and tests:
   ```bash
   ruff check src/
   pytest
   ```
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "feat: add support for new algorithm"
   ```
5. Push and open a Pull Request against `main`

## Commit Convention

This project follows [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation only
- `refactor:` — code change that neither fixes a bug nor adds a feature
- `test:` — adding or correcting tests
- `chore:` — maintenance tasks

## Code Style

- Code is formatted and linted with [ruff](https://docs.astral.sh/ruff/)
- Type hints are expected on public functions
- Tests are required for new features and bug fixes

## Pull Request Guidelines

- Keep PRs focused on a single concern
- Ensure CI passes before requesting review
- Update documentation if behavior changes
- Add tests covering the new or changed behavior

## Security

If you discover a security vulnerability, please do **not** open a public issue. Instead, contact the maintainer directly.

# Organisation App
## Project Scope
The goal of this project is a multi-purpose organisation app written in python,
which should be modular and easily extendable and scalable.

## Main Features
* **Recipe Management:** Create and store recipes for meal planning.
* **Meal Planning:** Schedule meals and menus over defined time intervals.
* **Shopping List Generation:** Automatically generate shopping lists based on current food stock and planned menus.

## Quickstart
### Prerequisites
* [uv](https://docs.astral.sh/uv/) (python project management tool)

### Installation & Execution
```bash
# Install dependencies
uv sync

# Run the application
uv run main.py

# Run local QA checks before pushing
uv run poe qa

# Poethepoet task which automatically runs the following commands in that order:
uv run ruff check --fix
uv run ruff format
uv run pytest
```

## Further Documentation
* [Architecture Guidelines](docs/architecture.md)
* [Use Cases](docs/use-cases.md)
* [Architecture Decision Records (ADRs)](docs/adrs)

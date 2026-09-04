# Organisation App
## Project Scope
The goal of this project is a multi-purpose organisation app written in python,
which should be modular and easily extendable and scalable.

## Main Features
* **Recipe Management:** Create, modify and delete recipes (compare UC-1.1); search and filter recipes (compare UC-1.2)
* **Meal Planning:** Create, modify and delete menus (compare UC-2.1); search and filter menus (compare UC-2.2)
* **Inventory Management:** Create, modify and delete inventory items (compare UC-3.1); search inventory (compare UC-3.2); generate shopping list (UC-3.3); export shopping list to a Markdown file (.md, compare UC-3.4)

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

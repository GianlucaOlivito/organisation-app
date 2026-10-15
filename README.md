# Organisation App
## Project Scope
The goal of this project is a multi-purpose organisation app written in python,
which should be modular, easily extendable and scalable.

## Application Information
* **Title:** Savoria
* **Logo:** Stored in [App Logo](assets/logo.ico)

## Main Features
* **Recipe Management:** Create, modify and delete recipes (compare UC-1.1); search and filter recipes (compare UC-1.2)
* **Meal Planning:** Create, modify and delete menus (compare UC-2.1); search and filter menus (compare UC-2.2)
* **Inventory Management:** Create, modify and delete inventory items (compare UC-3.1); search inventory (compare UC-3.2); generate shopping list and reconcile inventory based on consumed meals and applied shopping list (UC-3.3); export shopping list to a Markdown file (.md, compare UC-3.4)

## User Interface
**Flet** is used as the Python desktop framework for the application's graphical interface. All use cases defined in [Use Cases](docs/use-cases.md) are accessible through this GUI.

## Quickstart
### Prerequisites
* [uv](https://docs.astral.sh/uv/) (python project management tool)

### Installation & Execution
```bash
# Install dependencies
uv sync

# Run the application as a developer
uv run main.py

# Run the application as a user
# Unzip folder "savoria-X.Y.Z", enter unzipped folder and 
# double click Savoria.exe to launch the app.
```

### UV Poethepoet Task Runner for Workflow Automation
```bash
uv run poe qa
# Task 'qa':
ruff check --fix
ruff format
pytest

uv run poe git-ship -m "<type>(<scope>): <description>"
# Task 'git-ship':
git add .
git commit -m "$msg" # consumes defined commit message as an argument
git push -u origin HEAD

uv run poe git-sync
# Task 'git-sync':
git checkout main
git pull --prune
git branch --merged main | Select-String -NotMatch 'main' | ForEach-Object { git branch -d $_.ToString().Trim() }

uv run poe build-exe
# Task 'build-exe':
flet pack main.py --name Savoria --icon assets/logo.ico
'''powershell -Command "Copy-Item -Recurse -Force assets dist/assets"'''
```

## Further Documentation
* [Architecture Decision Records (ADRs)](docs/adrs)
* [Release Management](docs/release/release-management.md)
* [Release Notes](docs/release/release-notes.md)
* [Architecture Guidelines](docs/architecture.md)
* [C4 Architecture Snapshot](docs/C4-architecture-snapshot.md)
* [Software Design](docs/design.md)
* [Domain Data Models](docs/domain.md)
* [Testing](docs/testing.md)
* [User Interface](docs/ui.md)
* [Use Cases](docs/use-cases.md)
* [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md)

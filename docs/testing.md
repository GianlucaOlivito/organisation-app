# Testing

## Testing Strategy
For automated testing, the following uv pytest dependencies are used:

- pytest, version>=9.1.1
- pytest-asyncio, version>=1.4.0

Pytest tests are written respecting the following guidelines:

- Reusable pytest fixtures are defined in modules in [Fixtures](../tests/fixtures/)
- Those fixture modules are gathered in [Conftest](../tests/conftest.py) via pytest_plugins
- Fakes are preferred over mocks. They are defined in [Fakes](../tests/fakes/) and distributed via [Fakes Fixtures](../tests/fixtures/fakes.py)

Tests are divided into the following categories:

- Unit tests in [Unit Tests](../tests/unit)
- Integration tests in [Integration Tests](../tests/integration)
- System tests in [System Tests](../tests/system)

All available tests are run with the following command as the last step of the local Poe QA task:

uv run poe qa (compare with [README](../README.md))

## Manual Smoke Test
The following manual smoke test is intended as a "sanity check". It must not be performed before every single PR, but it is recommended to perform it, if the content of a PR might have an influence on the behaviour of the application during runtime.
Performing this manual smoke test must be documented in the PR description.

Note: This is a general happy path smoke test of the application. Specific new features should also be verified via manual testing on the real application before committing the issue, where they are implemented. But it's not necessary to repeat these tests in every later issue.

In the following section, PreCondition, MainCondition and PostCondition of the manual smoke test are described:

### PreCondition: Has to be done, before the smoke test is started.
- Run local Poe QA task without errors or warnings: uv run poe qa

### MainCondition: This is the actual smoke test.
- Run application: uv run main.py => App window must open without runtime or terminal errors or warnings.
- Add a simple, valid recipe (with ingredients that are not in stock) on recipes view. => Verify, that it is saved without error, is displayed and logged correctly and persists in [Recipes](../data/recipes.json)
- Add a valid menu containing that recipe as a course with 2 portions. => Verify, that it is saved without error, is displayed and logged correctly and persists in [Menus](../data/menus.json)
- Generate a shopping list for the date of the created menu. => Verify, that it is saved without error, is displayed and logged correctly.
- Export that shopping list. => Verify, that the export is output correctly in [Export](../exports/shopping_list.md) and logged correctly.
- Apply that shopping list. => Verify, that the in-memory shopping list is cleared, the display changes to the empty state view, the event is logged correctly and the inventory is reconciled correctly on inventory view and in [Inventory](../data/inventory.json)
- Consume the meal of the date of the created menu. => Verify, that the event is logged correctly and the inventory is reconciled correctly on inventory view and in [Inventory](../data/inventory.json)
- Clean up all remaining smoke test artifacts: delete test recipe, menu, "empty" inventory item objects on inventory view and content of the exported test shopping list in [Export](../exports/shopping_list.md).
=> Verify that everything is logged correctly and deleted correctly, both in UI and in file system.

### PostCondition: This ends the smoke test.
- Close app, kill terminal and delete created log file.

# 007 Application Packaging and Distribution

* **Status:** Accepted
* **Date:** 2026-10-15

## Context and Problem Statement
A fitting way to pack / build release versions of the application into executables and distribute them, had to be found.

## Decision Outcome
1. Use Flet's built-in **`flet pack`** utility (which leverages PyInstaller under the hood) to bundle the Python interpreter, dependencies, source code, and assets into a standalone executable.
2. Configure a dedicated Poe task `build-exe` in `pyproject.toml` to automate the build command.
3. Update `settings.ROOT_DIR` to support runtime path resolution when frozen (`sys.frozen`), ensuring `data/`, `logs/`, `exports/`, and `assets/` resolve correctly relative to the executable binary.
4. Synchronize the application version dynamically from package metadata (`pyproject.toml`) via `importlib.metadata` into `Settings.app_version`.

## Reasoning
* This seems to be a simple and pragmatic solution.

## Consequences
* **Positive:**
  * Users can launch Savoria natively as a standalone desktop app (`Savoria.exe`). Version numbers are single-sourced, and file paths adapt dynamically between development and production environments.
* **Negative:**
  * Build artifacts must be generated locally or via release pipelines and packaged binaries are platform-specific.

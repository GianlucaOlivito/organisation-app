# 001 Use `uv` for Python Project and Package Management

* **Status:** Accepted
* **Date:** 2026-08-24

## Context and Problem Statement
Python projects traditionally rely on tools like `pip`, `venv`, `poetry`, or `pipenv` for environment management and package resolution. We need a fast, deterministic tool to manage dependencies, lockfiles, and virtual environments with minimal setup overhead.

## Decision Outcome
Chosen option: **`uv`**

## Reasoning
* Clean project encapsulation, no global installations are required: neither of python nor of any dependencies.
* Performance of package installation (written in Rust)
* User-friendly project setup and handling

## Consequences
* **Positive:**
  * Fast dependency resolution and package installation in local and CI environments.
  * Single source of truth for dependencies in `pyproject.toml` and reproducible builds via `uv.lock`.
  * Simplifies CI workflow (`uv sync`, `uv run pytest`).
* **Negative:**
  * Team members/contributors must install `uv` binary prior to development.

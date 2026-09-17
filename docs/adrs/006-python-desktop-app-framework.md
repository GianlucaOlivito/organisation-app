# 006 Python Desktop App Framework

* **Status:** Accepted
* **Date:** 2026-09-17

## Context and Problem Statement
A fitting framework for a python desktop app realizing this project had to be decided.
The following candidates have been considered: Flet, PySide6 (Qt) and CustomTkinter.

## Decision Outcome
It was decided to use Flet as a framework for the python desktop app.

## Reasoning
* Flet was determined to be the most aesthetically appealing and compatible with the project:
It is pure python using flutter under the hood, but there are no HTML, CSS or other format / language dependencies.

## Consequences
* **Positive:**
  * Aesthetically appealing: Modern Material 3 look out-of-the-box; fluid cards, chips, and themes.
  * Supports use cases well with native date range pickers.
  * Fitting for a clean separation in the hexagonal architecture: outer UI adapter consumes container services.
  * Learning curve: gentle declarative widget structure, but pure python.
* **Negative:**
  * Not as industry-standard as PySide6 (Qt).

# 004 Shopping List Export Format

* **Status:** Accepted
* **Date:** 2026-09-04

## Context and Problem Statement
A first supported export format for ShoppingList objects had to be decided.

## Decision Outcome
It was decided to support Markdown (.md) files as first export format for shopping lists.

## Reasoning
* Markdown is a structured text format which does well in displaying human-readable,
checklist-like shopping lists with interactive checkboxes (digitally and on paper).

## Consequences
* **Positive:**
  * Pragmatic, simple, human-readable and interactive solution.
* **Negative:**
  * Less serializable and generally less convenient to process in code than other 
  structured formats such as .json or .csv.

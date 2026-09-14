# 005 Repositories Persistence Format

* **Status:** Accepted
* **Date:** 2026-09-13

## Context and Problem Statement
A first supported format for the persistence of the 3 subdomain repositories had to be decided.

## Decision Outcome
It was decided to support JSON (.json) files as first repositories persistence format.

## Reasoning
* JSON is a structured format which is convenient for processing the data bidirectionally in Python.

## Consequences
* **Positive:**
  * Convenient, bidirectional data processing (read from and write to repository)
* **Negative:**
  * Less human-readable than other structured formats such as .md. To export a whole repository or single objects out of it, later an other use case would have to be defined.

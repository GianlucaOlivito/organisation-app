# Use Cases
This document describes the high-level functional use cases supported by the core application logic.

## 1. Appointment Management
* **UC-1.1: Create Appointment / Reminder**
  * **Actor:** User
  * **Goal:** Create a scheduled event or reminder with a title, date/time and description.
* **UC-1.2: Sync with Calendar**
  * **Actor:** User / System
  * **Goal:** Export or synchronize created appointments with an external calendar service (e.g. iCal or Google Calendar).

## 2. Recipe Management
* **UC-2.1: Create & Store Recipe**
  * **Actor:** User
  * **Goal:** Store a recipe consisting of id, title, ingredients (quantities + units) and a description (preparation steps).
* **UC-2.2: Browse & Search Recipes**
  * **Actor:** User
  * **Goal:** Filter stored recipes by name, ingredient or tags.

## 3. Meal Planning
* **UC-3.1: Create Meal Plan**
  * **Actor:** User
  * **Goal:** Define a target time range (e.g. weekly schedule) and assign recipes to specific meals per day (possible for breakfast, lunch and dinner).

## 4. Shopping List Generation
* **UC-4.1: Account for Food Stock**
  * **Actor:** User / System
  * **Goal:** Deduct available inventory items from the required ingredients to produce a final missing-items list.
* **UC-4.2: Generate Shopping List**
  * **Actor:** User
  * **Goal:** Calculate total required ingredients for a selected meal plan.
* **UC-4.3: Export Shopping List**
  * **Actor:** User
  * **Goal:** Export a generated shopping list in a supported format.

# Use Cases
This document describes the high-level functional use cases supported by the core application logic.

## 1. Recipe Management
* **UC-1.1: Create, Modify and Delete Recipe**
  * **Actor:** User
  * **Goal:** Perform the following operations on a recipe consisting of ID, title, ingredients (quantities + units) and instructions (preparation steps): create, modify (+ save!) and delete.
* **UC-1.2: Search and Filter Recipes**
  * **Actor:** User
  * **Goal:** Perform the following operations on stored recipes: search all, by ID and by name and filter by ingredients.

## 2. Meal Planning
* **UC-2.1: Create, Modify and Delete Menus**
  * **Actor:** User
  * **Goal:** Perform the following operations on a menu consisting of ID, description (usually meal type like lunch or dinner), scheduled date and courses (recipe ID + portions): create, modify (+ save!) and delete.
* **UC-2.2: Search and Filter Menus**
  * **Actor:** User
  * **Goal:** Perform the following operations on stored menus: search all and by ID and filter by date range.
  Note: The result of filtering by date range can be used in subdomain inventory to help calculating the content of a shopping list.

## 3. Shopping List Generation
* **UC-3.1: Account for Food Stock**
  * **Actor:** User / System
  * **Goal:** Deduct available inventory items from the required ingredients to produce a final missing-items list.
* **UC-3.2: Generate Shopping List**
  * **Actor:** User
  * **Goal:** Calculate total required ingredients for a selected meal plan.
* **UC-3.3: Export Shopping List**
  * **Actor:** User
  * **Goal:** Export a generated shopping list in a supported format.

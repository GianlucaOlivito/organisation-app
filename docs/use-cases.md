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

## 3. Inventory Management
* **UC-3.1: Create, Modify and Delete Inventory Item**
  * **Actor:** User / System
  * **Goal:** Perform the following operations on an inventory item consisting of ID, name, quantity and unit: create, modify (+ save!) and delete.
  Note: System updates stock automatically, if a quantity changes.
* **UC-3.2: Search Inventory**
  * **Actor:** User
  * **Goal:** Perform the following operations on stored inventory items: search all, by ID and by name.
* **UC-3.3: Generate Shopping List**
  * **Actor:** User / System
  * **Goal:** Generate a shopping list consisting of ID and a list of shopping list items (consisting of name, quantity and unit) for a selected date range.
  Note: The System filters the MenuRepository by that date range to determine the needed quantities and searches the InventoryRepository for needed items to determine the already available quantities.
* **UC-3.4: Export Shopping List**
  * **Actor:** User / System
  * **Goal:** Format a generated shopping list and export it to a Markdown file (.md).

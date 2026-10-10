# User Interface

## 1. App Layout
This application is structured as a desktop app built using **Flet** (Python framework wrapping Flutter). 

### Layout Architecture
- **Window Shell**: A resizable desktop window managed by Flet's application runtime (`ft.run()`).
- **Main Layout**:
  - **Sidebar**: Persistent vertical navigation component on the left side to switch between views
  - **Main Content Area**: Dynamic viewport that renders the active view's content based on user input.

## 2. Navigation Guide
Users navigate the app via the left sidebar navigation rail. The application is divided into the following core functional views:

1. **Recipes**: Accesses recipes subdomain services.
2. **Menus**: Accesses meal planning subdomain services.
3. **Inventory**: Accesses inventory related inventory subdomain services.
4. **Shopping List**: Accesses shopping list related inventory subdomain services.
5. **Logs**: Logs application events in real time.

## 3. View Specifications
### 3.1 Recipes View
- **Purpose**: Perform CRUD-Operations on recipes, search and filter recipes (UC-1.1 & UC-1.2).
- **Key Components**:
  - Header bar displaying view title.
  - Top horizontal toolbar with a button to create a recipe and input fields and buttons to search or filter the recipes repository.
  - Grid of RecipeCards displaying the searched / filtered recipes.
  - RecipeForm providing a second view with input fields for recipe attributes.

### 3.2 Menus View
- **Purpose**: Perform CRUD-Operations on menus, search and filter menus (UC-2.1 & UC-2.2).
- **Key Components**:
  - Header bar displaying view title.
  - Top horizontal toolbar with a button to create a menu and input fields and buttons to search or filter the menus repository.
  - Grid of MenuCards displaying the searched / filtered menus.
  - MenuForm providing a second view with input fields for menu attributes.

### 3.3 Inventory View
- **Purpose**: Perform CRUD-Operations on inventory items, search and filter inventory (UC-3.1 & UC-3.2).
- **Key Components**:
  - Header bar displaying view title.
  - Top horizontal toolbar with a button to create an inventory (if empty) and an input field and button to search the inventory repository.
  - A single expanding InventoryCard displaying the searched inventory items.
  - InventoryForm providing a second view with input fields for inventory item attributes.

### 3.4 Shopping List View
- **Purpose**: Generate, export and apply a single in-memory shopping list, reconcile inventory after applying a shopping list or consuming meals (UC-3.3 & UC-3.4).
- **Key Components**:
  - Header bar displaying view title.
  - Top horizontal toolbar with a buttons to generate a shopping list and consume meals over a date range defined via input fields.
  - A single expanding ShoppingListCard displaying a generated in-memory shopping list.
  - ShoppingListCard contains buttons to apply, export and dismiss the underlying in-memory shopping list.

### 3.5 Logs View
- **Purpose**: Provide real-time logging for observability and debugging (no UC, just app infrastructure).
- **Key Components**:
  - Log text container subscribing to `LogBuffer` automatically updating incoming logs in real-time.
  - Top horizontal toolbar with a segmented button to filter displayed logs via log level and button to clear the in-memory log buffer.

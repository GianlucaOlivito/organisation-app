# Domain Data Models

## 1. Subdomain Recipes
### 1.1 RecipeIngredient
Ingredient reference within a Recipe:
- `name`: str
- `quantity`: float | str
- `unit`: str (no unit is represented by an empty string)

#### Validation
- `Name` must not be an empty string.
- `Quantity` must be converted into a valid float > 0.

### 1.2 Recipe
- `id`: UUID (default: uuid4)
- `name`: str
- `ingredients`: list[RecipeIngredient]
- `instructions`: str

#### Validation
- `Name` must not be an empty string.
- `Ingredients` must not be an empty list.
- `Instructions` must not be an empty string.

### 1.3 Example JSON Persistence
List of recipes in [Recipes](../data/recipes.json)
```json
[
    {
        "id": "11111111-1111-1111-1111-111111111111",
        "name": "Tomatensuppe",
        "ingredients": [
            {
                "name": "Tomaten",
                "quantity": 500.0,
                "unit": "g"
            },
            {
                "name": "Salz",
                "quantity": 2.0,
                "unit": "Prise"
            },
            {
                "name": "Pfeffer",
                "quantity": 1.0,
                "unit": "Prise"
            },
            {
                "name": "Wasser",
                "quantity": 1.0,
                "unit": "l"
            },
        ],
        "instructions": "Mix and boil."
    }
]
```

## 2. Subdomain Meal Planning
### 2.1 Course
Recipe reference within a Menu:
- `recipe_id`: UUID | str
- `portions`: int | str (default: 1)

#### Validation
- `Recipe_id` must be converted into a valid UUID.
- `Portions` must be converted into a valid integer > 0

### 2.2 Menu
- `id`: UUID (default: uuid4)
- `description`: str
- `scheduled_date`: date | str
- `courses`: list[Course] (default: empty list)

#### Validation
- `Description` must not be an empty string.
- `Scheduled_date` must be converted into a valid `date` object.
- `Courses` must not be an empty list.

### 2.3 Example JSON Persistence
List of menus in [Menus](../data/menus.json)
```json
[
  {
    "id": "22222222-2222-2222-2222-222222222222",
    "description": "Mittagessen",
    "scheduled_date": "2026-10-10",
    "courses": [
      {
        "recipe_id": "11111111-1111-1111-1111-111111111111",
        "portions": 4
      }
    ]
  }
]
```

## 3. Subdomain Inventory
### 3.1 InventoryItem
Represents a tracked supply item in stock:
- `id`: UUID (default: uuid4)
- `name`: str
- `quantity`: float | str
- `unit`: str (no unit is represented by an empty string)

#### Validation
- `Name` must not be an empty string.
- `Quantity` must be converted into a valid float >= 0.

### 3.2 ShoppingListItem
Represents an item in a ShoppingList:
- `name`: str
- `quantity`: float | str
- `unit`: str (no unit is represented by an empty string)

#### Validation
- `Name` must not be an empty string.
- `Quantity` must be converted into a valid float > 0.

### 3.3 ShoppingList
Represents a shopping list with a unique ID and a list of items:
- `id`: UUID (default: uuid4)
- `items`: list[ShoppingListItem] (default: empty list)

#### Validation
- `Items` must not be an empty list.

### 3.4 Example JSON Inventory Persistence
List of inventory items in [Inventory](../data/inventory.json)
```json
[
  {
    "id": "33333333-3333-3333-3333-333333333333",
    "name": "Tomaten",
    "quantity": 1000.0,
    "unit": "g"
  },
  {
    "id": "44444444-4444-4444-4444-444444444444",
    "name": "Salz",
    "quantity": 500.0,
    "unit": "g"
  }
]
```

### 3.5 Example Markdown ShoppingList Export
Shopping list with header and formatted list in [Shopping List](../exports/shopping_list.md)
# Einkaufsliste

| Erledigt | Menge | Einheit | Artikel |
| :---: | :---: | :---: | :--- |
| [ ] | 1000.0 | g | Tomaten |
| [ ] | 500.0 | g | Brot |
| [ ] | 500.0 | ml | Milch |

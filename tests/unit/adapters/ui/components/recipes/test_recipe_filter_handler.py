def test_filter_returns_all_when_queries_are_empty(
    recipe_filter_handler, sample_recipes
):
    results = recipe_filter_handler.filter(query="", ing_query="")

    assert len(results) == 2
    assert results == sample_recipes


def test_filter_by_recipe_name(recipe_filter_handler):
    results = recipe_filter_handler.filter(query="Spaghetti Carbonara")

    assert len(results) == 1
    assert results[0].name == "Spaghetti Carbonara"


def test_filter_by_recipe_id(recipe_filter_handler, sample_recipes):
    target_recipe = sample_recipes[0]
    results = recipe_filter_handler.filter(query=str(target_recipe.id))

    assert len(results) == 1
    assert results[0].id == target_recipe.id


def test_filter_by_ingredients_repository_search(recipe_filter_handler):
    results = recipe_filter_handler.filter(ing_query="Tomato")

    assert len(results) == 1
    assert results[0].name == "Tomato Soup"


def test_filter_by_query_and_ingredients_in_memory(recipe_filter_handler):
    matching = recipe_filter_handler.filter(
        query="Spaghetti Carbonara", ing_query="Pasta, Eggs"
    )

    assert len(matching) == 1
    assert matching[0].name == "Spaghetti Carbonara"

    mismatch = recipe_filter_handler.filter(
        query="Spaghetti Carbonara", ing_query="Tomato"
    )

    assert len(mismatch) == 0


def test_filter_invalid_uuid_falls_back_to_name_search(recipe_filter_handler):
    results = recipe_filter_handler.filter(query="non-existent-recipe")

    assert len(results) == 0

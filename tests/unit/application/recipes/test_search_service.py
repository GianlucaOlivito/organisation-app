from uuid import uuid4


def test_get_all_returns_empty_list_when_no_recipes(recipes_search_service):
    assert recipes_search_service.get_all() == []


def test_get_all_returns_all_recipes(recipes_search_service, sample_recipes):
    results = recipes_search_service.get_all()
    assert len(results) == 2
    assert results == sample_recipes


def test_get_by_id_returns_recipe_when_found(recipes_search_service, sample_recipes):
    expected_recipe = sample_recipes[0]
    found_recipe = recipes_search_service.get_by_id(expected_recipe.id)
    assert found_recipe == expected_recipe


def test_get_by_id_returns_none_when_not_found(recipes_search_service):
    assert recipes_search_service.get_by_id(uuid4()) is None


def test_get_by_name_returns_recipe_when_found(recipes_search_service, sample_recipes):
    expected_recipe = sample_recipes[0]
    found_recipe = recipes_search_service.get_by_name("Spaghetti Carbonara")
    assert found_recipe == expected_recipe


def test_get_by_name_returns_none_when_not_found(recipes_search_service):
    assert recipes_search_service.get_by_name("Nonexistent Recipe") is None


def test_filter_by_ingredients_returns_matching_recipes(
    recipes_search_service, sample_recipes
):
    results = recipes_search_service.filter_by_ingredients(["Pasta", "Eggs"])
    assert len(results) == 1
    assert results[0] == sample_recipes[0]


def test_filter_by_ingredients_returns_empty_list_when_no_match(recipes_search_service):
    results = recipes_search_service.filter_by_ingredients(["Chocolate"])
    assert results == []

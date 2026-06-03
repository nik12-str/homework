#Тесты 1

from main import Ingredient, Recipe, ShoppingList
import pytest

@pytest.fixture
def sample_ingredient():
    ingredient = Ingredient('Творог', 200, 'гр')
    return ingredient

def test_ingredient_name(sample_ingredient):
    assert sample_ingredient.name == 'Творог'

def test_ingredient_quantity(sample_ingredient):
    assert sample_ingredient.quantity == float(200)

def test_ingredient_unit(sample_ingredient):
    assert sample_ingredient.unit == 'гр'

def test_method_str(sample_ingredient):
    assert str(sample_ingredient) == 'Творог: 200.0 гр'

def test_method_eq_different_quantity(sample_ingredient):
    help_ingredient = Ingredient('Творог', 500, 'гр')
    assert sample_ingredient == help_ingredient

def test_method_eq_different_name(sample_ingredient):
    help_ingredient = Ingredient('Мука', 200, 'гр')
    assert sample_ingredient != help_ingredient

def test_method_eq_different_unit(sample_ingredient):
    help_ingredient = Ingredient('Творог', 200, 'кг')
    assert sample_ingredient != help_ingredient

def test_ingredient_negative_quantity():
    with pytest.raises(ValueError):
        Ingredient('Мука', -100, 'г')

#Тесты 2

@pytest.fixture
def sample_recipe():
    first_ingredient = Ingredient('Творог', 200, 'гр')
    second_ingredient = Ingredient('Сметана', 100, 'гр')
    third_ingredient = Ingredient('Сгущёнка', 50, 'гр')
    ingredients = [first_ingredient, second_ingredient, third_ingredient]
    return Recipe('Счастье мужика', ingredients)

def test_recipe_name(sample_recipe):
    assert sample_recipe.title == 'Счастье мужика'

def test_recipe_ingredients(sample_recipe):
    first_ingredient = Ingredient('Творог', 200, 'гр')
    second_ingredient = Ingredient('Сметана', 100, 'гр')
    third_ingredient = Ingredient('Сгущёнка', 50, 'гр')

    ingredients = [first_ingredient, second_ingredient, third_ingredient]

    assert sample_recipe.ingredients == ingredients

def test_method_add_new_ingredient(sample_recipe):
    help_ingredient = Ingredient('Клубника', 250, 'гр')
    length = len(sample_recipe.ingredients)

    sample_recipe.add_ingredient(help_ingredient)

    assert len(sample_recipe.ingredients) == length + 1


def test_method_add_old_ingredient_dublicate(sample_recipe):
    help_ingredient = Ingredient('Творог', 500, 'гр')
    length = len(sample_recipe.ingredients)

    sample_recipe.add_ingredient(help_ingredient)

    assert len(sample_recipe.ingredients) == length

def test_method_add_old_ingredient_sum(sample_recipe):
    help_ingredient = Ingredient('Творог', 500, 'гр')

    ing = None
    for ingredient in sample_recipe.ingredients:
        if ingredient.name == help_ingredient.name:
            ing = ingredient
    old_quantity = ing.quantity
    sample_recipe.add_ingredient(help_ingredient)
    new_quantity = ing.quantity

    assert new_quantity == old_quantity + help_ingredient.quantity

def test_method_scale_new_object(sample_recipe):
    old_recipe = sample_recipe

    new_recipe = sample_recipe.scale(2)

    assert old_recipe is not new_recipe

def test_method_scale_positive_ratio(sample_recipe):
    old_values = []
    for ing in sample_recipe.ingredients:
        old_values.append(ing.quantity)

    new_recipe = sample_recipe.scale(2)

    new_values = []
    for ing in new_recipe.ingredients:
        new_values.append(ing.quantity)

    flag = True
    for i in range(len(old_values)):
        if new_values[i] != old_values[i] * 2:
            flag = False

    assert flag

def test_method_scale_negative_ratio(sample_recipe):
    with pytest.raises(ValueError):
        sample_recipe.scale(-2)

def test_method_len(sample_recipe):
    assert len(sample_recipe) == len(sample_recipe.ingredients)

#Тесты 3

@pytest.fixture
def sample_shopping_list():
    return ShoppingList()

def test_method_add_recipe_correct_portions(sample_recipe, sample_shopping_list):
    sample_shopping_list.add_recipe(sample_recipe, 2)
    scaled_ings = sample_recipe.scale(2).ingredients
    items = sample_shopping_list._items
    negative_flag = False
    for ing in scaled_ings:
        found = False
        for item_ing, title in items:
            if item_ing.name == ing.name and item_ing.quantity == ing.quantity and item_ing.unit == ing.unit and title == sample_recipe.title:
                found = True
                break
        if not found:
            negative_flag = True
            break
    assert not negative_flag

def test_method_add_recipe_uncorrect_negative_portions(sample_recipe, sample_shopping_list):
    with pytest.raises(ValueError):
        sample_shopping_list.add_recipe(sample_recipe, -1)

def test_method_add_recipe_uncorrect_zero_portions(sample_recipe, sample_shopping_list):
    with pytest.raises(ValueError):
        sample_shopping_list.add_recipe(sample_recipe, 0)

def test_method_remove_recipe_existing(sample_recipe, sample_shopping_list):
    sample_shopping_list.add_recipe(sample_recipe, 1)
    sample_shopping_list.remove_recipe('Счастье мужика')
    assert len(sample_shopping_list._items) == 0

def test_method_remove_recipe_not_existing(sample_recipe, sample_shopping_list):
    sample_shopping_list.add_recipe(sample_recipe, 1)
    original_len = len(sample_shopping_list._items)
    sample_shopping_list.remove_recipe('Несуществующий рецепт')
    assert len(sample_shopping_list._items) == original_len

def test_get_list_sums_identical_ingredients():
    recipe1 = Recipe('Блины', [Ingredient('Мука', 500, 'г'), Ingredient('Яйца', 2, 'шт')])
    recipe2 = Recipe('Оладьи', [Ingredient('Мука', 300, 'г'), Ingredient('Яйца', 1, 'шт')])
    sl = ShoppingList()
    sl.add_recipe(recipe1, 1)
    sl.add_recipe(recipe2, 1)
    result = sl.get_list()
    found_flour = False
    found_eggs = False
    for ing in result:
        if ing.name == 'Мука':
            assert ing.quantity == 800
            assert ing.unit == 'г'
            found_flour = True
        elif ing.name == 'Яйца':
            assert ing.quantity == 3
            assert ing.unit == 'шт'
            found_eggs = True
    assert found_flour and found_eggs

def test_get_list_sorted(sample_recipe, sample_shopping_list):
    sample_shopping_list.add_recipe(sample_recipe, 1)
    result = sample_shopping_list.get_list()
    names = []
    for ing in result:
        names.append(ing.name)
    sorted_names = sorted(names)
    negative_flag = False
    for i in range(len(names)):
        if names[i] != sorted_names[i]:
            negative_flag = True
            break
    assert not negative_flag

def test_add_two_shopping_lists(sample_recipe):
    s1 = ShoppingList()
    s1.add_recipe(sample_recipe, 1)
    s2 = ShoppingList()
    recipe2 = Recipe('Кофе', [Ingredient('Кофе', 20, 'г')])
    s2.add_recipe(recipe2, 1)
    s3 = s1 + s2
    total_items = len(s1._items) + len(s2._items)
    assert len(s3._items) == total_items
    assert len(s1._items) == len(sample_recipe.ingredients)
    assert len(s2._items) == 1

def test_add_invalid_type(sample_shopping_list):
    with pytest.raises(TypeError):
        sample_shopping_list + 'abab'

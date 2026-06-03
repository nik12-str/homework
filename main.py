class Ingredient:

    def __init__(self, name, quantity, unit):
        self.name = str(name)
        self.unit = str(unit)
        self.quantity = float(quantity)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError('Количество должно быть положительным')
        self._quantity = float(value)

    def __str__(self):
        return f'{self.name}: {self.quantity} {self.unit}'

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if isinstance(other, Ingredient):
            if self.name == other.name and self.unit == other.unit:
                return True
            else:
                return False
        else:
            return False

class Recipe:

    def __init__(self, title, ingredients):
        self.title = str(title)
        self.ingredients = list(ingredients)

    def add_ingredient(self, ingredient):
        if isinstance(ingredient, Ingredient):
            for ing in self.ingredients:
                if ingredient == ing:
                    ing.quantity = ing.quantity + ingredient.quantity
                    break
            else:
                self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        if (isinstance(ratio, int) or isinstance(ratio, float)) and ratio > 0:
            return True
        else:
            return False

    def scale(self, ratio):
        if self.is_valid_ratio(ratio):
            ingredients = []
            for ing in self.ingredients:
                new_ing = Ingredient(ing.name, ing.quantity * ratio, ing.unit)
                ingredients.append(new_ing)
            return Recipe(self.title, ingredients)
        else:
            raise ValueError('ratio не является числом или не больше нуля')

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        ingredients = []
        for ing in self.ingredients:
            ingredients.append(str(ing))
        return f"Название блюда: {self.title}, список ингредиентов: {', '.join(ingredients)}"

class ShoppingList:

    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError('Количество порций должно быть положительным')
        for ing in recipe.scale(portions).ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title):
        new_items = []
        for ing, name in self._items:
            if name != title:
                new_items.append((ing, name))
        self._items = new_items[:]

    def get_list(self):
        lst = dict()
        for ing, name in self._items:
            if lst.get((ing.name, ing.unit), None) is None:
                lst[(ing.name, ing.unit)] = ing.quantity
            else:
                lst[(ing.name, ing.unit)] += ing.quantity

        ingredients = []
        for (name, unit), quantity in lst.items():
            ingredients.append(Ingredient(name, quantity, unit))

        return sorted(ingredients, key = lambda x: x.name)

    def __add__(self, other):
        if isinstance(other, ShoppingList):
            new_shopping_list = ShoppingList()
            new_shopping_list._items = self._items + other._items
            return new_shopping_list
        else:
            raise TypeError

class DietaryRecipe(Recipe):

    def __init__(self, title, diet_type, ingredients = None):
        super().__init__(title, ingredients if ingredients else [])
        self.diet_type = diet_type

    def scale(self, ratio):
        recipe = super().scale(ratio)
        return DietaryRecipe(recipe.title, self.diet_type, recipe.ingredients)

    def __str__(self):
        return f'[{self.diet_type}] {super().__str__()}'

import os
import yaml
from dataclasses import dataclass
from .products import Product

@dataclass
class Meal:
    name: str
    products: list[tuple[Product, int]]
    calories: float = 0
    proteins: float = 0
    fats: float = 0
    carbohydrates: float = 0
    weight: float = 0

    def __post_init__(self):
        for product, quantity in self.products:
            self.calories += product.calories * quantity / 100
            self.proteins += product.proteins * quantity / 100
            self.fats += product.fats * quantity / 100
            self.carbohydrates += product.carbohydrates * quantity / 100
            self.weight += product.packageWeight * quantity / 1000

def load_meals(filename: str, products: dict[str, Product]) -> dict[str, Meal]:
    with open(filename) as f:
        meals_data = yaml.safe_load(f)["meals"]
    
    meals = {}
    for meal_name, meal_data in meals_data.items():
        meal_products = []
        for product_name, quantity in meal_data.items():
            if product_name in products:
                meal_products.append((products[product_name], quantity))
            else:
                raise ValueError(f"Invalid product: {product_name}")
        meals[meal_name] = Meal(meal_name, meal_products)
    return meals

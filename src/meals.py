"""
meals.py

This module defines the Meal class and utility functions to load meal data from YAML files.
It ensures the integrity and validity of meal information used in meal planning applications.

Classes:
    Meal: A dataclass representing a meal consisting of various products.

Functions:
    load_meals(filename: str, products: Dict[str, Product]) -> Dict[str, Meal]:
        Loads meals from a YAML file and returns a dictionary of Meal instances.

    load_everyday(filename: str, products: Dict[str, Product]) -> Meal:
        Loads the everyday meal from a YAML file and returns a Meal instance.
"""

import yaml
from dataclasses import dataclass
from typing import List, Tuple, Dict
import os

from .products import Product


@dataclass
class Meal:
    """
    Represents a meal consisting of various products.

    Attributes:
        name (str): The name of the meal.
        products (List[Tuple[Product, int]]): A list of tuples containing Product instances and their quantities in grams.
        calories (float): Total calories in the meal.
        proteins (float): Total proteins in the meal.
        fats (float): Total fats in the meal.
        carbohydrates (float): Total carbohydrates in the meal.
        weight (float): Total weight of the meal in grams.
    """
    name: str
    products: List[Tuple[Product, int]]
    calories: float = 0.0
    proteins: float = 0.0
    fats: float = 0.0
    carbohydrates: float = 0.0
    weight: float = 0.0

    def __post_init__(self):
        """
        Calculates the total nutritional values and weight of the meal based on its products.

        Raises:
            ValueError: If any product quantity is negative.
        """
        for product, quantity in self.products:
            if quantity < 0:
                raise ValueError(f"Quantity for product '{product.name}' in meal '{self.name}' cannot be negative.")
            self.calories += product.calories * quantity / 100
            self.proteins += product.proteins * quantity / 100
            self.fats += product.fats * quantity / 100
            self.carbohydrates += product.carbohydrates * quantity / 100
            self.weight += product.packageWeight * quantity / 1000  # Convert to kilograms


def load_meals(filename: str, products: Dict[str, Product]) -> Dict[str, Meal]:
    """
    Loads meals from a YAML file.

    The YAML file should have the following structure:

    ```yaml
    meals:
      meal_name_1:
        product_name_1: 150
        product_name_2: 200
        ...
      meal_name_2:
        ...
    ```

    Args:
        filename (str): Path to the meals YAML file.
        products (Dict[str, Product]): Dictionary of available products.

    Returns:
        Dict[str, Meal]: A dictionary mapping meal names to Meal instances.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the YAML file has invalid format or contains invalid products.
        TypeError: If any of the fields have incorrect types.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Meals file not found: {filename}")

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            meals_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {filename}: {e}")

    if not isinstance(meals_data, dict) or 'meals' not in meals_data:
        raise ValueError(f"Invalid meals file format: 'meals' key not found in {filename}")

    meals = {}
    for meal_name, meal_details in meals_data['meals'].items():
        if not isinstance(meal_details, dict):
            raise ValueError(f"Invalid meal details for '{meal_name}': expected a dictionary")

        meal_products = []
        for product_name, quantity in meal_details.items():
            if not isinstance(quantity, (int, float)):
                raise TypeError(f"Quantity for product '{product_name}' in meal '{meal_name}' must be a number")
            if product_name not in products:
                raise ValueError(f"Invalid product '{product_name}' in meal '{meal_name}'")
            meal_products.append((products[product_name], quantity))

        try:
            meal = Meal(name=meal_name, products=meal_products)
        except ValueError as e:
            raise ValueError(f"Error creating Meal '{meal_name}': {e}")

        if meal_name in meals:
            raise ValueError(f"Duplicate meal name detected: '{meal_name}'")

        meals[meal_name] = meal

    return meals


def load_everyday(filename: str, products: Dict[str, Product]) -> Meal:
    """
    Loads the everyday meal from a YAML file.

    The YAML file should have the following structure:

    ```yaml
    product_name_1: 100
    product_name_2: 50
    ...
    ```

    Args:
        filename (str): Path to the everyday meal YAML file.
        products (Dict[str, Product]): Dictionary of available products.

    Returns:
        Meal: An instance of Meal representing the everyday meal.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the YAML file has invalid format or contains invalid products.
        TypeError: If any of the fields have incorrect types.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Everyday meal file not found: {filename}")

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            everyday_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {filename}: {e}")

    if not isinstance(everyday_data, dict):
        raise ValueError(f"Invalid everyday meal file format: expected a dictionary in {filename}")

    meal_products = []
    for product_name, quantity in everyday_data.items():
        if not isinstance(quantity, (int, float)):
            raise TypeError(f"Quantity for product '{product_name}' in everyday meal must be a number")
        if product_name not in products:
            raise ValueError(f"Invalid product '{product_name}' in everyday meal")
        meal_products.append((products[product_name], quantity))

    try:
        everyday_meal = Meal(name='каждый день', products=meal_products)
    except ValueError as e:
        raise ValueError(f"Error creating everyday Meal: {e}")

    return everyday_meal

"""
menus.py

This module defines the Menu dataclass and utility functions to load menu configurations
from YAML files. It ensures the integrity and validity of menu plans used in meal planning
applications, including handling of people counts per menu and generation of Bill of Materials (BOM).
    
Classes:
    Menu: A dataclass representing a menu consisting of multiple days.
    
Functions:
    load_menus(filename: str, days: Dict[str, Day]) -> List[Menu]:
        Loads menu configurations from a YAML file and returns a list of Menu instances.
    
    get_bom_for_menus(menus: List[Menu]) -> Dict[str, float]:
        Generates a Bill of Materials (BOM) for all menus combined.
    
    calculate_total_weight(menus: List[Menu]) -> float:
        Calculates the total weight of all menus.
    
    group_products_by_category(bom: Dict[str, float], products: Dict[str, Product]) -> Dict[str, Dict[str, float]]:
        Groups products in the BOM by their categories.
    
    print_grouped_products(grouped_products: Dict[str, Dict[str, float]], indent: int = 0):
        Prints the grouped products in a readable YAML format.
"""

import yaml
from dataclasses import dataclass, replace
from typing import List, Dict
import os

from .day import Day
from .products import Product, productCategoryMap, productGroups



@dataclass
class Menu:
    """
    Represents a menu consisting of multiple days.

    Attributes:
        name (str): The name of the menu.
        days (List[Day]): A list of Day instances included in the menu.
        default_people_count (int): The default number of people for the menu.
        calories (float): Total calories for the menu.
        proteins (float): Total proteins for the menu in grams.
        fats (float): Total fats for the menu in grams.
        carbohydrates (float): Total carbohydrates for the menu in grams.
        weight_per_person (float): Total weight of the menu per person in kilograms.
        total_weight (float): Total weight of the menu for all people in kilograms.
    """
    name: str
    days: List[Day]
    default_people_count: int
    calories: float = 0.0
    proteins: float = 0.0
    fats: float = 0.0
    carbohydrates: float = 0.0
    weight_per_person: float = 0.0
    total_weight: float = 0.0

    def __post_init__(self):
        """
        Calculates the total nutritional values and weight of the menu based on its days.
        """
        for day in self.days:
            # Accumulate nutritional values
            self.calories += day.calories
            self.proteins += day.proteins
            self.fats += day.fats
            self.carbohydrates += day.carbohydrates
            self.weight_per_person += day.weight
            # Accumulate total weight based on the number of people for each day
            self.total_weight += day.weight * day.people_count


def load_menus(filename: str, days: Dict[str, Day]) -> List[Menu]:
    """
    Loads menu configurations from a YAML file and returns a list of Menu instances.

    The YAML file should have the following structure:

    ```yaml
    rules:
      daily_calories_min: 2500
      daily_calories_max: 3200
      daily_protein: 55
      daily_fat: 60
      daily_carbs: 290

    menus:
      Menu1:
        days:
          - Monday
          - Tuesday
          - Wednesday
        people_count: 4

      Menu2:
        days:
          - Monday: 5
          - Thursday: 3
        people_count: 2
    ```

    In the `days` list, each entry can be either a string representing the day name
    with the default people count, or a dictionary with the day name as the key and
    a specific people count as the value.

    Args:
        filename (str): Path to the YAML file containing menu configurations.
        days (Dict[str, Day]): Dictionary of available Day instances.

    Returns:
        List[Menu]: A list of Menu instances.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
        ValueError: If the YAML file has an invalid format or contains invalid day entries.
        TypeError: If any of the fields have incorrect types.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Menus file not found: {filename}")

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {filename}: {e}")

    if not isinstance(config, dict):
        raise ValueError(f"Invalid format: Expected a dictionary at the top level in {filename}.")

    if 'menus' not in config:
        raise ValueError(f"Invalid format: 'menus' key not found in {filename}.")

    menus = []
    for menu_name, menu_data in config['menus'].items():
        if not isinstance(menu_data, dict):
            raise ValueError(f"Invalid menu data for '{menu_name}': expected a dictionary.")

        # Get default_people_count with validation
        default_people_count = menu_data.get('people_count', 1)
        if not isinstance(default_people_count, int) or default_people_count < 1:
            raise ValueError(f"Invalid default_people_count '{default_people_count}' for menu '{menu_name}'. It must be a positive integer.")

        menu_days = []
        for day_entry in menu_data.get('days', []):
            if isinstance(day_entry, str):
                day_name = day_entry
                people_count = default_people_count
            elif isinstance(day_entry, dict):
                if len(day_entry) != 1:
                    raise ValueError(f"Invalid day entry format in menu '{menu_name}': {day_entry}")
                day_name, people_count = next(iter(day_entry.items()))
                if not isinstance(people_count, int) or people_count < 1:
                    raise ValueError(f"Invalid people_count for day '{day_name}' in menu '{menu_name}': {people_count}")
            else:
                raise ValueError(f"Invalid day entry type in menu '{menu_name}': {day_entry}")

            if day_name not in days:
                raise ValueError(f"Invalid day: '{day_name}' in menu '{menu_name}'")

            original_day = days[day_name]
            # Create a copy of the day with the specified people_count
            day_copy = replace(original_day, people_count=people_count)
            menu_days.append(day_copy)

        menu = Menu(name=menu_name, days=menu_days, default_people_count=default_people_count)
        menus.append(menu)

    return menus


def get_bom_for_menus(menus: List[Menu]) -> Dict[str, float]:
    """
    Generates a Bill of Materials (BOM) for all menus combined.

    The BOM is a dictionary mapping product names to the total quantity required across all menus.

    Args:
        menus (List[Menu]): A list of Menu instances.

    Returns:
        Dict[str, float]: A dictionary mapping product names to their total required quantities.
    """
    bom = {}
    for menu in menus:
        for day in menu.days:
            for meal in [day.breakfast, day.lunch, day.dinner, day.everyday]:
                for product, quantity in meal.products:
                    bom[product.name] = bom.get(product.name, 0) + quantity * day.people_count
    return bom


def calculate_total_weight(menus: List[Menu]) -> float:
    """
    Calculates the total weight of all menus combined.

    Args:
        menus (List[Menu]): A list of Menu instances.

    Returns:
        float: The total weight of all menus in kilograms.
    """
    total_weight = 0.0
    for menu in menus:
        total_weight += menu.total_weight
    return total_weight


def group_products_by_category(bom: Dict[str, float], products: Dict[str, Product]) -> Dict[str, Dict[str, float]]:
    """
    Groups products in the BOM by their categories.

    Args:
        bom (Dict[str, float]): A dictionary mapping product names to their total required quantities.
        products (Dict[str, Product]): A dictionary mapping product names to Product instances.

    Returns:
        Dict[str, Dict[str, float]]: A dictionary where each key is a product category and the value is another
                                      dictionary mapping product names to their quantities.
    """
    grouped_products = {}
    for product_name, quantity in bom.items():
        product = products.get(product_name)
        if not product:
            continue  # Skip products that are not found in the products dictionary
        category = productCategoryMap.get(product.group, "Другое")
        if category not in grouped_products:
            grouped_products[category] = {}
        grouped_products[category][product_name] = grouped_products[category].get(product_name, 0) + quantity
    return grouped_products


def print_grouped_products(grouped_products: Dict[str, Dict[str, float]], indent: int = 0):
    """
    Prints the grouped products in a readable YAML format with the specified indentation.

    Args:
        grouped_products (Dict[str, Dict[str, float]]): A dictionary where each key is a product category
                                                        and the value is another dictionary mapping product
                                                        names to their quantities.
        indent (int, optional): The indentation level for the printed output. Defaults to 0.
    """
    for pg in productGroups:
        print(f"{'  ' * indent}{pg}:")
        pr_d = grouped_products.get(pg, {})
        if pr_d:
            dump = yaml.dump(pr_d, default_flow_style=False, allow_unicode=True)
            lines = dump.splitlines()
            if indent > 0:
                lines = [f"{'  ' * indent}{line}" for line in lines]
            dump = '\n'.join(lines)
            print(dump)
        else:
            print("  Нет продуктов")

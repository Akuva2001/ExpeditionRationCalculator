"""
bom_generator.py

This module includes functions related to generating and managing the Bill of Materials (BOM)
for the meal planning application. It facilitates the calculation of total product quantities
required across menus and their categorization.
"""

from typing import Dict, List
from .menus import Menu
from .products import Product, productCategoryMap


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

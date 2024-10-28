"""
config.py

This module defines the MealPlannerConfig class, which encapsulates all configuration
data required for the meal planning application. It serves as a centralized container
for products, meals, days, daily norms, and menus.
"""

from dataclasses import dataclass
from typing import Dict, List
from .products import Product
from .meals import Meal
from .day import Day
from .menus import Menu
from .daily_norms import DailyNorms


@dataclass
class MealPlannerConfig:
    """
    Encapsulates all configuration data required for the meal planning application.

    Attributes:
        products (Dict[str, Product]): Dictionary of available products.
        meals (Dict[str, Meal]): Dictionary of available meals.
        everyday (Meal): The everyday meal (e.g., snacks).
        days (Dict[str, Day]): Dictionary of day configurations.
        daily_norms (DailyNorms): Daily nutritional norms.
        menus (List[Menu]): List of menu configurations.
    """
    products: Dict[str, Product]
    meals: Dict[str, Meal]
    everyday: Meal
    days: Dict[str, Day]
    daily_norms: DailyNorms
    menus: List[Menu]

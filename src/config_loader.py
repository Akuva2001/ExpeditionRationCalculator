"""
config_loader.py

This module provides functionalities to parse command-line arguments and load
configuration data from YAML files or dictionaries for the meal planning application.
It ensures the integrity and validity of the loaded configurations.
"""

import argparse
from typing import Dict, List
import sys

from .products import Product, load_products
from .meals import load_meals, load_everyday, Meal
from .day import Day, load_days
from .daily_norms import DailyNorms, load_daily_norms
from .menus import load_menus, Menu
from .config import MealPlannerConfig


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments for configuration file paths and debug mode.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Generate a meal plan.")
    parser.add_argument(
        "--menu",
        default="menu/sample_menu.yml",
        help="Path to the menu file."
    )
    parser.add_argument(
        "--products",
        default="products/products.yml",
        help="Path to the products file."
    )
    parser.add_argument(
        "--meals",
        default="meals/meals.yml",
        help="Path to the meals file."
    )
    parser.add_argument(
        "--days",
        default="days/days.yml",
        help="Path to the days file."
    )
    parser.add_argument(
        "--everyday",
        default="meals/everyday.yml",
        help="Path to the everyday products file."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode for detailed output."
    )
    return parser.parse_args()


def load_configuration(args: argparse.Namespace) -> MealPlannerConfig:
    """
    Loads all necessary configurations for meal planning.

    Args:
        args (argparse.Namespace): Parsed command-line arguments containing file paths.
        debug (bool): Flag indicating whether to enable debug mode.

    Returns:
        MealPlannerConfig: An instance of MealPlannerConfig populated with loaded data.

    Raises:
        SystemExit: If any of the configuration loading steps fail.
    """
    debug = args.debug
    try:
        # Load products
        if debug:
            print("Loading products...")
        products: Dict[str, Product] = load_products(args.products)
        if debug:
            print(f"Loaded {len(products)} products.\n")

        # Load meals
        if debug:
            print("Loading meals...")
        meals: Dict[str, Meal] = load_meals(args.meals, products)
        if debug:
            print(f"Loaded {len(meals)} meals.\n")

        # Load everyday products
        if debug:
            print("Loading everyday products...")
        everyday: Meal = load_everyday(args.everyday, products)
        if debug:
            print("Loaded everyday meal.\n")

        # Load days
        if debug:
            print("Loading days...")
        days: Dict[str, Day] = load_days(args.days, meals, everyday)
        if debug:
            print(f"Loaded {len(days)} days.\n")

        # Load daily norms
        if debug:
            print("Loading daily nutritional norms...")
        daily_norms: DailyNorms = load_daily_norms(args.menu)
        if debug:
            print("Loaded daily norms.\n")

        # Load menus
        if debug:
            print("Loading menus...")
        menus: List[Menu] = load_menus(args.menu, days)
        if debug:
            print(f"Loaded {len(menus)} menus.\n")

        # Create MealPlannerConfig instance
        config = MealPlannerConfig(
            products=products,
            meals=meals,
            everyday=everyday,
            days=days,
            daily_norms=daily_norms,
            menus=menus
        )

        return config

    except (FileNotFoundError, ValueError, TypeError) as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)


def load_configuration_from_dict(config_dict: Dict[str, str]) -> MealPlannerConfig:
    """
    Loads all necessary configurations for meal planning from a dictionary.

    This function is useful for programmatic access, such as testing in Jupyter Notebooks.

    Args:
        config_dict (Dict[str, str]): A dictionary containing file paths for configurations.
            Expected keys: 'menu', 'products', 'meals', 'days', 'everyday'.
        debug (bool, optional): Flag indicating whether to enable debug mode. Defaults to False.

    Returns:
        MealPlannerConfig: An instance of MealPlannerConfig populated with loaded data.

    Raises:
        ValueError: If any required configuration paths are missing in config_dict.
        SystemExit: If any of the configuration loading steps fail.
    """
    required_keys = ['menu', 'products', 'meals', 'days', 'everyday']
    missing_keys = [key for key in required_keys if key not in config_dict]
    if missing_keys:
        raise ValueError(f"Missing configuration keys: {', '.join(missing_keys)}")

    class Args:
        menu = config_dict['menu']
        products = config_dict['products']
        meals = config_dict['meals']
        days = config_dict['days']
        everyday = config_dict['everyday']
        debug = config_dict.get('debug', False)

    args_instance = Args()
    return load_configuration(args_instance)

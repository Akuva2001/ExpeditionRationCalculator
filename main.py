"""
main.py

This script serves as the entry point for generating meal plans based on predefined
menus, meals, days, and product data. It loads configurations from YAML files or dictionaries,
validates the data, calculates nutritional information, and generates a Bill of Materials (BOM)
for shopping purposes.

Functionality:
    - Parses command-line arguments for configuration file paths and debug mode.
    - Loads and validates product, meal, day, daily norms, and menu data.
    - Checks daily nutritional rules and provides warnings if norms are not met.
    - Calculates total nutritional values and weights for menus.
    - Generates and prints categorized shopping lists (BOM) for individual menus and all menus combined.
    - Supports programmatic configuration loading for testing purposes.
"""

from src.config_loader import parse_arguments, load_configuration, load_configuration_from_dict
from src.display import display_menu_info, display_bom
from src.menus import calculate_total_weight



def main():
    """
    The main function orchestrates the loading of configurations, validation, and output generation
    for the meal planning application. It handles command-line arguments, loads data from YAML files
    or dictionaries, checks nutritional rules, and generates shopping lists.
    """
    # Parse command-line arguments
    args = parse_arguments()

    # Load all configurations
    config = load_configuration(args)

    # Display menu information and check nutritional rules
    display_menu_info(config.menus, config.daily_norms)

    # Display Bill of Materials (BOM)
    display_bom(config.menus, config.products)

    # Calculate and display total weight of all menus
    total_weight = calculate_total_weight(config.menus)
    print(f"Общий вес: {total_weight/1000:.1f} кг")


if __name__ == "__main__":
    main()

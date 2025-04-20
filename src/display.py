"""
display.py

This module contains functions responsible for displaying menu information and
the Bill of Materials (BOM) in a readable format for the meal planning application.
"""

import yaml
from typing import Dict, List
from .menus import Menu
from .products import Product, productGroups
from .daily_norms import DailyNorms
from .bom_generator import get_bom_for_menus, group_products_by_category
from .special_symbols import green_book, blue_book, exclamation, warning_sign
from .utilities import number_to_emoji



def display_menu_info(menus: List[Menu], daily_norms: DailyNorms):
    """
    Displays information about each menu, including nutritional values and any warnings.

    Args:
        menus (List[Menu]): A list of Menu instances.
        daily_norms (DailyNorms): The daily nutritional norms to check against.
        green_book (str): Unicode character for green book emoji.
        exclamation (str): Unicode character for exclamation mark emoji.
        warning_sign (str): Unicode character for warning sign emoji.
    """
    print(f"{green_book} Раскладка:")
    # Print information for each menu
    for i, menu in enumerate(menus, start=1):
        print(f"{green_book} Секция меню \"{menu.name}\":")
        print(f"  Веса дней {[f'{day.weight/1000:.1f}' for day in menu.days]}, общий вес {menu.total_weight/1000:.1f} кг")

        # Check rules for each day in the menu
        for day in menu.days:
            warnings = day.check_rules(daily_norms)
            for warning in warnings:
                print(f"  {exclamation} {warning}")

        # Print warning count
        warning_count = sum(len(day.check_rules(daily_norms)) for day in menu.days)
        print(f"{warning_sign} {warning_count} предупреждений")
        print()

        # Print meals for each day in the menu
        for j, day in enumerate(menu.days, start=1):
            print(f"{number_to_emoji(j, 2)}  Меню на ночёвку {j}, {day.people_count} человек: {day.name}")
            print(f"    ужин:    {day.dinner.name} ({', '.join(f'{product.name} {quantity * day.people_count:.0f}' for product, quantity in day.dinner.products)})")
            print(f"    завтрак: {day.breakfast.name} ({', '.join(f'{product.name} {quantity * day.people_count:.0f}' for product, quantity in day.breakfast.products)})")
            print(f"    перекус: {day.lunch.name} ({', '.join(f'{product.name} {quantity * day.people_count:.0f}' for product, quantity in day.lunch.products)})")
            print()

        print()


def display_bom(menus: List[Menu], products: Dict[str, Product]):
    """
    Displays the Bill of Materials (BOM) for each menu and for all menus combined.

    Args:
        menus (List[Menu]): A list of Menu instances.
        products (Dict[str, Product]): A dictionary of Product instances.
        blue_book (str): Unicode character for blue book emoji.
    """
    # Print BOM for each menu
    print(f"\n{blue_book} Список покупок для каждой секции меню по отдельности:")
    for menu in menus:
        print(f"{blue_book} Меню: {menu.name}, вес: {menu.total_weight/1000:.1f} кг")
        bom = get_bom_for_menus([menu])
        grouped_products = group_products_by_category(bom, products)
        print_grouped_products(grouped_products, indent=1)
        print()
    if len(menus) > 1:
        # Print combined BOM for all menus
        print(f"\n{green_book}{green_book} Список покупок для всех меню вместе:")
        combined_bom = get_bom_for_menus(menus)
        grouped_combined = group_products_by_category(combined_bom, products)
        print_grouped_products(grouped_combined, indent=0)


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
        print(f"{'  '*indent}{pg}:")
        pr_d = grouped_products[pg]
        for _ in range(indent+1):
            pr_d = {"some": pr_d}
        dump = yaml.dump(pr_d, default_flow_style=False, allow_unicode=True)
        lines = dump.splitlines()
        dump = '\n'.join(lines[indent+1:])
        print(dump)

"""
display.py

This module contains functions responsible for displaying menu information and
the Bill of Materials (BOM) in a readable format for the meal planning application.
"""

import yaml
from typing import Dict, List
from .menus import Menu
from .products import Product, productCategoryMap, productGroups
from .bom_generator import get_bom_for_menus, group_products_by_category



def display_menu_info(menus: List[Menu], daily_norms: 'DailyNorms', green_book: str, exclamation: str, warning_sign: str):
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
        print(f"  Веса дней {[f'{day.weight:.0f}' for day in menu.days]}, общий вес {menu.total_weight:.0f} кг")

        # Check rules for each day in the menu
        for day in menu.days:
            warnings = day.check_rules(daily_norms)
            for warning in warnings:
                print(f"  {exclamation} {warning}")

        # Print warning count
        warning_count = sum(len(day.check_rules(daily_norms)) for day in menu.days)
        print(f"{warning_sign} {warning_count} предупреждений")

        # Print meals for each day in the menu
        for j, day in enumerate(menu.days, start=1):
            print(f"  Меню на ночёвку {j}, {day.people_count} человек:")
            print(f"    ужин:    {day.dinner.name} ({', '.join(f'{product.name} {quantity * day.people_count:.0f}' for product, quantity in day.dinner.products)})")
            print(f"    завтрак: {day.breakfast.name} ({', '.join(f'{product.name} {quantity * day.people_count:.0f}' for product, quantity in day.breakfast.products)})")
            print(f"    перекус: {day.lunch.name} ({', '.join(f'{product.name} {quantity * day.people_count:.0f}' for product, quantity in day.lunch.products)})")

        print()


def display_bom(menus: List[Menu], products: Dict[str, Product], blue_book: str):
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
        print(f"{blue_book} Меню: {menu.name}, вес: {menu.total_weight:.0f} кг")
        bom = get_bom_for_menus([menu])
        grouped_products = group_products_by_category(bom, products)
        print_grouped_products(grouped_products, indent=1)
        print()

    # Print combined BOM for all menus
    print(f"\n{blue_book} Список покупок для всех меню вместе:")
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

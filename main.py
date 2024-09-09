import argparse
import yaml
from src.products import load_products
from src.meals import load_meals
from src.menus import (load_menus,
                       get_bom_for_menus, calculate_total_weight,
                       group_products_by_category, print_grouped_products)
from src.day import load_days
from src.dailyNorms import load_daily_norms

def main():
    parser = argparse.ArgumentParser(description="Generate a meal plan.")
    parser.add_argument("--menu", default="menu/sample_menu.yml", help="Path to the menu file.")
    parser.add_argument("--products", default="products/products.yml", help="Path to the products file.")
    parser.add_argument("--meals", default="meals/meals.yml", help="Path to the meals file.")
    parser.add_argument("--days", default="days/days.yml", help="Path to the days file.")
    args = parser.parse_args()

    green_book = chr(0x1F4D7)
    blue_book = chr(0x1F4D8)
    exclamation = chr(0x2757)
    warning_sign = chr(0x26A0)


    # Load products
    products = load_products(args.products)

    # Load meals
    meals = load_meals(args.meals, products)

    # Load days
    days = load_days(args.days, meals)

    # Load daily norms
    daily_norms = load_daily_norms(args.menu)

    # Load menus
    menus = load_menus(args.menu, days)

        
    # # Check rules
    # print("Список уникальных дней и замечаний по ним:")
    # for name, day in days.items():
    #     print(f"  День: {name}, вес на человека: {day.weight:.0f} г.")
    #     warnings = day.check_rules(daily_norms)
    #     # Print warnings
    #     for warning in warnings:
    #         print(f"   {exclamation}", warning)

    print(f"{green_book} Раскладка:")
    # Print information for each menu
    for i, menu in enumerate(menus, start=1):
        print(f"{green_book} Секция меню \"{menu.name}\":")
        print(f"  веса дней {[f'{day.weight:.0f}' for day in menu.days]}, общий вес {menu.total_weight:.0f}")

        # Check rules for each day in the menu
        for day in menu.days:
            warnings = day.check_rules(daily_norms)
            for warning in warnings:
                print(f"  {exclamation} {warning}")

        # Print warning count
        warning_count = sum(len(day.check_rules(daily_norms)) for day in menu.days)
        print(f"{warning_sign} {warning_count}")

        # Print meals for each day in the menu# Print meals for each day in the menu
        for j, day in enumerate(menu.days, start=1):
            print(f"  Меню на ночёвку {j}:")
            print(f"    ужин:    {day.dinner.name} ({', '.join(f'{product.name} {quantity * menu.people_count:.0f}' for product, quantity in day.dinner.products)})")
            print(f"    завтрак: {day.breakfast.name} ({', '.join(f'{product.name} {quantity * menu.people_count:.0f}' for product, quantity in day.breakfast.products)})")
            print(f"    перекус: {day.lunch.name} ({', '.join(f'{product.name} {quantity * menu.people_count:.0f}' for product, quantity in day.lunch.products)})")

        print()

    # Print BOM for each menu
    print(f"\n{blue_book} Список покупок для каждой секции меню по отедльности:")
    for menu in menus:
        print(f"{blue_book} Меню: {menu.name}, вес: {menu.total_weight:.0f}")
        bom = get_bom_for_menus(menus)
        grouped_products = group_products_by_category(bom, products)
        print_grouped_products(grouped_products, indent=1)
        print()

    print(f"\n{green_book}{green_book} Список покупок для всех меню вместе:")
    bom = get_bom_for_menus(menus)
    grouped_products = group_products_by_category(bom, products)
    print_grouped_products(grouped_products, indent=0)
        
    print(f"Общий вес: {calculate_total_weight(menus):.0f}")

if __name__ == "__main__":
    main()

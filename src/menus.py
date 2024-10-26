import yaml
from dataclasses import dataclass, field
from typing import List
from .day import Day, DailyNorms
from .products import productCategoryMap, productGroups


@dataclass
class Menu:
    name: str
    days: List[Day]
    people_count: int
    calories: float = 0
    proteins: float = 0
    fats: float = 0
    carbohydrates: float = 0
    weight_per_person: float = 0
    total_weight: float = 0

    def __post_init__(self):
        for day in self.days:
            self.calories += day.calories
            self.proteins += day.proteins
            self.fats += day.fats
            self.carbohydrates += day.carbohydrates
            self.weight_per_person += day.weight
            self.total_weight += day.weight * self.people_count
    
    def get_bom(self):
        bom = {}
        for day in self.days:
            for meal in [day.breakfast, day.lunch, day.dinner]:
                for product, quantity in meal.products:
                    bom[product.name] = bom.get(product.name, 0) + quantity * self.people_count
        return bom


def load_menus(filename: str, days: dict[str, Day]) -> List[Menu]:
    with open(filename) as f:
        config = yaml.safe_load(f)

    menus = []
    for menu_name, menu_data in config['menus'].items():
        menu_days = []
        for day_name in menu_data['days']:
            if day_name in days:
                menu_days.append(days[day_name])
            else:
                raise ValueError(f"Invalid day: {day_name}")
        menus.append(Menu(menu_name, menu_days, menu_data['people_count']))

    return menus

def get_bom_for_menus(menus: List[Menu]) -> dict:
    bom = {}
    for menu in menus:
        for day in menu.days:
            for meal in [day.breakfast, day.lunch, day.dinner, day.everyday]:
                for product, quantity in meal.products:
                    bom[product.name] = bom.get(product.name, 0) + quantity * menu.people_count
    return bom

def calculate_total_weight(menus: List[Menu]) -> float:
    total_weight = 0
    for menu in menus:
        total_weight += menu.total_weight
    return total_weight

def group_products_by_category(bom: dict, products: dict) -> dict:
    grouped_products = {}
    for product_name, quantity in bom.items():
        product = products[product_name]
        category = productCategoryMap.get(product.group, "Другое")
        if category not in grouped_products:
            grouped_products[category] = {}
        grouped_products[category][product_name] = quantity
    return grouped_products

def print_grouped_products(grouped_products: dict, indent: int = 0):
    for pg in productGroups:
        print(f"{'  '*indent}{pg}:")
        pr_d = grouped_products[pg]
        for _ in range(indent+1):
            pr_d = {"some": pr_d}
        dump = yaml.dump(pr_d, default_flow_style=False, allow_unicode=True)
        lines = dump.splitlines()
        dump = '\n'.join(lines[indent+1:])
        print(dump)


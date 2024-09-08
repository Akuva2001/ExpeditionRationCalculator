import yaml
from dataclasses import dataclass
from enum import Enum

class ProductCategory(Enum):
    Whatever = 0
    Grains = 1
    Vegetables = 2
    Meat = 3
    Milk = 4
    Dispersed = 5
    Drinkable = 6
    Sweets = 7
    Nuts = 8
    TouristShop = 9
    Sausage = 10

productGroups = ["Крупы", "Овощи", "Мясо и молочка", "Сладкое", "Сухофрукты и орехи", "Другое"]

productCategoryMap = {ProductCategory.Whatever: "Другое",
                     ProductCategory.Grains: "Крупы",
                     ProductCategory.Vegetables: "Овощи",
                     ProductCategory.Meat: "Мясо и молочка",
                     ProductCategory.Milk: "Мясо и молочка",
                     ProductCategory.Dispersed: "Другое",
                     ProductCategory.Drinkable: "Другое",
                     ProductCategory.Sweets: "Сладкое",
                     ProductCategory.Nuts: "Сухофрукты и орехи",
                     ProductCategory.TouristShop: "Другое"}

@dataclass
class Product:
    name: str
    calories: float
    proteins: float
    fats: float
    carbohydrates: float
    group: ProductCategory = ProductCategory.Whatever
    packageWeight: int = 1000
    costPerPackage: int = 0
    percentage: float = 100.0

    def __post_init__(self):
        if isinstance(self.group, str):
            self.group = getattr(ProductCategory, self.group)



def load_products(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)

    products = {}
    for name, details in data['products'].items():
        product = Product(name, **details)
        products[name] = product

    return products

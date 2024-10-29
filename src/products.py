"""
products.py

This module defines the Product and ProductCategory classes, along with utility functions
to load product data from YAML files. It ensures the integrity and validity of product
information used in meal planning applications.

Classes:
    ProductCategory: An enumeration of possible product categories.
    Product: A dataclass representing a product with its nutritional and packaging details.

Functions:
    load_products(filename: str) -> Dict[str, Product]:
        Loads products from a YAML file and returns a dictionary of Product instances.
"""

import yaml
from dataclasses import dataclass
from enum import Enum
from typing import Dict


class ProductCategory(Enum):
    """
    Enumeration of product categories.

    Attributes:
        WHATEVER (str): Default category for unspecified products.
        GRAINS (str): Category for grain products.
        VEGETABLES (str): Category for vegetable products.
        MEAT (str): Category for meat products.
        MILK (str): Category for milk products.
        DISPERSSED (str): Category for dispersed products.
        DRINKABLE (str): Category for drinkable products.
        SWEETS (str): Category for sweet products.
        NUTS (str): Category for nuts and dried fruits.
        TOURIST_SHOP (str): Category for tourist shop products.
        SAUSAGE (str): Category for sausage products.
    """
    WHATEVER = "Whatever"
    GRAINS = "Grains"
    VEGETABLES = "Vegetables"
    MEAT = "Meat"
    MILK = "Milk"
    DISPERSSED = "Dispersed"
    DRINKABLE = "Drinkable"
    SWEETS = "Sweets"
    NUTS = "Nuts"
    TOURIST_SHOP = "TouristShop"
    SAUSAGE = "Sausage"

    @staticmethod
    def from_str(label: str) -> 'ProductCategory':
        """
        Converts a string label to a corresponding ProductCategory enum member.

        Args:
            label (str): The string representation of the category.

        Returns:
            ProductCategory: The corresponding enum member.

        Example:
            >>> ProductCategory.from_str("grains")
            ProductCategory.GRAINS

        If the label does not match any enum member, returns ProductCategory.WHATEVER.
        """
        try:
            return ProductCategory[label.upper().replace(" ", "_")]
        except KeyError:
            return ProductCategory.WHATEVER


# List of product groups in Russian for categorization
productGroups = ["Крупы", "Овощи", "Мясо и молочка", "Сладкое", "Сухофрукты и орехи", "Другое"]

# Mapping from ProductCategory enum to Russian product group names
productCategoryMap: Dict[ProductCategory, str] = {
    ProductCategory.WHATEVER: "Другое",
    ProductCategory.GRAINS: "Крупы",
    ProductCategory.VEGETABLES: "Овощи",
    ProductCategory.MEAT: "Мясо и молочка",
    ProductCategory.MILK: "Мясо и молочка",
    ProductCategory.DISPERSSED: "Другое",
    ProductCategory.DRINKABLE: "Другое",
    ProductCategory.SWEETS: "Сладкое",
    ProductCategory.NUTS: "Сухофрукты и орехи",
    ProductCategory.TOURIST_SHOP: "Другое",
    ProductCategory.SAUSAGE: "Другое"
}


@dataclass
class Product:
    """
    Represents a product with its nutritional information and packaging details.

    Attributes:
        name (str): The name of the product.
        calories (float): Calories per 100 grams of the product.
        proteins (float): Proteins per 100 grams of the product.
        fats (float): Fats per 100 grams of the product.
        carbohydrates (float): Carbohydrates per 100 grams of the product.
        group (ProductCategory): The category of the product.
        packageWeight (int): The weight of one package in grams.
        costPerPackage (float): The cost of one package in currency units.
        percentage (float): Freshness or quality percentage of the product.
    """

    name: str
    calories: float
    proteins: float
    fats: float
    carbohydrates: float
    group: ProductCategory = ProductCategory.WHATEVER
    packageWeight: int = 1000  # in grams
    costPerPackage: float = 0.0  # in currency units
    percentage: float = 100.0  # freshness or similar metric

    def __post_init__(self):
        """
        Validates and processes the product data after initialization.

        - Converts the group from string to ProductCategory enum if necessary.
        - Validates that numerical fields are within acceptable ranges.

        Raises:
            ValueError: If any numerical field is out of its valid range or if the group is invalid.
            TypeError: If the group is neither a string nor a ProductCategory enum member.
        """
        # Convert group from string to ProductCategory enum if necessary
        if isinstance(self.group, str):
            try:
                self.group = ProductCategory.from_str(self.group)
            except Exception as e:
                raise ValueError(f"Invalid group '{self.group}' for product '{self.name}': {e}")
        elif not isinstance(self.group, ProductCategory):
            raise TypeError(f"Group must be a string or ProductCategory enum for product '{self.name}'")

        # Validate numerical fields
        if self.calories < 0:
            raise ValueError(f"Calories cannot be negative for product '{self.name}'")
        if self.proteins < 0:
            raise ValueError(f"Proteins cannot be negative for product '{self.name}'")
        if self.fats < 0:
            raise ValueError(f"Fats cannot be negative for product '{self.name}'")
        if self.carbohydrates < 0:
            raise ValueError(f"Carbohydrates cannot be negative for product '{self.name}'")
        if self.packageWeight <= 0:
            raise ValueError(f"Package weight must be positive for product '{self.name}'")
        if not (0.0 <= self.percentage <= 100.0):
            raise ValueError(f"Percentage must be between 0 and 100 for product '{self.name}'")
        if self.costPerPackage < 0:
            raise ValueError(f"Cost per package cannot be negative for product '{self.name}'")


def load_products(filename: str) -> Dict[str, Product]:
    """
    Loads products from a YAML file and returns a dictionary of Product instances.

    The YAML file should have the following structure:

    ```yaml
    products:
      product_name_1:
        calories: 250
        proteins: 10
        fats: 5
        carbohydrates: 30
        group: "Grains"
        packageWeight: 1000
        costPerPackage: 50.0
        percentage: 100.0
      product_name_2:
        ...
    ```

    Args:
        filename (str): Path to the YAML file containing product data.

    Returns:
        Dict[str, Product]: A dictionary mapping product names to Product instances.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the YAML file has invalid format or contains invalid product data.
        TypeError: If any of the fields have incorrect types.
    """
    products: Dict[str, Product] = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Products file not found: {filename}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {filename}: {e}")

    # Validate the structure of the YAML data
    if not isinstance(data, dict) or 'products' not in data:
        raise ValueError(f"Invalid products file format: 'products' key not found in {filename}")

    for name, details in data['products'].items():
        if not isinstance(details, dict):
            raise ValueError(f"Invalid product details for '{name}': expected a dictionary")

        # Ensure all required fields are present and have correct types
        required_fields = ['calories', 'proteins', 'fats', 'carbohydrates']
        for field_name in required_fields:
            if field_name not in details:
                raise ValueError(f"Missing required field '{field_name}' for product '{name}'")
            if not isinstance(details[field_name], (int, float)):
                raise TypeError(f"Field '{field_name}' for product '{name}' must be a number")

        # Get optional fields with defaults
        group = details.get('group', ProductCategory.WHATEVER)
        package_weight = details.get('packageWeight', 1000)
        cost_per_package = details.get('costPerPackage', 0.0)
        percentage = details.get('percentage', 100.0)

        try:
            product = Product(
                name=name,
                calories=float(details['calories']),
                proteins=float(details['proteins']),
                fats=float(details['fats']),
                carbohydrates=float(details['carbohydrates']),
                group=group,
                packageWeight=int(package_weight),
                costPerPackage=float(cost_per_package),
                percentage=float(percentage)
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"Error creating Product '{name}': {e}")

        # Check for duplicate product names
        if name in products:
            raise ValueError(f"Duplicate product name detected: '{name}'")

        products[name] = product

    return products

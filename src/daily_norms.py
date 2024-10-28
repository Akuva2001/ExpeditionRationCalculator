"""
daily_norms.py

This module defines the DailyNorms dataclass and a utility function to load daily nutritional norms
from a YAML configuration file. It ensures that the nutritional norms used in meal planning
applications are correctly loaded and validated.
"""

import yaml
from dataclasses import dataclass
from typing import Any, Dict
import os


@dataclass
class DailyNorms:
    """
    Represents the daily nutritional norms.

    Attributes:
        daily_calories_min (float): Minimum daily calorie intake.
        daily_calories_max (float): Maximum daily calorie intake.
        daily_protein (float): Minimum daily protein intake in grams.
        daily_fat (float): Minimum daily fat intake in grams.
        daily_carbs (float): Minimum daily carbohydrate intake in grams.
    """
    daily_calories_min: float = 2500
    daily_calories_max: float = 3200
    daily_protein: float = 55
    daily_fat: float = 60
    daily_carbs: float = 290

    def __post_init__(self):
        """
        Validates the initialized values to ensure they meet logical constraints.

        Raises:
            ValueError: If any of the nutritional norms are set to negative values or if the
                        minimum calories exceed the maximum calories.
        """
        if self.daily_calories_min < 0:
            raise ValueError("daily_calories_min cannot be negative.")
        if self.daily_calories_max < 0:
            raise ValueError("daily_calories_max cannot be negative.")
        if self.daily_protein < 0:
            raise ValueError("daily_protein cannot be negative.")
        if self.daily_fat < 0:
            raise ValueError("daily_fat cannot be negative.")
        if self.daily_carbs < 0:
            raise ValueError("daily_carbs cannot be negative.")
        if self.daily_calories_min > self.daily_calories_max:
            raise ValueError("daily_calories_min cannot be greater than daily_calories_max.")


def load_daily_norms(filename: str) -> DailyNorms:
    """
    Loads daily nutritional norms from a YAML file and returns a DailyNorms instance.

    The YAML file should have the following structure:

    ```yaml
    rules:
      daily_calories_min: 2500
      daily_calories_max: 3200
      daily_protein: 55
      daily_fat: 60
      daily_carbs: 290
    ```

    Args:
        filename (str): Path to the YAML file containing daily norms.

    Returns:
        DailyNorms: An instance of DailyNorms populated with values from the YAML file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
        ValueError: If the YAML file has an invalid format or contains invalid values.
        TypeError: If any of the fields have incorrect types.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Daily norms file not found: {filename}")

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {filename}: {e}")

    if not isinstance(data, dict):
        raise ValueError(f"Invalid format: Expected a dictionary at the top level in {filename}.")

    if 'rules' not in data:
        raise ValueError(f"Invalid format: 'rules' key not found in {filename}.")

    rules = data['rules']
    if not isinstance(rules, dict):
        raise ValueError(f"Invalid format: 'rules' should be a dictionary in {filename}.")

    # Define the required fields and their expected types
    required_fields: Dict[str, Any] = {
        'daily_calories_min': float,
        'daily_calories_max': float,
        'daily_protein': float,
        'daily_fat': float,
        'daily_carbs': float
    }

    # Validate the presence and types of required fields
    validated_rules: Dict[str, float] = {}
    for field, field_type in required_fields.items():
        if field not in rules:
            raise ValueError(f"Missing required field '{field}' in 'rules' of {filename}.")
        value = rules[field]
        if not isinstance(value, (int, float)):
            raise TypeError(f"Field '{field}' must be a number (int or float) in {filename}.")
        validated_rules[field] = float(value)

    # Create and return the DailyNorms instance with validated data
    try:
        daily_norms = DailyNorms(**validated_rules)
    except ValueError as e:
        raise ValueError(f"Error initializing DailyNorms: {e}")

    return daily_norms

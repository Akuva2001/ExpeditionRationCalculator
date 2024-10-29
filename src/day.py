"""
day.py

This module defines the Day dataclass and utility functions to load day configurations
from YAML files. It ensures the integrity and validity of daily meal plans used in
meal planning applications.

Classes:
    Day: A dataclass representing a day's meal plan, including breakfast, lunch, dinner,
         and everyday meals.

Functions:
    load_days(filename: str, meals: Dict[str, Meal], everyday: Meal) -> Dict[str, Day]:
        Loads day configurations from a YAML file and returns a dictionary of Day instances.
"""

import yaml
from dataclasses import dataclass
from typing import List, Dict
import os

from .meals import Meal
from .daily_norms import DailyNorms


@dataclass
class Day:
    """
    Represents a day's meal plan, including breakfast, lunch, dinner, and everyday meals.

    Attributes:
        name (str): The name of the day.
        breakfast (Meal): The breakfast meal.
        lunch (Meal): The lunch meal.
        dinner (Meal): The dinner meal.
        everyday (Meal): The everyday meal (e.g., snacks).
        calories (float): Total calories for the day.
        proteins (float): Total proteins for the day in grams.
        fats (float): Total fats for the day in grams.
        carbohydrates (float): Total carbohydrates for the day in grams.
        weight (float): Total weight of the meals for the day in kilograms.
        people_count (int): Number of people for whom the meals are planned.
    """
    name: str
    breakfast: Meal
    lunch: Meal
    dinner: Meal
    everyday: Meal
    calories: float = 0.0
    proteins: float = 0.0
    fats: float = 0.0
    carbohydrates: float = 0.0
    weight: float = 0.0
    people_count: int = 1

    def __post_init__(self):
        """
        Calculates the total nutritional values and weight of the day's meals based on individual meals.

        Raises:
            ValueError: If people_count is less than 1.
        """
        if self.people_count < 1:
            raise ValueError(f"people_count must be at least 1 for day '{self.name}'.")

        # Sum up nutritional values and weight from all meals
        self.calories = (
            self.breakfast.calories +
            self.lunch.calories +
            self.dinner.calories +
            self.everyday.calories
        )
        self.proteins = (
            self.breakfast.proteins +
            self.lunch.proteins +
            self.dinner.proteins +
            self.everyday.proteins
        )
        self.fats = (
            self.breakfast.fats +
            self.lunch.fats +
            self.dinner.fats +
            self.everyday.fats
        )
        self.carbohydrates = (
            self.breakfast.carbohydrates +
            self.lunch.carbohydrates +
            self.dinner.carbohydrates +
            self.everyday.carbohydrates
        )
        self.weight = (
            self.breakfast.weight +
            self.lunch.weight +
            self.dinner.weight +
            self.everyday.weight
        )

    def check_rules(self, rules: DailyNorms) -> List[str]:
        """
        Checks the day's nutritional values against the provided daily norms and returns any warnings.

        Args:
            rules (DailyNorms): The daily nutritional norms to check against.

        Returns:
            List[str]: A list of warning messages if any norms are not met.
        """
        warnings = []
        if self.calories < rules.daily_calories_min:
            warnings.append(
                f"Слишком мало калорий: {self.calories:.0f}, нужно ещё {rules.daily_calories_min - self.calories:.0f}"
            )
        if self.calories > rules.daily_calories_max:
            warnings.append(
                f"Слишком много калорий: {self.calories:.0f}, избыток {self.calories - rules.daily_calories_max:.0f}"
            )
        if self.proteins < rules.daily_protein:
            warnings.append(
                f"Слишком мало белков: {self.proteins:.0f}, нужно ещё {rules.daily_protein - self.proteins:.0f}"
            )
        if self.fats < rules.daily_fat:
            warnings.append(
                f"Слишком мало жиров: {self.fats:.0f}, нужно ещё {rules.daily_fat - self.fats:.0f}"
            )
        if self.carbohydrates < rules.daily_carbs:
            warnings.append(
                f"Слишком мало углеводов: {self.carbohydrates:.0f}, нужно ещё {rules.daily_carbs - self.carbohydrates:.0f}"
            )
        return warnings


def load_days(filename: str, meals: Dict[str, Meal], everyday: Meal) -> Dict[str, Day]:
    """
    Loads day configurations from a YAML file and returns a dictionary of Day instances.

    The YAML file should have the following structure:

    ```yaml
    days:
      day_name_1:
        breakfast: meal_name_1
        lunch: meal_name_2
        dinner: meal_name_3
      day_name_2:
        breakfast: meal_name_4
        lunch: meal_name_5
        dinner: meal_name_6
      ...
    ```

    Args:
        filename (str): Path to the YAML file containing day configurations.
        meals (Dict[str, Meal]): Dictionary of available meals.
        everyday (Meal): The everyday meal to be included in each day.

    Returns:
        Dict[str, Day]: A dictionary mapping day names to Day instances.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
        ValueError: If the YAML file has an invalid format or contains invalid meal names.
        TypeError: If any of the fields have incorrect types.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Days file not found: {filename}")

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            days_data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {filename}: {e}")

    if not isinstance(days_data, dict):
        raise ValueError(f"Invalid format: Expected a dictionary at the top level in {filename}.")

    if 'days' not in days_data:
        raise ValueError(f"Invalid format: 'days' key not found in {filename}.")

    days = {}
    for day_name, day_details in days_data['days'].items():
        if not isinstance(day_details, dict):
            raise ValueError(f"Invalid day details for '{day_name}': expected a dictionary.")

        # Extract meal names
        breakfast_name = day_details.get('breakfast')
        lunch_name = day_details.get('lunch')
        dinner_name = day_details.get('dinner')
        people_count = day_details.get('people_count', 1)  # Default to 1 if not specified

        # Validate presence of required meals
        if not breakfast_name:
            raise ValueError(f"Missing 'breakfast' for day '{day_name}' in {filename}.")
        if not lunch_name:
            raise ValueError(f"Missing 'lunch' for day '{day_name}' in {filename}.")
        if not dinner_name:
            raise ValueError(f"Missing 'dinner' for day '{day_name}' in {filename}.")

        # Retrieve Meal instances
        breakfast = meals.get(breakfast_name)
        lunch = meals.get(lunch_name)
        dinner = meals.get(dinner_name)

        if not breakfast:
            raise ValueError(
                f"Invalid breakfast meal '{breakfast_name}' for day '{day_name}' in {filename}."
            )
        if not lunch:
            raise ValueError(
                f"Invalid lunch meal '{lunch_name}' for day '{day_name}' in {filename}."
            )
        if not dinner:
            raise ValueError(
                f"Invalid dinner meal '{dinner_name}' for day '{day_name}' in {filename}."
            )

        # Validate people_count
        if not isinstance(people_count, int) or people_count < 1:
            raise ValueError(
                f"Invalid people_count '{people_count}' for day '{day_name}' in {filename}. It must be a positive integer."
            )

        # Create Day instance with specified people_count
        day = Day(
            name=day_name,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            everyday=everyday,
            people_count=people_count
        )

        if day_name in days:
            raise ValueError(f"Duplicate day name detected: '{day_name}' in {filename}.")

        days[day_name] = day

    return days

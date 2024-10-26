import yaml
from dataclasses import dataclass
from typing import List
from .meals import Meal
from .dailyNorms import DailyNorms


@dataclass
class Day:
    name: str
    breakfast: Meal
    lunch: Meal
    dinner: Meal
    everyday: Meal
    calories: float = 0
    proteins: float = 0
    fats: float = 0
    carbohydrates: float = 0
    weight: float = 0
    people_count: int = 1

    def __post_init__(self):
        self.calories = self.breakfast.calories + self.lunch.calories + self.dinner.calories + self.everyday.calories
        self.proteins = self.breakfast.proteins + self.lunch.proteins + self.dinner.proteins + self.everyday.proteins
        self.fats = self.breakfast.fats + self.lunch.fats + self.dinner.fats + self.everyday.fats
        self.carbohydrates = self.breakfast.carbohydrates + self.lunch.carbohydrates + self.dinner.carbohydrates + self.everyday.carbohydrates
        self.weight = self.breakfast.weight + self.lunch.weight + self.dinner.weight + self.everyday.weight

    def check_rules(self, rules: DailyNorms) -> List[str]:
        warnings = []
        if self.calories < rules.daily_calories_min:
            warnings.append(f"Слишком мало калорий: {self.calories:.0f}, нужно ещё {rules.daily_calories_min - self.calories:.0f}")
        if self.calories > rules.daily_calories_max:
            warnings.append(f"Слишком много калорий: {self.calories:.0f}, избыток {self.calories - rules.daily_calories_max:.0f}")
        if self.proteins < rules.daily_protein:
            warnings.append(f"Слишком мало белков: {self.proteins:.0f}, нужно ещё {rules.daily_protein - self.proteins:.0f}")
        if self.fats < rules.daily_fat:
            warnings.append(f"Слишком мало жиров: {self.fats:.0f}, нужно ещё {rules.daily_fat - self.fats:.0f}")
        if self.carbohydrates < rules.daily_carbs:
            warnings.append(f"Слишком мало углеводов: {self.carbohydrates:.0f}, нужно ещё {rules.daily_carbs - self.carbohydrates:.0f}")
        return warnings



def load_days(filename: str, meals: dict[str, Meal], everyday: Meal) -> dict[str, Day]:
    with open(filename) as f:
        days_data = yaml.safe_load(f)

    days = {}
    for day_name, day_data in days_data['days'].items():
        breakfast = meals.get(day_data['breakfast'])
        lunch = meals.get(day_data['lunch'])
        dinner = meals.get(day_data['dinner'])
        if not breakfast:
            raise ValueError(f"Invalid meal in day: {day_name}, meal_name: {day_data['breakfast']}, day_data: {day_data}")
        if not lunch:
            raise ValueError(f"Invalid meal in day: {day_name}, meal_name: {day_data['lunch']}, day_data: {day_data}")
        if not dinner:
            raise ValueError(f"Invalid meal in day: {day_name}, meal_name: {day_data['dinner']}, day_data: {day_data}")
        days[day_name] = Day(day_name, breakfast, lunch, dinner, everyday)

    return days
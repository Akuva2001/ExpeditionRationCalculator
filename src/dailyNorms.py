import yaml
from dataclasses import dataclass

@dataclass
class DailyNorms:
    daily_calories_min: float = 2500
    daily_calories_max: float = 3200
    daily_protein: float = 55
    daily_fat: float = 60
    daily_carbs: float = 290

def load_daily_norms(filename: str) -> DailyNorms:
    with open(filename) as f:
        data = yaml.safe_load(f)
    return DailyNorms(**data['rules'])
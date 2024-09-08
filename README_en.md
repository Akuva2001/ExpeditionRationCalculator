# Meal Planner Project

This project is a meal planning application that allows you to plan menus based on products, meals, and daily norms. The application allows you to load products, meals, and days from YAML files, and to load menus and check them against daily norms.

This project is also a port from Kotlin to Python of this project: https://gitlab.com/zimy/expedition-ration-calculator-classes. Some configuration changes were made during cloning, but the main idea remained the same.

## Requirements

To run this application, you need Python and a package manager such as pip. You can search for instructions on how to install them for your specific case.

## Installation

1. Clone the repository:

```
git clone https://github.com/Akuva2001/ExpeditionRationCalculator.git
```

2. Navigate to the project directory:

```
cd ExpeditionRationCalculator
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Run the application:

```
python meal_planner.py --menu menu/sample_menu.yml --products products/products.yml --meals meals/meals.yml --days days/days.yml
```

2. The application will output the meal plan, a list of purchases for each menu section separately, and a list of purchases for all menus combined.
3. You can modify the [products.yaml](products/products.yaml), [meals.yaml](meals/meals.yml), [days.yaml](days/days.yml), and [sample_menu.yaml](menu/sample_menu.yml) files, or create new ones. When creating new files, don't forget to specify the path to them in the command to run the application.
4. As an alternative, you can open the [main.ipynb](main.ipynb) file, which has the same functionality.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
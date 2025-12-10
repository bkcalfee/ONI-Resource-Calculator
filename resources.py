"""
Data module for the ONI resource calculator.

This file defines dictionaries that describe resources, food
items, and buildings. The main calculator imports these values
and uses them in computations.
"""

# Basic resource definitions. Each resource has a 'name',
# an optional unit, and a short description. Values are
# illustrative rather than game-accurate.
RESOURCES = {
    "water": {"name": "Water", "unit": "kg", "desc": "Liquid water"},
    "oxygen": {"name": "Oxygen", "unit": "kg", "desc": "Breathable O2"},
    "algae": {"name": "Algae", "unit": "kg", "desc": "Algae for oxygen production"},
    "coal": {"name": "Coal", "unit": "kg", "desc": "Fuel for generators"},
    "iron_ore": {"name": "Iron Ore", "unit": "kg", "desc": "Basic building material"},
}

# Food items. Each food entry includes calories per unit so
# the calculator can determine how many units are needed.
# Numbers are illustrative.
FOODS = {
    "mushroom": {"name": "Mushroom", "calories": 120, "unit": "kg", "desc": "Raw food"},
    "grilled_mushroom": {"name": "Grilled Mushroom", "calories": 400, "unit": "plate", "desc": "Cooked meal"},
    "basic_meal": {"name": "Basic Meal", "calories": 1200, "unit": "plate", "desc": "Full meal"},
}

# Building costs per structure: how many kg of resource are
# required to build one unit of the building. Use these to
# estimate material needs.
BUILDINGS = {
    "simple_bed": {"name": "Simple Cot", "iron_ore": 20},
    "oxygen_generator": {"name": "O2 Generator", "iron_ore": 50, "algae": 10},
    "water_pump": {"name": "Water Pump", "iron_ore": 40},
}


def sample_project():
    """Return a very small sample project dictionary for demo/testing.

    This is used by the demo code so we can run the module without
    typing input during automated tests.
    """
    return {
        "duplicants": 3,
        "days": 7,
        "food_choice": "basic_meal",
        "buildings": {"simple_bed": 3, "oxygen_generator": 1},
    }

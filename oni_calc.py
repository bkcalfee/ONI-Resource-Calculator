"""
Oxygen Not Included - Resource Calculator

This module provides a self-contained project that calculates
resource needs for a colony over a number of days.

Features:
- Compute food needs (based on a chosen food item with calories)
- Compute building material totals
- Save and load project files (JSON)
- Export a short summary to CSV

The code aims to be readable and straightforward.
"""

import os
import csv
import sys
from pathlib import Path

# When this file is run directly (or imported by runpy), Python may not
# find sibling modules unless the folder is on sys.path. Try a normal
# import first; if it fails, add the file directory to sys.path and
# import again. This makes the import more robust for testing.
try:
    from resources import RESOURCES, FOODS, BUILDINGS, sample_project
    from utils import safe_int, print_table, save_project, load_project, time_stamp
except Exception:
    this_dir = str(Path(__file__).resolve().parent)
    if this_dir not in sys.path:
        sys.path.insert(0, this_dir)
    from resources import RESOURCES, FOODS, BUILDINGS, sample_project
    from utils import safe_int, print_table, save_project, load_project, time_stamp


def compute_requirements(duplicants, days, food_key, buildings):
    """Compute total resource requirements for a small project.

    Parameters
    - duplicants: int count of duplicants
    - days: number of in-game days to plan for
    - food_key: key from FOODS dictionary
    - buildings: dict of building_key -> count

    Returns a dict with totals for food and materials.
    """
    if food_key not in FOODS:
        raise ValueError("Unknown food: " + str(food_key))

    food_info = FOODS[food_key]
    calories_per_unit = food_info["calories"]

    # Fixed daily calorie need per duplicant (illustrative value).
    calories_per_duplicant_per_day = 1200

    total_calories_needed = duplicants * days * calories_per_duplicant_per_day

    # Compute how many food units we need (round up)
    units_needed = total_calories_needed // calories_per_unit
    if total_calories_needed % calories_per_unit:
        units_needed += 1

    # Building material totals
    materials = {}
    for bkey, count in buildings.items():
        info = BUILDINGS.get(bkey)
        if not info:
            # skip unknown building keys but continue
            continue
        for res_key, qty in info.items():
            if res_key == "name":
                continue
            materials[res_key] = materials.get(res_key, 0) + qty * count

    return {
        "duplicants": duplicants,
        "days": days,
        "food": {"key": food_key, "units": units_needed, "unit": food_info.get("unit")},
        "materials": materials,
    }


def format_summary(requirements):
    """Return a short printable summary (list of rows) for print_table."""
    rows = []
    rows.append(["Duplicants", requirements["duplicants"]])
    rows.append(["Days", requirements["days"]])

    food = requirements["food"]
    rows.append(["Food item", FOODS[food["key"]]["name"]])
    rows.append(["Food units needed", f"{food['units']} {food['unit']}"])

    # Add materials
    rows.append(["", ""])  # blank row for spacing
    rows.append(["Material", "Total"])
    for mat, qty in requirements["materials"].items():
        name = RESOURCES.get(mat, {}).get("name", mat)
        unit = RESOURCES.get(mat, {}).get("unit", "units")
        rows.append([name, f"{qty} {unit}"])

    return rows


def save_summary_csv(path, requirements):
    """Save a minimal CSV with the results so the user can open it in a spreadsheet."""
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Duplicants", requirements['duplicants']])
        writer.writerow(["Days", requirements['days']])
        writer.writerow([""])
        food = requirements['food']
        writer.writerow(["Food item", FOODS[food['key']]['name']])
        writer.writerow(["Food units needed", f"{food['units']} {food['unit']}"])
        writer.writerow([""])
        writer.writerow(["Material", "Total"])
        for mat, qty in requirements['materials'].items():
            name = RESOURCES.get(mat, {}).get('name', mat)
            unit = RESOURCES.get(mat, {}).get('unit', 'units')
            writer.writerow([name, f"{qty} {unit}"])


def interactive_create_project():
    """Interactively create a project using basic input calls.

    Keep prompts short and avoid advanced arguments.
    """
    print("Create a small ONI resource project")
    dup = safe_int("How many duplicants? ")
    days = safe_int("How many days to plan for? ")

    print("Available food choices:")
    for k, v in FOODS.items():
        print(f" - {k}: {v['name']} ({v['calories']} cal per {v['unit']})")

    food_choice = input("Choose food key from above (e.g. basic_meal): ").strip()
    if food_choice not in FOODS:
        print("Unknown food choice; defaulting to 'basic_meal'.")
        food_choice = 'basic_meal'

    print("\nNow enter building counts. Press Enter to keep zero.")
    buildings = {}
    for bkey, info in BUILDINGS.items():
        cnt = input(f"How many {info['name']}? ").strip()
        try:
            cnt = int(cnt) if cnt else 0
        except ValueError:
            cnt = 0
        if cnt:
            buildings[bkey] = cnt

    project = {
        'duplicants': dup,
        'days': days,
        'food_choice': food_choice,
        'buildings': buildings,
    }
    return project


def main_menu():
    """Main interactive menu for the project.

    Use numbered options and short prompts.
    """
    print("ONI Resource Calculator")
    print("Type the number for the action and press Enter.")

    while True:
        print("\nMenu:")
        print("1) Create new project")
        print("2) Load project from file")
        print("3) Run demo project")
        print("4) Quit")

        choice = input("> ").strip()
        if choice == '1':
            proj = interactive_create_project()
        elif choice == '2':
            path = input("Enter project JSON filename to load: ").strip()
            try:
                proj = load_project(path)
                print("Loaded project from", path)
            except Exception as e:
                print("Failed to load project:", e)
                continue
        elif choice == '3':
            proj = sample_project()
            print("Using demo project from resources.sample_project()")
        elif choice == '4':
            print("Goodbye")
            break
        else:
            print("Unknown option")
            continue

        # Compute requirements and show a summary
        req = compute_requirements(proj['duplicants'], proj['days'], proj['food_choice'], proj.get('buildings', {}))
        rows = format_summary(req)
        print('\n--- Project Summary ---')
        print_table(rows)

        # Offer to save
        save = input("Save project and summary? (y/N): ").strip().lower()
        if save == 'y':
            name = input("Filename base (without extension), or press Enter for timestamp: ").strip()
            if not name:
                name = time_stamp()
            json_path = name + ".json"
            csv_path = name + "_summary.csv"
            try:
                save_project(json_path, proj)
                save_summary_csv(csv_path, req)
                print(f"Saved {json_path} and {csv_path}")
            except Exception as e:
                print("Error saving:", e)


if __name__ == '__main__':
    # If the user runs the file, show the simple menu.
    main_menu()

"""
Utility helpers for the ONI calculator.

Small helper functions that keep the main code organized.
Functions include input parsing, table printing, and project
save/load operations.
"""

import json
from datetime import datetime


def safe_int(prompt, default=None):
    """Prompt for an integer and return it.

    If the user types something invalid, prompt again.
    This centralizes conversion handling in one place.
    """
    while True:
        try:
            text = input(prompt)
            if text.strip() == "" and default is not None:
                return default
            return int(text)
        except ValueError:
            print("Please type a whole number (e.g. 3). Try again.")


def print_table(rows, headers=None):
    """Print a table (list of rows) with optional headers.

    Columns are aligned using basic string formatting.
    """
    if not rows:
        print("(no rows)")
        return

    # Compute column widths
    cols = len(rows[0])
    widths = [0] * cols
    if headers:
        for i, h in enumerate(headers):
            widths[i] = max(widths[i], len(str(h)))
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(str(c)))

    # Header
    if headers:
        line = "  ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
        print(line)
        print("-" * len(line))

    # Rows
    for r in rows:
        print("  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)))


def save_project(path, data):
    """Save a project dictionary to a JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_project(path):
    """Load a project dictionary from a JSON file and return it."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def time_stamp():
    """Return a short timestamp string for saving files and logs."""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

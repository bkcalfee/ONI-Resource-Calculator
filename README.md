# ONI Resource Calculator

Brief description
-----------------
This small project computes basic resource needs for a colony in the game "Oxygen Not Included" (ONI). It is a self-contained set of Python modules that:

- calculate food requirements for a specified number of duplicants over a number of days,
- compute total building material needs for simple building counts,
- allow saving/loading of project settings (JSON) and exporting a summary (CSV),
- provide an interactive command-line menu to create projects and run a demo.

Files in this folder
--------------------
- `oni_calc.py` — main program: interactive menu, computation functions, CSV export, and save/load handlers.
- `resources.py` — data definitions for resources, food items, and building costs used by the calculator.
- `utils.py` — helper functions: input parsing, table printing, JSON save/load, and timestamp helper.

Requirements
------------
- Python 3.8 or newer is recommended.
- No third-party packages are required; the code uses only the Python standard library (modules such as `json`, `csv`, `datetime`, and `pathlib`).

How to run
----------
Open a terminal (PowerShell) and change to this folder:

```powershell
cd "c:\Users\bkcal\iCloudDrive\School\Fall 2025\ISAT 252 Python\FINAL\ONI"
```

- Run the interactive menu:

```powershell
python .\oni_calc.py
```

Choose option `3` to run the included demo project (quick verification). You can also create a new project (option `1`) or load a saved project (option `2`).

- Run the demo non-interactively (starts the program; follow prompts):

```powershell
python -c "import runpy; runpy.run_path(r'.\\oni_calc.py')"
```

- Call functions directly from a Python REPL (example):

```python
import runpy
ns = runpy.run_path('oni_calc.py')
from resources import sample_project
proj = sample_project()
req = ns['compute_requirements'](proj['duplicants'], proj['days'], proj['food_choice'], proj['buildings'])
print(req)
```

What the code produces
----------------------
- When you compute requirements, the result includes total food units needed and a dictionary of material totals (e.g., iron ore, algae).
- If you choose to save a project, the program writes a `.json` project file and a `_summary.csv` file with the same base name.

Notes
-----
- Resource and food numbers in `resources.py` are illustrative and simplified; they are intended for demonstration and classroom use, not exact game balances.
- The project uses only standard Python library modules, so no additional installation is required beyond having Python itself.

Next steps (optional)
---------------------
- Add oxygen/water consumption rates and include them in the summary.
- Add unit tests or a `demo_run.py` script that runs the demo and saves outputs automatically.
- Create a `README` in the repository root with links to this folder and to run instructions for other scripts.

If you want any of the optional next steps, tell me which and I will add them.

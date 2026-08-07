# Dorm Hallway Dining-Menu Board

Shows the campus dining-hall menu for the **current or next meal** on a screen
in the hallway. It figures out the right meal from the clock and the serving
schedule, scrapes the menu, and displays it fullscreen.

Menu source: https://menus.campus-dining.com/eliorna/d1031
(NC School of Science & Math – Morganton, "d1031")

## One-time setup

1. Install [Python 3.9+](https://www.python.org/downloads/) (check "Add Python to PATH").
2. Open a terminal in this folder and run:

   ```bash
   pip install -r requirements.txt
   ```

## Run it

Fullscreen board (this is what the hallway PC should run):

```bash
python menu_board.py
```

- Press **Esc** (or **q**) to quit.
- It re-checks the clock and re-scrapes every 10 minutes automatically.

### Testing / other modes

Print the menu once to the console (no window):

```bash
python menu_board.py --once
```

Force a specific day and meal:

```bash
python menu_board.py --date 2026-08-13 --meal Lunch
```

## Which meal does it show?

Serving schedule (Eastern time):

| Days      | Meals                                                        |
|-----------|--------------------------------------------------------------|
| Mon–Fri   | Breakfast 7:00–9:30 · Lunch 11:00–13:00 · Dinner 17:00–19:00 |
| Sat–Sun   | Brunch 10:00–13:00 (listed as "Lunch") · Dinner 17:00–19:00  |

- During a meal → that meal, tagged **NOW SERVING**.
- Between meals → the next meal, tagged **UP NEXT**.
- After the last meal of the day → tomorrow's first meal.

## Make it start automatically (optional)

To have the board launch when the PC boots, create a shortcut to:

```
pythonw menu_board.py
```

and drop it in the Startup folder (press `Win+R`, type `shell:startup`, Enter).
Using `pythonw` (instead of `python`) hides the console window.

## If the menu ever stops loading

The dining site could change its page structure or the unit code. The two
things to check in `menu_board.py`:

- `UNIT = "eliorna/d1031"` — the campus/dining-hall code (from the menu URL).
- The CSS class names in `_parse_stations()` / `_parse_periods()`
  (`k10-recipe__name`, `k10-recipe__nutrient_energy`, `k10-course__name`,
  `k10-menu-selector__option`).

#!/usr/bin/env python3
"""
Dorm Hallway Dining-Menu Board
==============================

Scrapes the campus dining-hall menu (Tenkites / Elior platform) and shows the
menu for the *current or next* meal, based on the serving schedule.

Menu source (unit d1031 = "NC School of Science & Math - Morganton"):
    https://menus.campus-dining.com/eliorna/d1031

Serving schedule (Eastern time):
    Mon-Fri : Breakfast 7:00-9:30, Lunch 11:00-13:00, Dinner 17:00-19:00
    Sat/Sun : Brunch    10:00-13:00 (shown as "Lunch" on the menu), Dinner 17:00-19:00

Which meal is shown?
    - If a meal is being served right now  -> that meal        ("NOW SERVING")
    - If we're between meals               -> the next meal    ("UP NEXT")
    - If the day's meals are all over      -> tomorrow's first meal

Usage:
    python menu_board.py            # fullscreen board that refreshes itself (press Esc to quit)
    python menu_board.py --once     # print the menu once to the console and exit (good for testing)
    python menu_board.py --date 2026-08-13 --meal Lunch   # force a specific day/meal (testing)

Requirements:  pip install -r requirements.txt
"""

import argparse
import sys
from datetime import datetime, time, timedelta

import requests
from bs4 import BeautifulSoup

try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python < 3.9
    print("This script needs Python 3.9 or newer.")
    sys.exit(1)


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
BASE = "https://menus.tenkites.com"
UNIT = "eliorna/d1031"          # the campus/dining-hall code from the menu URL
EASTERN = "America/New_York"    # schedule is in Eastern time
REFRESH_MINUTES = 10            # how often the board re-scrapes / re-checks the clock
HTTP_TIMEOUT = 20               # seconds


def eastern_now():
    """Current time in Eastern (handles EST/EDT automatically)."""
    try:
        return datetime.now(ZoneInfo(EASTERN))
    except Exception:
        print(
            "Could not load the 'America/New_York' timezone.\n"
            "On Windows, run:  pip install tzdata\n"
        )
        raise


# --------------------------------------------------------------------------- #
# Serving schedule  ->  which meal to show
# --------------------------------------------------------------------------- #
# Each entry: (label shown on board, start, end, period-name used on the menu site)
def meals_for_day(day):
    weekday = day.weekday()  # Mon=0 ... Sun=6
    if weekday < 5:  # Monday - Friday
        return [
            ("Breakfast", time(7, 0),  time(9, 30), "Breakfast"),
            ("Lunch",     time(11, 0), time(13, 0), "Lunch"),
            ("Dinner",    time(17, 0), time(19, 0), "Dinner"),
        ]
    else:            # Saturday / Sunday  (brunch is listed as "Lunch" on the menu)
        return [
            ("Brunch", time(10, 0), time(13, 0), "Lunch"),
            ("Dinner", time(17, 0), time(19, 0), "Dinner"),
        ]


def pick_meal(now):
    """
    Return (date, board_label, menu_period_name, status) for the meal to display.
    Looks at today first, then rolls forward day by day if today's meals are done.
    """
    tz = now.tzinfo
    day = now.date()
    for _ in range(8):  # look ahead up to a week (handles breaks with no menus)
        for label, start, end, period_name in meals_for_day(day):
            end_dt = datetime.combine(day, end, tzinfo=tz)
            if now < end_dt:
                start_dt = datetime.combine(day, start, tzinfo=tz)
                status = "NOW SERVING" if now >= start_dt else "UP NEXT"
                return day, label, period_name, status
        day = day + timedelta(days=1)  # everything today is over; try the next day
    # Fallback (should never happen)
    day = now.date()
    return day, "Breakfast", "Breakfast", "UP NEXT"


# --------------------------------------------------------------------------- #
# Scraping
# --------------------------------------------------------------------------- #
def _menu_url(date_str, mlguid=None):
    url = f"{BASE}/{UNIT}?cl=true&mldate={date_str}&internalrequest=true"
    if mlguid:
        url += f"&mlguid={mlguid}"
    return url


def _get_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (dorm-menu-board)"}
    resp = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    return resp.text


def _parse_periods(soup):
    """Return list of (period_name, guid) offered for the loaded date."""
    periods = []
    for opt in soup.select(".k10-menu-selector__option[data-menu-identifier]"):
        name = opt.get_text(strip=True)
        guid = opt.get("data-menu-identifier")
        if name and guid:
            periods.append((name, guid))
    return periods


def _parse_stations(soup):
    """
    Walk the menu body in order, grouping items under their station header.
    Returns list of {"name": station, "items": [(item_name, calories), ...]}.
    """
    stations = []
    current = None
    for el in soup.select(".k10-course__name, .k10-recipe.k10-recipe_menu-item"):
        classes = el.get("class", [])
        if "k10-course__name" in classes:
            current = {"name": el.get_text(" ", strip=True), "items": []}
            stations.append(current)
        else:  # a recipe/menu item card
            name_el = el.select_one(".k10-recipe__name")
            cal_el = el.select_one(".k10-recipe__nutrient_energy")
            name = name_el.get_text(" ", strip=True) if name_el else ""
            cal = cal_el.get_text(" ", strip=True) if cal_el else ""
            if not name:
                continue
            if current is None:  # items before any station header
                current = {"name": "", "items": []}
                stations.append(current)
            current["items"].append((name, cal))
    # Drop empty stations
    return [s for s in stations if s["items"]]


def scrape_menu(date_str, wanted_period):
    """
    Fetch the menu for `date_str` and the `wanted_period` (e.g. "Lunch").
    Returns dict: {date, period, available_periods, stations} or None if no menu.
    """
    # 1) Load the date once to discover which periods exist and their ids.
    soup = BeautifulSoup(_get_html(_menu_url(date_str)), "html.parser")
    periods = _parse_periods(soup)
    if not periods:
        return None  # no menu posted for this day

    # 2) Match the wanted period (case-insensitive); fall back to the default view.
    guid = None
    matched_name = None
    for name, g in periods:
        if name.lower() == wanted_period.lower():
            guid, matched_name = g, name
            break

    if guid:
        soup = BeautifulSoup(_get_html(_menu_url(date_str, guid)), "html.parser")
        shown_period = matched_name
    else:
        # Requested period isn't offered that day; show whatever the site defaults to.
        sel = soup.select_one(".k10-menu-selector__name")
        shown_period = sel.get_text(strip=True) if sel else periods[0][0]

    stations = _parse_stations(soup)
    return {
        "date": date_str,
        "period": shown_period,
        "available_periods": [p[0] for p in periods],
        "stations": stations,
    }


def get_board_data(now=None, force_date=None, force_meal=None):
    """High-level: decide the meal, scrape it, and package everything for display."""
    now = now or eastern_now()
    if force_date and force_meal:
        day = datetime.strptime(force_date, "%Y-%m-%d").date()
        board_label, period_name, status = force_meal, force_meal, "SELECTED"
    else:
        day, board_label, period_name, status = pick_meal(now)

    date_str = day.strftime("%Y-%m-%d")
    pretty_date = day.strftime("%A, %B %-d") if sys.platform != "win32" \
        else day.strftime("%A, %B %d").replace(" 0", " ")

    try:
        menu = scrape_menu(date_str, period_name)
        error = None
    except Exception as exc:  # network / parse problems shouldn't crash the board
        menu, error = None, str(exc)

    return {
        "now": now,
        "date_str": date_str,
        "pretty_date": pretty_date,
        "board_label": board_label,
        "status": status,
        "menu": menu,
        "error": error,
    }


# --------------------------------------------------------------------------- #
# Console output (for testing / headless use)
# --------------------------------------------------------------------------- #
def render_text(data):
    lines = []
    header = f"{data['board_label'].upper()}  ({data['status']})"
    #lines.append("=" * 60)
    lines.append(header.center(60))
    #lines.append(data["pretty_date"].center(60))
    #lines.append("=" * 60)

    if data["error"]:
        lines.append("")
        lines.append("  Could not load the menu right now.")
        lines.append(f"  ({data['error']})")
    elif not data["menu"] or not data["menu"]["stations"]:
        lines.append("")
        lines.append("  No menu posted for this meal yet. Check back soon!")
    else:
        for station in data["menu"]["stations"]:
            lines.append("")
            #lines.append(f"  {station['name']}")
            #lines.append("  " + "-" * (len(station["name"]) or 4))
            for name, cal in station["items"]:
                cal_txt = f"  ({cal})" if cal else ""
                lines.append(f"{name}{cal_txt}")
    lines.append("")
    #lines.append(f"Updated {data['now'].strftime('%-I:%M %p') if sys.platform!='win32' else data['now'].strftime('%I:%M %p').lstrip('0')}".center(60))
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Fullscreen GUI board (Tkinter — built into Python, no extra install)
# --------------------------------------------------------------------------- #
def run_gui():
    import tkinter as tk

    BG = "#0f3d2e"      # dark green (matches the dining site)
    ACCENT = "#a5c422"  # lime green
    FG = "#ffffff"

    root = tk.Tk()
    root.title("Dining Menu")
    root.configure(bg=BG)
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("q", lambda e: root.destroy())

    # Scrollable area
    canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(root, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    inner = tk.Frame(canvas, bg=BG)
    canvas.create_window((0, 0), window=inner, anchor="nw", width=root.winfo_screenwidth())
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    root.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"))

    def clear():
        for w in inner.winfo_children():
            w.destroy()

    def build(data):
        clear()
        pad = 40
        tk.Label(inner, text=f"{data['board_label']}  •  {data['status']}",
                 font=("Segoe UI", 46, "bold"), bg=BG, fg=ACCENT).pack(anchor="w", padx=pad, pady=(30, 0))
        tk.Label(inner, text=data["pretty_date"],
                 font=("Segoe UI", 26), bg=BG, fg=FG).pack(anchor="w", padx=pad)
        tk.Frame(inner, bg=ACCENT, height=4).pack(fill="x", padx=pad, pady=18)

        if data["error"]:
            tk.Label(inner, text="Could not load the menu right now.\nWill retry automatically.",
                     font=("Segoe UI", 24), bg=BG, fg=FG, justify="left").pack(anchor="w", padx=pad, pady=20)
        elif not data["menu"] or not data["menu"]["stations"]:
            tk.Label(inner, text="No menu posted for this meal yet.\nCheck back soon!",
                     font=("Segoe UI", 24), bg=BG, fg=FG, justify="left").pack(anchor="w", padx=pad, pady=20)
        else:
            for station in data["menu"]["stations"]:
                tk.Label(inner, text=station["name"], font=("Segoe UI", 30, "bold"),
                         bg=BG, fg=ACCENT).pack(anchor="w", padx=pad, pady=(16, 2))
                for name, cal in station["items"]:
                    row = tk.Frame(inner, bg=BG)
                    row.pack(anchor="w", fill="x", padx=pad + 20)
                    tk.Label(row, text=f"• {name}", font=("Segoe UI", 22),
                             bg=BG, fg=FG).pack(side="left")
                    if cal:
                        tk.Label(row, text=f"   {cal}", font=("Segoe UI", 18),
                                 bg=BG, fg="#c9d6b0").pack(side="left")

        tk.Label(inner, text=f"Updated {data['now'].strftime('%I:%M %p').lstrip('0')}   •   Esc to exit",
                 font=("Segoe UI", 14), bg=BG, fg="#9fb39a").pack(anchor="w", padx=pad, pady=30)
        canvas.yview_moveto(0)

    def refresh():
        try:
            build(get_board_data())
        except Exception as exc:
            clear()
            tk.Label(inner, text=f"Error: {exc}", font=("Segoe UI", 20),
                     bg=BG, fg=FG).pack(padx=40, pady=40)
        root.after(REFRESH_MINUTES * 60 * 1000, refresh)  # schedule next refresh

    refresh()
    root.mainloop()


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Dorm dining-hall menu board")
    ap.add_argument("--once", action="store_true", help="print the menu once and exit")
    ap.add_argument("--date", help="force a date, YYYY-MM-DD (testing)")
    ap.add_argument("--meal", help="force a meal: Breakfast/Lunch/Dinner (testing)")
    args = ap.parse_args()

    if args.once or args.date or args.meal:
        data = get_board_data(force_date=args.date, force_meal=args.meal)
        #print(data)
        print(render_text(data))
    else:
        run_gui()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from datetime import datetime

SCHEDULE = {
    0: [("8:30", "9:20", "A"), ("9:25", "10:15", "B"), ("10:20", "11:10", "C"), ("11:15", "12:05", "D"), ("12:05", "12:55", "LUNCH"), ("12:55", "1:45", "E"), ("1:50", "2:40", "F"), ("2:45", "3:35", "G"), ("3:40", "5:00", "Meeting")],
    1: [("8:30", "9:20", "D"), ("9:25", "10:15", "E"), ("10:20", "11:10", "A"), ("11:10", "11:50", "A LAB"), ("11:50", "12:40", "LUNCH"), ("12:40", "1:20", "G LAB"), ("1:20", "2:10", "G"), ("2:15", "3:05", "F"), ("3:05", "4:00", "Flexible Use Time")],
    2: [("8:30", "9:20", "B"), ("9:25", "10:15", "D"), ("10:20", "11:10", "C"), ("11:10", "11:50", "C LAB"), ("11:50", "12:40", "LUNCH"), ("12:40", "1:20", "E LAB"), ("1:20", "2:10", "E"), ("2:15", "3:05", "F"), ("3:10", "4:00", "G")],
    3: [("8:30", "9:20", "C"), ("9:25", "10:15", "A"), ("10:20", "11:10", "B"), ("11:10", "11:50", "B LAB"), ("11:50", "12:40", "LUNCH"), ("12:40", "1:20", "F LAB"), ("1:20", "2:10", "F"), ("2:15", "3:05", "G"), ("3:05", "4:00", "Flexible Use Time")],
    4: [("8:30", "9:20", "A"), ("9:25", "10:15", "C"), ("10:20", "11:10", "D"), ("11:10", "11:50", "D LAB"), ("11:50", "12:40", "LUNCH"), ("12:40", "1:30", "B"), ("1:35", "2:25", "E"), ("2:25", "3:05", "E LAB"), ("3:05", "4:00", "Flexible Use Time")],
}

MEALS = [
    (7*60, 9*60 + 30, "BREAKFAST"),
    (11*60, 13*60, "LUNCH"),
    (17*60, 19*60, "DINNER"),
]

def to_minutes(t):
    t = t.strip().lower()
    is_pm = "pm" in t
    is_am = "am" in t
    t = t.replace("am", "").replace("pm", "").strip()
    h, m = map(int, t.split(":"))
    if is_pm and h != 12:
        h += 12
    if is_am and h == 12:
        h = 0
    return h * 60 + m

def fmt_minutes(n):
    h, m = divmod(max(0, n), 60)
    if h and m:
        return f"{h} hour(s) {m} minute(s)"
    if h:
        return f"{h} hour(s)"
    return f"{m} minute(s)"

def find_current(now_min, items):
    for i, (start, end, label) in enumerate(items):
        s = to_minutes(start) if isinstance(start, str) else start
        e = to_minutes(end) if isinstance(end, str) else end
        if s <= now_min < e:
            return i, (s, e, label)
    return None, None

def find_next(now_min, items):
    for start, end, label in items:
        s = to_minutes(start) if isinstance(start, str) else start
        e = to_minutes(end) if isinstance(end, str) else end
        if now_min < s:
            return (s, e, label)
    return None

def find_next_class(now_min, day_blocks):
    for start, end, label in day_blocks:
        if label in {"BREAKFAST", "LUNCH", "DINNER"}:
            continue
        s = to_minutes(start)
        e = to_minutes(end)
        if now_min < s:
            return (s, e, label)
    return None

def main():
    now = datetime.now()
    day = now.weekday()
    now_min = now.hour * 60 + now.minute
    blocks = SCHEDULE.get(day, [])

    meal_idx, meal = find_current(now_min, MEALS)
    class_idx, cur_class = find_current(now_min, blocks)
    next_class = find_next_class(now_min, blocks)
    next_meal = find_next(now_min, MEALS)

    if meal and cur_class and cur_class[2] not in {"LUNCH"}:
        _, _, meal_label = meal
        _, _, class_label = cur_class
        message = f"{meal_label} right now. {class_label} right now."
        if next_class:
            ns, ne, nl = next_class
            message += f" {fmt_minutes(ns - now_min)} till {nl} block."
        return (message)
        

    if meal and not cur_class:
        _, _, meal_label = meal
        message = f"{meal_label} right now."
        if next_class:
            ns, ne, nl = next_class
            message += f" {fmt_minutes(ns - now_min)} till {nl} block."
        return (message)
        

    if cur_class:
        _, _, class_label = cur_class
        nxt = find_next(now_min, blocks)
        if nxt:
            ns, ne, nl = nxt
            if nl in {"BREAKFAST", "LUNCH", "DINNER"}:
                message = f"{class_label} right now. {fmt_minutes(ns - now_min)} till {nl} block."
            else:
                message = f"{class_label} right now. {fmt_minutes(ns - now_min)} till {nl} block."
        else:
            message = f"{class_label} right now. No later blocks scheduled."
        return (message)
        

    if next_class:
        ns, ne, nl = next_class
        return (f"No block right now. {fmt_minutes(ns - now_min)} till {nl} block.")
        

    return ("No more scheduled blocks today.")

if __name__ == "__main__":
    print(main())

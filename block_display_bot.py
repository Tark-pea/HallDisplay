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
    (7 * 60, 9 * 60 + 30, "BREAKFAST"),
    (11 * 60, 13 * 60, "LUNCH"),
    (17 * 60, 19 * 60, "DINNER"),
]


def to_minutes(t):
    """Convert a time string to minutes after midnight."""
    t = t.strip().lower()

    if "am" in t or "pm" in t:
        is_pm = "pm" in t
        t = t.replace("am", "").replace("pm", "").strip()
        h, m = map(int, t.split(":"))

        if is_pm and h != 12:
            h += 12
        elif not is_pm and h == 12:
            h = 0
    else:
        h, m = map(int, t.split(":"))

        # School schedule assumption:
        # 8-11 = morning
        # 12 = noon
        # 1-7 = afternoon
        if 1 <= h <= 7:
            h += 12

    return h * 60 + m


# Convert schedule once
SCHEDULE_MIN = {
    day: [(to_minutes(s), to_minutes(e), label) for s, e, label in blocks]
    for day, blocks in SCHEDULE.items()
}


def fmt_minutes(n):
    h, m = divmod(max(0, n), 60)
    if h and m:
        return f"{h} hour(s) {m} minute(s)"
    if h:
        return f"{h} hour(s)"
    return f"{m} minute(s)"


def current_item(now_min, items):
    for i, (start, end, label) in enumerate(items):
        if start <= now_min < end:
            return i, (start, end, label)
    return None, None


def next_item(now_min, items):
    for start, end, label in items:
        if now_min < start:
            return (start, end, label)
    return None


def class_now(now_min, blocks):
    class_items = [
        item for item in blocks
        if item[2] not in {"BREAKFAST", "LUNCH", "DINNER"}
    ]
    return current_item(now_min, class_items)


def next_class(now_min, blocks):
    class_items = [
        item for item in blocks
        if item[2] not in {"BREAKFAST", "LUNCH", "DINNER"}
    ]
    return next_item(now_min, class_items)


def meal_now(now_min):
    return current_item(now_min, MEALS)


def status_text(now=None):
    if now is None:
        now = datetime.now()

    day = now.weekday()
    now_min = now.hour * 60 + now.minute

    blocks = SCHEDULE_MIN.get(day, [])

    _, cls = class_now(now_min, blocks)
    _, meal = meal_now(now_min)
    nclass = next_class(now_min, blocks)

    if meal and cls:
        msg = f"{meal[2]} right now. {cls[2]} right now."
        if nclass:
            msg += f" {fmt_minutes(nclass[0] - now_min)} till {nclass[2]} block."
        return msg

    if meal:
        msg = f"{meal[2]} right now."
        if nclass:
            msg += f" {fmt_minutes(nclass[0] - now_min)} till {nclass[2]} block."
        return msg

    if cls:
        nxt = next_item(now_min, blocks)
        if nxt:
            return f"{cls[2]} right now. {fmt_minutes(nxt[0] - now_min)} till {nxt[2]} block."
        return f"{cls[2]} right now. No later blocks scheduled."

    if nclass:
        return f"No block right now. {fmt_minutes(nclass[0] - now_min)} till {nclass[2]} block."

    return "No more scheduled blocks today."


if __name__ == "__main__":
    print(status_text())

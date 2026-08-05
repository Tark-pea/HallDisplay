#!/usr/bin/env python3
import tkinter as tk
from datetime import datetime
import block_display_bot as bdb

BG = "#111111"
STONE = "#1b1b1b"
STONE_2 = "#252525"
BLUE = "#2c7fb8"
JADE = "#c1296d"
TERRACOTTA = "#b35a3c"
CREAM = "#f2e6c9"
GOLD = "#d4a64a"
BORDER = "#4a3b22"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hall Display")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())

        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True)

        top = tk.Frame(root, bg=BG)
        top.pack(fill="x", pady=(10, 8))

        self.time_label = tk.Label(
            top, fg=CREAM, bg=BG, font=("Sans", 42, "bold"), pady=8
        )
        self.time_label.pack()

        self.time_bar = tk.Frame(top, bg=BLUE, height=8)
        self.time_bar.pack(fill="x", padx=30, pady=(6, 0))

        self.block_frame = self.make_panel(root, "Today's Blocks", BLUE, 0)
        self.block_frame.pack(fill="x", padx=26, pady=(12, 14))

        self.block_label = tk.Label(
            self.block_frame.body,
            fg=JADE,
            bg=STONE,
            font=("Sans", 30, "bold"),
            wraplength=900,
            justify="center",
        )
        self.block_label.pack(fill="both", expand=True, padx=18, pady=18)

        self.important_frame = self.make_panel(root, "Important things", TERRACOTTA, 1)
        self.important_frame.pack(fill="x", padx=26, pady=(8, 14))
        self.add_bullet(self.important_frame.body, "Welcome Juniors!", CREAM)
        self.add_bullet(self.important_frame.body, "And Welcome Back Seniors!", CREAM)
        self.add_bullet(self.important_frame.body, "To those new here, welcome to the best hall on campus!", CREAM)

        self.extra_frame = self.make_panel(root, "Menu", GOLD, 2)
        self.extra_frame.pack(fill="x", padx=26, pady=(8, 14))
        tk.Label(
            self.extra_frame.body,
            text="Enter Food here ....",
            fg=CREAM,
            bg=STONE,
            font=("Sans", 18),
            wraplength=900,
            justify="left",
        ).pack(anchor="w", padx=18, pady=(16, 8))

        self.extra2_frame = self.make_panel(root, "Loops", GOLD, 3)
        self.extra2_frame.pack(fill="x", padx=26, pady=(8, 14))
        tk.Label(
            self.extra2_frame.body,
            text="No loops today or tomorrow.\nTo view and sign up for loops please go to loops.ncssm.edu/loops",
            fg=CREAM,
            bg=STONE,
            font=("Sans", 18),
            wraplength=900,
            justify="left",
        ).pack(anchor="w", padx=18, pady=(16, 8))

        self.update_ui()

    def make_panel(self, parent, title, accent, step):
        outer = tk.Frame(parent, bg=BORDER, highlightthickness=0)
        inner = tk.Frame(outer, bg=STONE, highlightbackground=accent, highlightthickness=2)
        inner.pack(fill="both", expand=True, padx=6, pady=6)

        header = tk.Frame(inner, bg=accent, height=48)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_wrap = tk.Frame(header, bg=accent)
        title_wrap.pack(fill="both", expand=True)
        tk.Label(
            title_wrap,
            text=title,
            fg="white",
            bg=accent,
            font=("Sans", 22, "bold"),
        ).pack(anchor="w", padx=16, pady=8)

        # simple stepped pattern for a temple feel
        pattern = tk.Frame(header, bg=accent)
        pattern.pack(side="right", padx=12)
        for i in range(3):
            size = 8 + (i * 4)
            tk.Frame(pattern, bg=BG, width=size, height=4).grid(row=0, column=i, padx=1)
            tk.Frame(pattern, bg=BG, width=size, height=4).grid(row=1, column=i, padx=1, pady=(2,0))

        body = tk.Frame(inner, bg=STONE, height=step * 10 + 160)
        body.pack(fill="x")
        body.pack_propagate(False)

        outer.body = body
        return outer

    def add_bullet(self, parent, text, fg):
        row = tk.Frame(parent, bg=STONE)
        row.pack(fill="x", padx=18, pady=6)
        tk.Label(row, text="▣", fg=GOLD, bg=STONE, font=("Sans", 16, "bold")).pack(side="left", padx=(0, 10))
        tk.Label(row, text=text, fg=fg, bg=STONE, font=("Sans", 18), wraplength=900, justify="left").pack(side="left", anchor="w")

    def update_ui(self):
        now = datetime.now()
        self.time_label.config(text=now.strftime("%A, %b %d  •  %I:%M %p"))
        try:
            self.block_label.config(text=bdb.status_text())
        except Exception:
            self.block_label.config(text="Schedule unavailable.")
        self.after(1000, self.update_ui)

if __name__ == "__main__":
    App().mainloop()

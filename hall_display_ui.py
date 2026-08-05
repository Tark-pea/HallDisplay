#!/usr/bin/env python3
import tkinter as tk
from datetime import datetime
import block_display_bot as bdb

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hall Display")
        self.configure(bg="#111111")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())

        self.time_label = tk.Label(self, fg="white", bg="#111111", font=("Sans", 42, "bold"))
        self.time_label.pack(pady=(20, 10))

        self.block_label = tk.Label(self, fg="#c1296d", bg="#111111", font=("Sans", 34, "bold"), wraplength=1100, justify="center")
        self.block_label.pack(pady=(10, 40))

        self.box1 = tk.Frame(self, bg="#1b1b1b", highlightbackground="#333333", highlightthickness=2, width=1000, height=640)
        self.box1.pack(pady=20)
        self.box1.pack_propagate(False)
        tk.Label(self.box1, text="Important things:", fg="white", bg="#1b1b1b", font=("Sans", 24, "bold")).pack(anchor="w", padx=20, pady=(15, 0))
        tk.Label(self.box1, text="• Welcome Juniors!", fg="#cccccc", bg="#1b1b1b", font=("Sans", 18)).pack(anchor="w", padx=20, pady=10)
        tk.Label(self.box1, text="• And Welcome Back Seniors!", fg="#cccccc", bg="#1b1b1b", font=("Sans", 18)).pack(anchor="w", padx=20, pady=10)
        tk.Label(self.box1, text="• To Those New Here, Welcome To The Best Hall On Campus!", fg="#cccccc", bg="#1b1b1b", font=("Sans", 18)).pack(anchor="w", padx=20, pady=10)

        self.box2 = tk.Frame(self, bg="#1b1b1b", highlightbackground="#333333", highlightthickness=2, width=1000, height=640)
        self.box2.pack(pady=20)
        self.box2.pack_propagate(False)
        tk.Label(self.box2, text="", fg="white", bg="#1b1b1b", font=("Sans", 24, "bold")).pack(anchor="w", padx=20, pady=(15, 0))

        self.update_ui()

    def update_ui(self):
        now = datetime.now()
        self.time_label.config(text=now.strftime("%A, %b %d  •  %I:%M %p"))
        self.block_label.config(text=bdb.main())
        self.after(1000, self.update_ui)

if __name__ == "__main__":
    App().mainloop()

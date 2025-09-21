import time
from dataclasses import dataclass, field
from typing import List

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

@dataclass
class LPStats:
    total_levels: int
    start_times: List[float] = field(default_factory=list)
    elapsed: List[float] = field(default_factory=list)
    attempts: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.start_times = [0.0] * (self.total_levels + 1)
        self.elapsed = [0.0] * (self.total_levels + 1)
        self.attempts = [0] * (self.total_levels + 1)

    def start_level(self, level: int):
        self.start_times[level] = time.perf_counter()
        self.attempts[level] += 1

    def finish_level(self, level: int) -> float:
        dt = time.perf_counter() - self.start_times[level]
        self.elapsed[level] = dt
        return dt

    def as_dict(self):
        return {"elapsed": self.elapsed, "attempts": self.attempts, "total": self.total_levels}

    def from_dict(self, d: dict):
        self.total_levels = int(d.get("total", self.total_levels))
        self.elapsed = d.get("elapsed", self.elapsed)
        self.attempts = d.get("attempts", self.attempts)

def lp_show_stats_window(parent, stats: LPStats):
    import tkinter as tk
    from tkinter import ttk

    win = tk.Toplevel(parent)
    win.title("Statisztika")
    win.geometry("640x420")

    fig = Figure(figsize=(6.0, 3.2), dpi=100)
    ax = fig.add_subplot(111)

    levels = list(range(1, stats.total_levels + 1))
    times = [max(0.0, float(stats.elapsed[i])) for i in levels]

    ax.bar(levels, times)
    ax.set_title("Szintidők (s)")
    ax.set_xlabel("Szint")
    ax.set_ylabel("Idő [s]")
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    frm = ttk.Frame(win)
    frm.pack(fill=tk.X)
    ttk.Label(frm, text=f"Kísérletek: {[stats.attempts[i] for i in levels]}").pack(padx=8, pady=8, anchor="w")

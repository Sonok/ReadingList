#!/usr/bin/env python3
"""Render progress.png and the README progress table from progress.csv.

progress.csv rows: date,book,done,total. Units are pages. The green book baseline (30 of 191 as of 2026-10-03) is an
estimate from problems done in ch 2 and 4 plus ch 1 and 3.1; forward progress is logged by page.
Run after appending a row:  python3 scripts/plot_progress.py
"""
import csv
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
CSV, PNG, README = ROOT / "progress.csv", ROOT / "progress.png", ROOT / "README.md"

# Fixed categorical order and hue per book; never reassigned when a book is added or finished.
BOOKS = [
    ("K&R", "#2a78d6", "pages"),
    ("A Tour of C++", "#eb6834", "pages"),
    ("Green book", "#1baf7a", "pages"),
    ("DDIA", "#eda100", "pages"),
]
TEXT, TEXT2, GRID = "#1f1f1e", "#5f5e58", "#e6e5e0"

series = defaultdict(list)
with CSV.open() as f:
    for row in csv.DictReader(f):
        series[row["book"]].append((date.fromisoformat(row["date"]), int(row["done"]), int(row["total"])))
for v in series.values():
    v.sort()

today = date.today()
fig, ax = plt.subplots(figsize=(9, 4.2), dpi=160)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
for name, color, _ in BOOKS:
    pts = series.get(name)
    if not pts:
        continue
    xs = [p[0] for p in pts] + [today]
    ys = [100 * p[1] / p[2] for p in pts]
    ys.append(ys[-1])  # carry the latest value to today
    ax.plot(xs, ys, color=color, lw=2, solid_joinstyle="round", solid_capstyle="round", label=name)
    ax.plot([p[0] for p in pts], ys[:-1], "o", color=color, ms=5, mec="white", mew=1.5)
    ax.annotate(f"{name}  {ys[-1]:.0f}%", (today, ys[-1]), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=9, color=TEXT)

top = max(100 * p[-1][1] / p[-1][2] for p in series.values())
ax.set_ylim(0, min(100, (int(top // 10) + 2) * 10))  # headroom above the leader; grows toward 100 as books finish
ax.set_ylabel("% complete", color=TEXT2, fontsize=9)
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.grid(axis="y", color=GRID, lw=1)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(GRID)
ax.tick_params(colors=TEXT2, labelsize=8.5, length=0)
ax.legend(loc="upper left", frameon=False, fontsize=8.5, labelcolor=TEXT)
ax.set_title("Tier 1 and 2 books in progress", loc="left", fontsize=11, color=TEXT, pad=10)
fig.tight_layout()
fig.subplots_adjust(right=0.80)
fig.savefig(PNG, facecolor="white")

# README table between markers.
rows = ["| Book | Progress | | Unit |", "|---|---|---|---|"]
for name, _, unit in BOOKS:
    pts = series.get(name)
    if not pts:
        continue
    d, done, total = pts[-1]
    pct = 100 * done / total
    bar = "█" * round(pct / 5) + "░" * (20 - round(pct / 5))
    rows.append(f"| {name} | `{bar}` | {pct:.0f}% | {done} of {total} {unit} |")
block = "\n".join(rows)
text = README.read_text()
new = re.sub(r"(<!-- progress:start -->\n).*?(<!-- progress:end -->)", lambda m: m.group(1) + block + "\n" + m.group(2), text, flags=re.S)
if new != text:
    README.write_text(new)
print(block)

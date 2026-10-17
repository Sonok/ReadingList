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
# Green book (#1baf7a) was removed 2026-10-11; its hue went to Putnam Guide.
BOOKS = [
    ("K&R", "#2a78d6", "pages"),
    ("A Tour of C++", "#eb6834", "pages"),
    ("CP Handbook", "#9a5bd9", "pages"),  # 279-page copy; read from the start, baseline page 24 (corrected 2026-10-16)
    ("DDIA", "#eda100", "pages"),
    ("Putnam Guide ch 1", "#1baf7a", "items"),
    ("Quant Primer", "#d6336c", "pages"),  # Bester, An Interview Primer for Quantitative Finance, 92 pages  # 1 definition + 5 theorems + 13 examples + 1 strategies section + 52 exercises
]
TEXT, TEXT2, GRID = "#1f1f1e", "#5f5e58", "#e6e5e0"

series = defaultdict(list)
with CSV.open() as f:
    for row in csv.DictReader(f):
        series[row["book"]].append((date.fromisoformat(row["date"]), int(row["done"]), int(row["total"])))
for k, v in series.items():
    # One point per day: keep the highest value logged that day.
    byday = {}
    for d, done, total in v:
        if d not in byday or done > byday[d][0]:
            byday[d] = (done, total)
    series[k] = sorted((d, done, total) for d, (done, total) in byday.items())

today = date.today()
ends = []  # (y, label, color) for end labels, placed after the axes are scaled
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
    ends.append((ys[-1], f"{name}  {ys[-1]:.0f}%", color))

top = max(100 * p[-1][1] / p[-1][2] for p in series.values())
ax.set_ylim(0, min(100, (int(top // 10) + 2) * 10))  # headroom above the leader; grows toward 100 as books finish
# End labels: sort by value, push apart to a minimum gap, and connect displaced ones to the line end with a leader.
ymax = ax.get_ylim()[1]
gap = ymax * 0.07
ends.sort()
placed = []
for y, _, _ in ends:
    placed.append(y if not placed else max(y, placed[-1] + gap))
x0, x1 = ax.get_xlim()  # matplotlib date numbers (float days)
xt = mdates.date2num(today)
dx = (x1 - x0) * 0.045
for (y, label, color), ly in zip(ends, placed):
    if abs(ly - y) > 1e-9:
        ax.plot([xt, xt + dx], [y, ly], color=color, lw=1, clip_on=False, solid_capstyle="round")
    ax.text(xt + dx * 1.15, ly, label, va="center", fontsize=9, color=TEXT, clip_on=False)
ax.set_xlim(x0, x1)
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

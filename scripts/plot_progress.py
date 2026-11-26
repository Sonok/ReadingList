#!/usr/bin/env python3
"""Render progress.png, the interactive index.html, and the README progress table from progress.csv.

progress.csv rows: date,book,done,total. Units per book are in BOOKS below (pages, items, or questions). The green book baseline (30 of 191 as of 2026-10-03) is an
estimate from problems done in ch 2 and 4 plus ch 1 and 3.1; forward progress is logged by page.
Run after appending a row:  python3 scripts/plot_progress.py
"""
import csv
import html
import json
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
LOG, PAGE, TEMPLATE = ROOT / "log.md", ROOT / "index.html", ROOT / "scripts" / "chart_template.html"
# log.md section heading for each charted book, used to attach that day's note to its point on the interactive chart.
LOG_HEADINGS = {
    "The C Programming Language (K&R)": "K&R",
    "A Tour of C++": "A Tour of C++",
    "Competitive Programmer's Handbook": "CP Handbook",
    "Designing Data-Intensive Applications": "DDIA",
    "An Interview Primer for Quantitative Finance": "Quant Primer",
}

# Fixed categorical order and hue per book; never reassigned when a book is added or finished.
# Hue #1baf7a belonged to a book since removed; leave it unused.
BOOKS = [
    ("K&R", "#2a78d6", "pages"),
    ("A Tour of C++", "#eb6834", "pages"),
    ("CP Handbook", "#9a5bd9", "pages"),  # 279-page copy; read from the start, baseline page 24 (corrected 2026-10-16)
    ("DDIA", "#eda100", "pages"),
    ("Quant Primer", "#d6336c", "items"),  # Bester, An Interview Primer for Quantitative Finance: 39 questions (41 numbered minus R questions 3 and 36) + 19 reading sections = 58 items (switched from 92 pages on 2026-10-18)
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
plt.rcParams["font.family"] = ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]
fig, ax = plt.subplots(figsize=(9, 4.6), dpi=200)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
handles, labels, latest = [], [], {}
for name, color, _ in BOOKS:
    pts = series.get(name)
    if not pts:
        continue
    xs = [p[0] for p in pts] + [today]
    ys = [100 * p[1] / p[2] for p in pts]
    ys.append(ys[-1])  # carry the latest value to today
    latest[name] = ys[-1]
    ax.plot(xs, ys, color=color, lw=2, solid_joinstyle="round", solid_capstyle="round", zorder=3)
    # One marker per series, at its current value, ringed in the surface color so overlapping ends stay legible.
    (dot,) = ax.plot([today], [ys[-1]], "o", color=color, ms=7.5, mec="white", mew=2, zorder=4, clip_on=False)
    handles.append(dot)
    labels.append(f"{name}  {ys[-1]:.0f}%")

# The leader gets a value label at its line end; the legend row carries every book's value.
leader = max(latest, key=latest.get)
top = latest[leader]
ax.set_ylim(0, min(100, (int(top // 10) + 2) * 10))  # headroom above the leader; grows toward 100 as books finish
x0, x1 = ax.get_xlim()  # matplotlib date numbers (float days)
xt = mdates.date2num(today)
ax.set_xlim(x0, xt + (xt - x0) * 0.07)
ax.annotate(f"{top:.0f}%", (xt, top), xytext=(9, 0), textcoords="offset points", va="center",
            fontsize=11, fontweight="bold", color=TEXT, annotation_clip=False)

ax.yaxis.set_major_locator(plt.MultipleLocator(10 if ax.get_ylim()[1] <= 60 else 20))
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %-d"))
ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(colors=TEXT2, labelsize=9, length=0, pad=6)

fig.subplots_adjust(left=0.065, right=0.965, top=0.74, bottom=0.09)
fig.text(0.02, 0.94, "Reading progress", fontsize=14, fontweight="bold", color=TEXT, va="center")
fig.text(0.02, 0.875, "Percent of each book complete", fontsize=10, color=TEXT2, va="center")
fig.legend(handles, labels, loc="center left", bbox_to_anchor=(0.008, 0.795), ncol=len(handles), frameon=False,
           fontsize=9.5, labelcolor=TEXT, handletextpad=0.2, columnspacing=1.6, borderaxespad=0, borderpad=0)
fig.savefig(PNG, facecolor="white")

# Interactive page: the same series plus each day's note from log.md, injected into the template.
notes, book = defaultdict(dict), None
for line in LOG.read_text().splitlines():
    if line.startswith("## "):
        book = LOG_HEADINGS.get(line[3:].strip())
    elif book and (m := re.match(r"- (\d{4}-\d{2}-\d{2}): (.*)", line)):
        notes[book][m.group(1)] = m.group(2)
payload = {"today": today.isoformat(), "books": [
    {"name": name, "color": color, "unit": unit, "points": [
        {"d": d.isoformat(), "done": done, "total": total, "note": html.escape(notes[name].get(d.isoformat(), ""))}
        for d, done, total in series.get(name, [])]}
    for name, color, unit in BOOKS]}
for b in payload["books"]:
    b["name"] = html.escape(b["name"])
PAGE.write_text(TEMPLATE.read_text().replace("/*DATA*/", json.dumps(payload).replace("</", "<\\/")))

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

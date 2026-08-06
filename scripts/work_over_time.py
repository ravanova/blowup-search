#!/usr/bin/env python3
"""Regenerate the work-over-time chart from git history.

`legs_over_time.py` plots each leg once, at its FIRST commit, so a leg that runs
for three hours is a single point and the curve reads flat while real work is
happening. This script measures the work itself: every non-merge commit on the
branch, binned in time, split by what it was and how much it moved.

Three shared-x panels:
  1. commits per bin, split leg work vs orchestration (the `Leg 0:` DM/ORCH/BENCH
     commits, plus the handful of unlabelled ones)
  2. distinct legs committing per bin -- how many agents were actually in flight
  3. lines changed per bin, split hand-authored vs curated JSON

Lines changed is reported split because it is otherwise a misleading number:
the curated evidence JSON under writeup/data/ is machine-emitted and dominates
any raw total. Panel 3 shows that rather than hiding it.

Usage:
    scripts/work_over_time.py                       # writes reports/work_over_time.html
    scripts/work_over_time.py --bin 30              # bin width in minutes (default: 15)
    scripts/work_over_time.py --rev main            # which history to measure (default: main)
    scripts/work_over_time.py -o some/path.html
"""
import argparse
import html
import json
import re
import subprocess
from datetime import datetime, timezone

LEG_RE = re.compile(r"^Leg (\d+):")


def is_generated(path):
    """Curated evidence blobs -- emitted by a runner, not typed by anyone."""
    return path.startswith("writeup/data/") or path.endswith(".json")


def commit_rows(repo_root, rev):
    raw = subprocess.run(
        ["git", "log", rev, "--no-merges", "--numstat", "-M",
         "--pretty=format:@@|%H|%ad|%s", "--date=iso-strict"],
        cwd=repo_root, capture_output=True, text=True, check=True,
    ).stdout
    rows, cur = [], None
    for line in raw.splitlines():
        if line.startswith("@@|"):
            _, sha, ts, subject = line.split("|", 3)
            m = LEG_RE.match(subject)
            cur = {
                "sha": sha,
                "t": datetime.fromisoformat(ts),
                "subject": subject,
                "leg": int(m.group(1)) if m else None,
                "hand": 0,
                "gen": 0,
            }
            rows.append(cur)
        elif line.strip() and cur is not None:
            parts = line.split("\t")
            if len(parts) == 3 and parts[0].isdigit():
                moved = int(parts[0]) + int(parts[1])
                if is_generated(parts[2]):
                    cur["gen"] += moved
                else:
                    cur["hand"] += moved
    rows.sort(key=lambda c: c["t"])
    return rows


def build_bins(rows, bin_minutes):
    """Bin from the first numbered leg onward; earlier history predates the run."""
    numbered = [c for c in rows if c["leg"]]
    if not numbered:
        raise SystemExit("No 'Leg N:' commits found in git history.")
    start = numbered[0]["t"]
    run = [c for c in rows if c["t"] >= start]

    step = bin_minutes * 60
    floor = int(start.timestamp()) // step * step
    last = int(run[-1]["t"].timestamp())

    bins = {}
    b = floor
    while b <= last:
        bins[b] = {"t": b, "leg": 0, "orch": 0, "hand": 0, "gen": 0, "legs": set()}
        b += step

    for c in run:
        d = bins[int(c["t"].timestamp()) // step * step]
        if c["leg"]:
            d["leg"] += 1
            d["legs"].add(c["leg"])
        else:
            d["orch"] += 1          # Leg 0 (DM/ORCH/BENCH) and unlabelled commits
        d["hand"] += c["hand"]
        d["gen"] += c["gen"]

    series = []
    for b in sorted(bins):
        d = bins[b]
        series.append({
            "t": d["t"] * 1000,
            "leg": d["leg"],
            "orch": d["orch"],
            "par": len(d["legs"]),
            "hand": d["hand"],
            "gen": d["gen"],
        })
    return series, run


def hourly_table(series, bin_minutes):
    per_hour = {}
    for d in series:
        h = d["t"] // 3600000 * 3600000
        e = per_hour.setdefault(h, {"t": h, "leg": 0, "orch": 0, "par": 0, "hand": 0, "gen": 0})
        e["leg"] += d["leg"]
        e["orch"] += d["orch"]
        e["par"] = max(e["par"], d["par"])
        e["hand"] += d["hand"]
        e["gen"] += d["gen"]
    return [per_hour[k] for k in sorted(per_hour)]


TEMPLATE = r"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Work over time</title>
<style>
.viz-root {
  color-scheme: light;
  --surface-1:      #fcfcfb;
  --page:           #f9f9f7;
  --text-primary:   #0b0b0b;
  --text-secondary: #52514e;
  --text-muted:     #898781;
  --grid:           #e1e0d9;
  --baseline:       #c3c2b7;
  --series-1:       #2a78d6;
  --series-2:       #eb6834;
  --ballast:        #cdccc2;
  --band:           rgba(11,11,11,0.028);
  --border:         rgba(11,11,11,0.10);
}
@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) .viz-root {
    color-scheme: dark;
    --surface-1:      #1a1a19;
    --page:           #0d0d0d;
    --text-primary:   #ffffff;
    --text-secondary: #c3c2b7;
    --text-muted:     #898781;
    --grid:           #2c2c2a;
    --baseline:       #383835;
    --series-1:       #3987e5;
    --series-2:       #d95926;
    --ballast:        #55544e;
    --band:           rgba(255,255,255,0.030);
    --border:         rgba(255,255,255,0.10);
  }
}
:root[data-theme="dark"] .viz-root {
  color-scheme: dark;
  --surface-1:      #1a1a19;
  --page:           #0d0d0d;
  --text-primary:   #ffffff;
  --text-secondary: #c3c2b7;
  --text-muted:     #898781;
  --grid:           #2c2c2a;
  --baseline:       #383835;
  --series-1:       #3987e5;
  --series-2:       #d95926;
  --ballast:        #55544e;
  --band:           rgba(255,255,255,0.030);
  --border:         rgba(255,255,255,0.10);
}
* { box-sizing: border-box; }
body { margin: 0; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
.viz-root { background: var(--page); color: var(--text-primary); min-height: 100vh; }
.wrap { max-width: 1040px; margin: 0 auto; padding: 32px 20px 48px; }
h1 { font-size: 1.15rem; font-weight: 600; margin: 0 0 4px; }
.subtitle { color: var(--text-secondary); font-size: 0.88rem; margin: 0 0 24px; max-width: 68ch; line-height: 1.5; }
.card { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 20px 20px 10px; }
.stats { display: flex; gap: 32px; flex-wrap: wrap; margin-bottom: 22px; }
.stat-label { font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em; }
.stat-value { font-size: 1.4rem; font-weight: 600; color: var(--text-primary); }
.stat-note { font-size: 0.72rem; color: var(--text-muted); margin-top: 1px; }
.legend { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; font-size: 0.8rem; color: var(--text-secondary); margin: 0 0 2px 2px; }
.legend span.k { display: inline-flex; align-items: center; gap: 6px; }
.sw { width: 10px; height: 10px; border-radius: 2px; }
.sw-1 { background: var(--series-1); }
.sw-2 { background: var(--series-2); }
.sw-b { background: var(--ballast); }
.chart-container { position: relative; }
svg { display: block; width: 100%; height: auto; overflow: visible; }
.axis-label { font-size: 11px; fill: var(--text-muted); }
.panel-title { font-size: 12px; font-weight: 600; fill: var(--text-secondary); }
.panel-unit { font-size: 11px; fill: var(--text-muted); }
.grid-line { stroke: var(--grid); stroke-width: 1; }
.baseline { stroke: var(--baseline); stroke-width: 1; }
.day-band { fill: var(--band); }
.day-divider { stroke: var(--baseline); stroke-width: 1; }
.day-label { font-size: 11px; font-weight: 600; fill: var(--text-secondary); }
.seg-1 { fill: var(--series-1); }
.seg-2 { fill: var(--series-2); }
.seg-b { fill: var(--ballast); }
.col-hit { fill: transparent; }
.col-hi { fill: var(--text-primary); opacity: 0; pointer-events: none; }
.col-hi.on { opacity: 0.06; }
#tooltip {
  position: absolute; pointer-events: none; background: var(--surface-1);
  border: 1px solid var(--border); border-radius: 8px; padding: 9px 11px;
  font-size: 12px; color: var(--text-primary); box-shadow: 0 4px 16px rgba(0,0,0,0.18);
  opacity: 0; transition: opacity 0.08s ease; white-space: nowrap; z-index: 10;
}
#tooltip .tt-title { font-weight: 600; margin-bottom: 5px; }
#tooltip table { border-collapse: collapse; font-variant-numeric: tabular-nums; }
#tooltip td { padding: 1px 0; }
#tooltip td.v { text-align: right; padding-left: 14px; color: var(--text-secondary); }
#tooltip td.k { color: var(--text-secondary); }
#tooltip .dot { display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: 6px; }
details { margin-top: 18px; }
summary { font-size: 0.82rem; color: var(--text-secondary); cursor: pointer; padding: 4px 0; }
summary:focus-visible { outline: 2px solid var(--series-1); outline-offset: 2px; border-radius: 3px; }
.tbl-scroll { overflow-x: auto; margin-top: 10px; }
table.data { border-collapse: collapse; font-size: 0.8rem; font-variant-numeric: tabular-nums; width: 100%; }
table.data th, table.data td { padding: 5px 10px; text-align: right; border-bottom: 1px solid var(--grid); white-space: nowrap; }
table.data th:first-child, table.data td:first-child { text-align: left; }
table.data th { color: var(--text-muted); font-weight: 600; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; }
.footnote { font-size: 0.76rem; color: var(--text-muted); margin: 14px 2px 0; line-height: 1.5; max-width: 74ch; }
@media (prefers-reduced-motion: reduce) { #tooltip { transition: none; } }
</style>
</head>
<body>
<div class="viz-root">
<div class="wrap">
  <h1>Work over time</h1>
  <p class="subtitle">Every non-merge commit on <code>__REV__</code> from the first numbered leg onward, in __BIN__-minute bins. The cumulative-legs chart counts each leg once, at its first commit, so it reads flat while a leg is still working; this counts the work. Generated by <code>scripts/work_over_time.py</code> on __GENERATED__.</p>

  <div class="card">
    <div class="stats">
      <div><div class="stat-label">Commits</div><div class="stat-value">__TOT_COMMITS__</div><div class="stat-note">__TOT_LEG__ leg &middot; __TOT_ORCH__ orchestration</div></div>
      <div><div class="stat-label">Peak legs in parallel</div><div class="stat-value">__PEAK_PAR__</div><div class="stat-note">in one __BIN__-min bin</div></div>
      <div><div class="stat-label">Hand-authored lines</div><div class="stat-value">__TOT_HAND__</div><div class="stat-note">plus __TOT_GEN__ curated JSON</div></div>
      <div><div class="stat-label">Bins with no commit</div><div class="stat-value">__IDLE_PCT__%</div><div class="stat-note">__IDLE_N__ of __NBINS__ bins</div></div>
    </div>

    <div class="legend">
      <span class="k"><span class="sw sw-1"></span>leg work</span>
      <span class="k"><span class="sw sw-2"></span>orchestration &amp; planning</span>
      <span class="k"><span class="sw sw-b"></span>curated JSON (machine-emitted)</span>
    </div>

    <div class="chart-container" id="chart-container">
      <svg id="chart" viewBox="0 0 1000 530" preserveAspectRatio="xMidYMid meet" role="img"
           aria-label="Three time-aligned panels: commits per bin, legs committing in parallel, and lines changed per bin."></svg>
      <div id="tooltip" role="status" aria-live="polite"></div>
    </div>

    <details>
      <summary>Table view &mdash; hourly totals</summary>
      <div class="tbl-scroll">
        <table class="data">
          <thead><tr><th>Hour</th><th>Leg commits</th><th>Orchestration</th><th>Peak parallel legs</th><th>Hand-authored lines</th><th>Curated JSON lines</th></tr></thead>
          <tbody id="tbody"></tbody>
        </table>
      </div>
    </details>
  </div>

  <p class="footnote">__FOOTNOTE__</p>
</div>
</div>

<script>
const data = __DATA_JSON__;
const hourly = __HOURLY_JSON__;
const binMs = __BIN_MS__;

const svg = document.getElementById('chart');
const NS = 'http://www.w3.org/2000/svg';
const W = 1000, H = 530;
// top band holds the day labels; each panel's own title sits just above its frame
const M = { top: 44, right: 20, bottom: 44, left: 56 };
const plotW = W - M.left - M.right;

// Three shared-x panels. Separate y-scales live in separate panels, never on one plot.
const panels = [
  { key: 'commits', title: 'Commits landed',            unit: 'per bin',   y: M.top,        h: 150 },
  { key: 'par',     title: 'Legs committing in parallel', unit: 'distinct legs', y: M.top + 184, h: 86 },
  { key: 'lines',   title: 'Lines changed',             unit: 'per bin',   y: M.top + 304, h: 138 },
];

const tMin = data[0].t;
const tMax = data[data.length - 1].t + binMs;
const xScale = t => M.left + ((t - tMin) / (tMax - tMin)) * plotW;
const barW = Math.max(plotW / data.length - 2, 1.5);

const maxCommits = Math.max(...data.map(d => d.leg + d.orch), 1);
const maxPar     = Math.max(...data.map(d => d.par), 1);
const maxLines   = Math.max(...data.map(d => d.hand + d.gen), 1);
const maxes = { commits: maxCommits, par: maxPar, lines: maxLines };

const el = (tag, attrs) => {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  return e;
};
const startOfDay = t => { const d = new Date(t); d.setHours(0, 0, 0, 0); return d.getTime(); };
const fmtDay  = t => new Date(t).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
const fmtTime = t => new Date(t).toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' });
const fmtInt  = n => n.toLocaleString();

// Top-rounded bar: 4px radius on the data end, square where it meets the baseline.
function barPath(x, y, w, h, r) {
  r = Math.max(0, Math.min(r, w / 2, h));
  return `M ${x},${y + h} L ${x},${y + r} Q ${x},${y} ${x + r},${y} `
       + `L ${x + w - r},${y} Q ${x + w},${y} ${x + w},${y + r} L ${x + w},${y + h} Z`;
}

// ---- day bands, drawn under everything -------------------------------------
const days = [];
for (let c = startOfDay(tMin); c <= tMax; c += 864e5) days.push(c);
days.forEach((dayStart, i) => {
  const x1 = xScale(Math.max(dayStart, tMin));
  const x2 = xScale(Math.min(dayStart + 864e5, tMax));
  if (i % 2 === 1) {
    panels.forEach(p => svg.appendChild(el('rect', {
      class: 'day-band', x: x1, y: p.y, width: Math.max(x2 - x1, 0), height: p.h })));
  }
  const label = el('text', { class: 'day-label', x: (x1 + x2) / 2, y: 15, 'text-anchor': 'middle' });
  label.textContent = fmtDay(Math.max(dayStart, tMin));
  svg.appendChild(label);
  if (i > 0) panels.forEach(p => svg.appendChild(el('line', {
    class: 'day-divider', x1, x2: x1, y1: p.y, y2: p.y + p.h })));
});

// ---- panel frames ----------------------------------------------------------
panels.forEach(p => {
  const yScale = v => p.y + p.h - (v / maxes[p.key]) * p.h;
  p.yScale = yScale;

  const ticks = 3;
  for (let i = 0; i <= ticks; i++) {
    const v = (maxes[p.key] / ticks) * i;
    const y = yScale(v);
    svg.appendChild(el('line', { class: 'grid-line', x1: M.left, x2: W - M.right, y1: y, y2: y }));
    const t = el('text', { class: 'axis-label', x: M.left - 10, y: y + 4, 'text-anchor': 'end' });
    t.textContent = maxes[p.key] >= 1000 ? Math.round(v / 1000) + 'k' : Math.round(v);
    svg.appendChild(t);
  }
  svg.appendChild(el('line', { class: 'baseline', x1: M.left, x2: W - M.right, y1: p.y + p.h, y2: p.y + p.h }));

  const title = el('text', { class: 'panel-title', x: M.left, y: p.y - 8 });
  title.textContent = p.title;
  svg.appendChild(title);
  // right-aligned, so it can never collide with the title however long that gets
  const unit = el('text', { class: 'panel-unit', x: W - M.right, y: p.y - 8, 'text-anchor': 'end' });
  unit.textContent = p.unit;
  svg.appendChild(unit);
});

// ---- marks -----------------------------------------------------------------
const GAP = 2;  // surface gap between stacked segments, per mark spec
data.forEach(d => {
  const x = xScale(d.t) + 1;

  // panel 1 — commits, stacked leg + orchestration
  const p1 = panels[0];
  let base = p1.y + p1.h;
  [['orch', 'seg-2'], ['leg', 'seg-1']].forEach(([key, cls], idx) => {
    if (!d[key]) return;
    const h = (d[key] / maxCommits) * p1.h;
    const top = base - h;
    const isTop = (key === 'leg') || !d.leg;
    svg.appendChild(el('path', { class: cls, d: barPath(x, top, barW, Math.max(h - (idx ? GAP : 0), 0.8), isTop ? 4 : 0) }));
    base = top - (idx ? GAP : 0);
  });

  // panel 2 — parallelism, single series
  const p2 = panels[1];
  if (d.par) {
    const h = (d.par / maxPar) * p2.h;
    svg.appendChild(el('path', { class: 'seg-1', d: barPath(x, p2.y + p2.h - h, barW, h, 4) }));
  }

  // panel 3 — lines changed, stacked hand-authored + curated JSON
  const p3 = panels[2];
  let b3 = p3.y + p3.h;
  [['gen', 'seg-b'], ['hand', 'seg-1']].forEach(([key, cls], idx) => {
    if (!d[key]) return;
    const h = (d[key] / maxLines) * p3.h;
    const top = b3 - h;
    const isTop = (key === 'hand') || !d.hand;
    svg.appendChild(el('path', { class: cls, d: barPath(x, top, barW, Math.max(h - (idx ? GAP : 0), 0.8), isTop ? 4 : 0) }));
    b3 = top - (idx ? GAP : 0);
  });
});

// ---- x axis ----------------------------------------------------------------
const HOUR = 36e5;
const span = tMax - tMin;
const step = [1, 2, 3, 4, 6, 8, 12, 24].map(h => h * HOUR).find(s => span / s <= 12) || 24 * HOUR;
const axisY = panels[2].y + panels[2].h;
for (let c = Math.ceil(tMin / step) * step; c <= tMax; c += step) {
  const x = xScale(c);
  const t = el('text', { class: 'axis-label', x: x, y: axisY + 20, 'text-anchor': 'middle' });
  t.textContent = fmtTime(c);
  svg.appendChild(t);
}
const xlab = el('text', { class: 'axis-label', x: M.left + plotW / 2, y: H - 6, 'text-anchor': 'middle' });
xlab.textContent = 'date & time';
svg.appendChild(xlab);

// ---- hover: one column, all three panels -----------------------------------
const tooltip = document.getElementById('tooltip');
const container = document.getElementById('chart-container');
const topY = panels[0].y, botY = panels[2].y + panels[2].h;

data.forEach(d => {
  const x = xScale(d.t);
  const hi = el('rect', { class: 'col-hi', x: x, y: topY, width: barW + 2, height: botY - topY });
  svg.appendChild(hi);
  const hit = el('rect', { class: 'col-hit', x: x - 1, y: topY, width: barW + 4, height: botY - topY });
  hit.addEventListener('mouseenter', () => {
    hi.classList.add('on');
    const rect = container.getBoundingClientRect();
    const sx = svg.getBoundingClientRect().width / W;
    const row = (sw, k, v) => `<tr><td class="k"><span class="dot" style="background:${sw}"></span>${k}</td><td class="v">${v}</td></tr>`;
    const cs = getComputedStyle(document.querySelector('.viz-root'));
    tooltip.innerHTML =
      `<div class="tt-title">${fmtDay(d.t)} ${fmtTime(d.t)}&ndash;${fmtTime(d.t + binMs)}</div><table>`
      + row(cs.getPropertyValue('--series-1'), 'leg commits', fmtInt(d.leg))
      + row(cs.getPropertyValue('--series-2'), 'orchestration', fmtInt(d.orch))
      + row(cs.getPropertyValue('--series-1'), 'legs in parallel', fmtInt(d.par))
      + row(cs.getPropertyValue('--series-1'), 'hand-authored lines', fmtInt(d.hand))
      + row(cs.getPropertyValue('--ballast'), 'curated JSON lines', fmtInt(d.gen))
      + `</table>`;
    tooltip.style.opacity = '1';
    let left = x * sx + 16;
    if (left + 230 > rect.width) left = x * sx - 230;
    tooltip.style.left = Math.max(0, left) + 'px';
    tooltip.style.top = '10px';
  });
  hit.addEventListener('mouseleave', () => { hi.classList.remove('on'); tooltip.style.opacity = '0'; });
  svg.appendChild(hit);
});

// ---- table view ------------------------------------------------------------
document.getElementById('tbody').innerHTML = hourly.map(h =>
  `<tr><td>${fmtDay(h.t)} ${fmtTime(h.t)}</td><td>${fmtInt(h.leg)}</td><td>${fmtInt(h.orch)}</td>`
  + `<td>${fmtInt(h.par)}</td><td>${fmtInt(h.hand)}</td><td>${fmtInt(h.gen)}</td></tr>`).join('');
</script>
</body>
</html>
"""


def render(series, hourly, rows, bin_minutes, rev):
    tot_leg = sum(d["leg"] for d in series)
    tot_orch = sum(d["orch"] for d in series)
    tot_hand = sum(d["hand"] for d in series)
    tot_gen = sum(d["gen"] for d in series)
    idle_n = sum(1 for d in series if d["leg"] + d["orch"] == 0)
    peak_par = max(d["par"] for d in series)

    gen_share = 100 * tot_gen / (tot_hand + tot_gen) if (tot_hand + tot_gen) else 0
    footnote = (
        f"Lines changed counts insertions plus deletions, with renames followed (<code>-M</code>). "
        f"Curated JSON is broken out because it is {gen_share:.0f}% of all lines moved and is emitted by "
        f"runners rather than authored, so a combined total would read as effort it does not represent. "
        f"Orchestration covers the <code>Leg 0:</code> DM/ORCH/BENCH commits and the few unlabelled ones. "
        f"Merge commits are excluded; only <code>{html.escape(rev)}</code> is measured, so work still "
        f"living on unmerged branches does not appear."
    )

    out = TEMPLATE
    for token, value in [
        ("__DATA_JSON__", json.dumps(series, separators=(",", ":"))),
        ("__HOURLY_JSON__", json.dumps(hourly, separators=(",", ":"))),
        ("__BIN_MS__", str(bin_minutes * 60 * 1000)),
        ("__BIN__", str(bin_minutes)),
        ("__REV__", html.escape(rev)),
        ("__GENERATED__", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
        ("__TOT_COMMITS__", f"{tot_leg + tot_orch:,}"),
        ("__TOT_LEG__", f"{tot_leg:,}"),
        ("__TOT_ORCH__", f"{tot_orch:,}"),
        ("__PEAK_PAR__", str(peak_par)),
        ("__TOT_HAND__", f"{tot_hand:,}"),
        ("__TOT_GEN__", f"{tot_gen:,}"),
        ("__IDLE_PCT__", f"{100 * idle_n / len(series):.0f}"),
        ("__IDLE_N__", str(idle_n)),
        ("__NBINS__", str(len(series))),
        ("__FOOTNOTE__", footnote),
    ]:
        out = out.replace(token, value)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-o", "--output", default="reports/work_over_time.html", help="output HTML path")
    parser.add_argument("--bin", type=int, default=15, help="bin width in minutes (default: 15)")
    parser.add_argument("--rev", default="main", help="history to measure (default: main)")
    parser.add_argument("--repo-root", default=".", help="git repo root (default: cwd)")
    args = parser.parse_args()

    rows = commit_rows(args.repo_root, args.rev)
    series, run = build_bins(rows, args.bin)
    hourly = hourly_table(series, args.bin)

    with open(args.output, "w") as f:
        f.write(render(series, hourly, run, args.bin, args.rev))

    print(f"Wrote {args.output} ({len(run)} commits, {len(series)} x {args.bin}min bins)")


if __name__ == "__main__":
    main()

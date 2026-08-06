#!/usr/bin/env python3
"""Regenerate the legs-over-time chart from git history.

Walks `git log` for commit subjects of the form "Leg N: ..." (the
ORCHESTRATION.md numbering scheme, which starts at leg 54 — everything
before that predates the convention and isn't numbered), takes each leg's
first commit timestamp as its landing time, and writes a self-contained
HTML chart (no external assets, works offline) to the output path.

Usage:
    scripts/legs_over_time.py                          # writes reports/legs_over_time.html
    scripts/legs_over_time.py --since 2026-08-01        # chart floor (default: 2026-08-01)
    scripts/legs_over_time.py -o some/other/path.html
"""
import argparse
import html
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone

LEG_RE = re.compile(r"^Leg (\d+):")


def leg_commits(repo_root):
    out = subprocess.run(
        ["git", "log", "--all", "--pretty=format:%ad|%s", "--date=iso-strict"],
        cwd=repo_root, capture_output=True, text=True, check=True,
    ).stdout
    by_leg = {}
    for line in out.splitlines():
        ts, _, subject = line.partition("|")
        m = LEG_RE.match(subject)
        if not m:
            continue
        leg = int(m.group(1))
        if leg == 0:
            continue  # Leg 0 = repo-wide/orchestrator commits, not a numbered leg
        t = datetime.fromisoformat(ts)
        if leg not in by_leg or t < by_leg[leg]:
            by_leg[leg] = t
    return sorted(by_leg.items(), key=lambda kv: kv[1])


def build_data(leg_times):
    return [
        {"leg": leg, "ts": t.isoformat(), "cum": i}
        for i, (leg, t) in enumerate(leg_times, start=1)
    ]


TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Legs completed over time</title>
<style>
.viz-root {{
  color-scheme: light;
  --surface-1:      #fcfcfb;
  --page:           #f9f9f7;
  --text-primary:   #0b0b0b;
  --text-secondary: #52514e;
  --text-muted:     #898781;
  --grid:           #e1e0d9;
  --baseline:       #c3c2b7;
  --series-1:       #2a78d6;
  --series-1-fill:  rgba(42,120,214,0.10);
  --border:         rgba(11,11,11,0.10);
}}
@media (prefers-color-scheme: dark) {{
  :root:where(:not([data-theme="light"])) .viz-root {{
    color-scheme: dark;
    --surface-1:      #1a1a19;
    --page:           #0d0d0d;
    --text-primary:   #ffffff;
    --text-secondary: #c3c2b7;
    --text-muted:     #898781;
    --grid:           #2c2c2a;
    --baseline:       #383835;
    --series-1:       #3987e5;
    --series-1-fill:  rgba(57,135,229,0.14);
    --border:         rgba(255,255,255,0.10);
  }}
}}
:root[data-theme="dark"] .viz-root {{
  color-scheme: dark;
  --surface-1:      #1a1a19;
  --page:           #0d0d0d;
  --text-primary:   #ffffff;
  --text-secondary: #c3c2b7;
  --text-muted:     #898781;
  --grid:           #2c2c2a;
  --baseline:       #383835;
  --series-1:       #3987e5;
  --series-1-fill:  rgba(57,135,229,0.14);
  --border:         rgba(255,255,255,0.10);
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--page); font-family: system-ui, -apple-system, "Segoe UI", sans-serif; color: var(--text-primary); }}
.wrap {{ max-width: 920px; margin: 0 auto; padding: 32px 20px 48px; }}
h1 {{ font-size: 1.15rem; font-weight: 600; margin: 0 0 4px; }}
.subtitle {{ color: var(--text-secondary); font-size: 0.88rem; margin: 0 0 24px; }}
.card {{ background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 20px 20px 8px; }}
.stats {{ display: flex; gap: 28px; flex-wrap: wrap; margin-bottom: 20px; }}
.stat-label {{ font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em; }}
.stat-value {{ font-size: 1.4rem; font-weight: 600; color: var(--text-primary); font-variant-numeric: tabular-nums; }}
svg {{ display: block; width: 100%; height: auto; overflow: visible; }}
.axis-label {{ font-size: 11px; fill: var(--text-muted); }}
.grid-line {{ stroke: var(--grid); stroke-width: 1; }}
.baseline {{ stroke: var(--baseline); stroke-width: 1; }}
.day-band-a {{ fill: var(--surface-1); }}
.day-band-b {{ fill: var(--grid); opacity: 0.35; }}
.day-divider {{ stroke: var(--baseline); stroke-width: 1; stroke-dasharray: 3 3; }}
.day-label {{ font-size: 11px; font-weight: 600; fill: var(--text-secondary); }}
.line-path {{ fill: none; stroke: var(--series-1); stroke-width: 2; stroke-linejoin: round; }}
.area-path {{ fill: var(--series-1-fill); }}
.dot {{ fill: var(--surface-1); stroke: var(--series-1); stroke-width: 1.6; }}
.dot.hot {{ fill: var(--series-1); }}
#tooltip {{
  position: absolute; pointer-events: none; background: var(--surface-1);
  border: 1px solid var(--border); border-radius: 8px; padding: 8px 10px;
  font-size: 12px; color: var(--text-primary); box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  opacity: 0; transition: opacity 0.08s ease; white-space: nowrap; z-index: 10;
}}
#tooltip .tt-title {{ font-weight: 600; margin-bottom: 2px; }}
#tooltip .tt-sub {{ color: var(--text-secondary); }}
.chart-container {{ position: relative; }}
.legend {{ display: flex; align-items: center; gap: 8px; font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 4px; }}
.legend-swatch {{ width: 10px; height: 10px; border-radius: 2px; background: var(--series-1); }}
</style>
</head>
<body>
<div class="viz-root">
<div class="wrap">
  <h1>Legs completed over time</h1>
  <p class="subtitle">Cumulative count of numbered legs ({leg_lo}–{leg_hi}) landed on <code>main</code>, plotted from {chart_floor_label} through the latest leg. Generated by <code>scripts/legs_over_time.py</code> on {generated_on}.</p>

  <div class="card">
    <div class="stats">
      <div><div class="stat-label">Chart span</div><div class="stat-value">{span_label}</div></div>
      <div><div class="stat-label">Legs landed</div><div class="stat-value">{leg_count}</div></div>
      <div><div class="stat-label">Leg-numbering window</div><div class="stat-value">{numbering_window}</div></div>
      <div><div class="stat-label">Gaps in numbering</div><div class="stat-value">{gaps_label}</div></div>
    </div>
    <div class="legend"><span class="legend-swatch"></span> cumulative legs landed</div>
    <div class="chart-container" id="chart-container">
      <svg id="chart" viewBox="0 0 880 440" preserveAspectRatio="xMidYMid meet"></svg>
      <div id="tooltip"></div>
    </div>
  </div>
</div>
</div>

<script>
const data = {data_json};
const chartFloor = {chart_floor_ms};

const svg = document.getElementById('chart');
const svgNS = 'http://www.w3.org/2000/svg';
const W = 880, H = 440;
const margin = {{ top: 28, right: 24, bottom: 46, left: 44 }};
const plotW = W - margin.left - margin.right;
const plotH = H - margin.top - margin.bottom;

data.forEach(d => {{ d.t = new Date(d.ts).getTime(); }});
const tMin = chartFloor;
const tMax = data[data.length - 1].t;
const yMax = data[data.length - 1].cum;

function xScale(t) {{ return margin.left + ((t - tMin) / (tMax - tMin)) * plotW; }}
function yScale(c) {{ return margin.top + plotH - (c / yMax) * plotH; }}

function el(tag, attrs) {{
  const e = document.createElementNS(svgNS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  return e;
}}
function dayKey(t) {{ const d = new Date(t); return `${{d.getFullYear()}}-${{d.getMonth()}}-${{d.getDate()}}`; }}
function startOfDay(t) {{ const d = new Date(t); d.setHours(0, 0, 0, 0); return d.getTime(); }}
function fmtDay(t) {{ return new Date(t).toLocaleDateString(undefined, {{ month: 'short', day: 'numeric' }}); }}
function fmtTime(t) {{ return new Date(t).toLocaleTimeString(undefined, {{ hour: 'numeric', minute: '2-digit' }}); }}

const days = [];
let cursor = startOfDay(tMin);
while (cursor <= tMax) {{ days.push(cursor); cursor += 24 * 3600 * 1000; }}

const activeDayKeys = new Set(data.map(d => dayKey(d.t)));
days.forEach((dayStart, i) => {{
  const bandStart = Math.max(dayStart, tMin);
  const bandEnd = Math.min(dayStart + 24 * 3600 * 1000, tMax);
  const x1 = xScale(bandStart);
  const x2 = xScale(bandEnd);
  svg.appendChild(el('rect', {{ class: i % 2 === 0 ? 'day-band-a' : 'day-band-b', x: x1, y: margin.top, width: Math.max(x2 - x1, 0), height: plotH }}));
  const isActive = activeDayKeys.has(dayKey(bandStart));
  if (isActive || i % 2 === 0) {{
    const label = el('text', {{ class: 'day-label', x: (x1 + x2) / 2, y: margin.top - 10, 'text-anchor': 'middle' }});
    label.textContent = fmtDay(bandStart);
    svg.appendChild(label);
  }}
  if (i > 0) svg.appendChild(el('line', {{ class: 'day-divider', x1, x2: x1, y1: margin.top, y2: margin.top + plotH }}));
}});

const yTicks = 5;
for (let i = 0; i <= yTicks; i++) {{
  const v = Math.round((yMax / yTicks) * i);
  const y = yScale(v);
  svg.appendChild(el('line', {{ class: 'grid-line', x1: margin.left, x2: W - margin.right, y1: y, y2: y }}));
  const t = el('text', {{ class: 'axis-label', x: margin.left - 10, y: y + 4, 'text-anchor': 'end' }});
  t.textContent = v;
  svg.appendChild(t);
}}

const legsStart = data[0].t;
const dayTickStepMs = 2 * 24 * 3600 * 1000;
let dayTickCursor = startOfDay(tMin);
for (; dayTickCursor < startOfDay(legsStart); dayTickCursor += dayTickStepMs) {{
  const x = xScale(dayTickCursor);
  const t = el('text', {{ class: 'axis-label', x: x, y: H - margin.bottom + 20, 'text-anchor': 'middle' }});
  t.textContent = fmtDay(dayTickCursor);
  svg.appendChild(t);
}}
const tickStepMs = 2 * 3600 * 1000;
let tickCursor = Math.ceil(startOfDay(legsStart) / tickStepMs) * tickStepMs;
for (; tickCursor <= tMax; tickCursor += tickStepMs) {{
  const x = xScale(tickCursor);
  const t = el('text', {{ class: 'axis-label', x: x, y: H - margin.bottom + 20, 'text-anchor': 'middle' }});
  t.textContent = fmtTime(tickCursor);
  svg.appendChild(t);
}}
const xAxisLabel = el('text', {{ class: 'axis-label', x: margin.left + plotW / 2, y: H - 4, 'text-anchor': 'middle' }});
xAxisLabel.textContent = 'date & time';
svg.appendChild(xAxisLabel);

svg.appendChild(el('line', {{ class: 'baseline', x1: margin.left, x2: W - margin.right, y1: margin.top + plotH, y2: margin.top + plotH }}));

let stepPts = [[margin.left, yScale(0)]];
data.forEach((d, i) => {{
  const x = xScale(d.t);
  const y = yScale(d.cum);
  const prevY = i === 0 ? yScale(0) : yScale(data[i - 1].cum);
  stepPts.push([x, prevY]);
  stepPts.push([x, y]);
}});
stepPts.push([W - margin.right, yScale(data[data.length - 1].cum)]);
const linePath = 'M ' + stepPts.map(p => p.join(',')).join(' L ');
const areaPath = linePath + ` L ${{W - margin.right}},${{margin.top + plotH}} L ${{margin.left}},${{margin.top + plotH}} Z`;
svg.appendChild(el('path', {{ class: 'area-path', d: areaPath }}));
svg.appendChild(el('path', {{ class: 'line-path', d: linePath }}));

const tooltip = document.getElementById('tooltip');
const container = document.getElementById('chart-container');
data.forEach(d => {{
  const x = xScale(d.t);
  const y = yScale(d.cum);
  const dot = el('circle', {{ class: 'dot', cx: x, cy: y, r: 3.2 }});
  svg.appendChild(dot);
  const hit = el('circle', {{ cx: x, cy: y, r: 9, fill: 'transparent' }});
  hit.addEventListener('mouseenter', () => {{
    dot.classList.add('hot');
    dot.setAttribute('r', 4.5);
    const rect = container.getBoundingClientRect();
    const svgRect = svg.getBoundingClientRect();
    const scaleX = svgRect.width / W;
    const scaleY = svgRect.height / H;
    tooltip.innerHTML = `<div class="tt-title">Leg ${{d.leg}} — #${{d.cum}} landed</div><div class="tt-sub">${{d.ts.replace('T', ' ').slice(0, 16)}}</div>`;
    tooltip.style.opacity = '1';
    let left = (x * scaleX) + 14;
    let top = (y * scaleY) - 10;
    if (left + 160 > rect.width) left = (x * scaleX) - 160;
    tooltip.style.left = left + 'px';
    tooltip.style.top = top + 'px';
  }});
  hit.addEventListener('mouseleave', () => {{
    dot.classList.remove('hot');
    dot.setAttribute('r', 3.2);
    tooltip.style.opacity = '0';
  }});
  svg.appendChild(hit);
}});
</script>
</body>
</html>
"""


def render(leg_times, chart_floor):
    data = build_data(leg_times)
    legs = [leg for leg, _ in leg_times]
    lo, hi = min(legs), max(legs)
    expected = set(range(lo, hi + 1))
    gaps = sorted(expected - set(legs))
    gaps_label = ", ".join(str(g) for g in gaps) if gaps else "none"

    first_t, last_t = leg_times[0][1], leg_times[-1][1]
    window = last_t - first_t
    hours, rem = divmod(int(window.total_seconds()), 3600)
    minutes = rem // 60
    numbering_window = f"{hours}h {minutes}m"

    span_label = f"{chart_floor.strftime('%b %-d')} – {last_t.strftime('%b %-d')}"

    return TEMPLATE.format(
        leg_lo=lo,
        leg_hi=hi,
        chart_floor_label=html.escape(chart_floor.strftime("%b %-d, %Y")),
        generated_on=html.escape(datetime.now(timezone.utc).strftime("%Y-%m-%d")),
        span_label=html.escape(span_label),
        leg_count=len(leg_times),
        numbering_window=numbering_window,
        gaps_label=html.escape(gaps_label),
        data_json=json.dumps(data),
        chart_floor_ms=int(chart_floor.timestamp() * 1000),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-o", "--output", default="reports/legs_over_time.html", help="output HTML path")
    parser.add_argument("--since", default="2026-08-01", help="chart x-axis floor, YYYY-MM-DD (default: 2026-08-01)")
    parser.add_argument("--repo-root", default=".", help="git repo root (default: cwd)")
    args = parser.parse_args()

    leg_times = leg_commits(args.repo_root)
    if not leg_times:
        raise SystemExit("No 'Leg N:' commits found in git history.")

    tz = leg_times[0][1].tzinfo
    chart_floor = datetime.fromisoformat(args.since).replace(tzinfo=tz)

    html_out = render(leg_times, chart_floor)
    with open(args.output, "w") as f:
        f.write(html_out)
    print(f"Wrote {args.output} ({len(leg_times)} legs, {leg_times[0][0]}–{leg_times[-1][0]})")


if __name__ == "__main__":
    main()

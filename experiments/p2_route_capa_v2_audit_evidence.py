"""fig67 -- Route-CAPA v2 (leg 292): rebuild the audit figure from the curated JSON.

`writeup/build_figures.py` runs every registered evidence script with NO arguments, so
the registered entry point must be cheap and side-effect-free.  The audit itself is not:
`experiments/p2_route_capa_v2_audit.py` executes all 46 cited test files and costs hours
of wall time.  This script therefore does the one thing the figure build needs -- read
the banked `writeup/data/p2_route_capa_v2_audit.json` and re-render
`writeup/figures/fig67_route_capa_v2_audit.png` -- and never re-runs the sweep.

To regenerate the DATA (not just the figure):
    .venv/bin/python experiments/p2_route_capa_v2_audit.py --workers 2
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))

from p2_route_capa_v2_audit import DATA, make_figure  # noqa: E402

import json  # noqa: E402


def main() -> int:
    if not DATA.exists():
        print(f"  SKIP fig67: {DATA} not present -- run the audit first")
        return 0
    make_figure(json.loads(DATA.read_text()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

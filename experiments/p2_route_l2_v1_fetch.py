#!/usr/bin/env python3
"""Leg 397 (unit L2') -- STEP 2 of 3: pull the full texts named in SS2.3 and extract them.

Papers/ is gitignored on purpose; this script is the committed record of WHICH full
texts were pulled and what their md5s were, so the quote-relocation in step 3 is
reproducible without committing third-party PDFs.

Every fetch is banked with its HTTP status and md5.  A fetch that fails is banked
`UNREACHABLE` with its reason -- never silently dropped and never a zero (SS2.2).

    python3 experiments/p2_route_l2_v1_fetch.py [arxiv_id ...]
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPERS = ROOT / "Papers"
OUT = ROOT / "writeup" / "data" / "p2_route_l2_fulltext_v1.json"

# SS2.3's families -> the reachable primary texts.  Journal-only pre-arXiv sources
# (Necas-Ruzicka-Sverak 1996 Acta Math.; Tsai 1998 ARMA; Bogovskii 1979 Dokl.;
# Giga-Kohn 1985/1987 CPAM) are declared UNREACHABLE at primary text IN ADVANCE by
# SS2.1 and appear here only through a reachable SECONDARY that states them verbatim.
WANTED = [
    ("1610.09464", "F2", "Chae-Wolf, Removing discretely self-similar singularities for the 3D Navier-Stokes equations"),
    ("2202.08352", "F2", "Bradshaw-Tsai, Spatial decay of discretely self-similar solutions to the Navier-Stokes equations"),
    ("2409.13586", "F2", "Asymptotic properties of discretely self-similar Navier-Stokes solutions with rough data"),
    ("2006.15776", "F1", "Leray's backward self-similar solutions of the 3D Navier-Stokes equations in Morrey spaces (SECONDARY for NRS/Tsai)"),
    ("2607.09619", "F1", "On rotated backwards self-similar solutions of the incompressible 3D Navier-Stokes equations"),
    ("1204.0529",  "F3", "Jia-Sverak, Local-in-space estimates near initial time ... and forward self-similar solutions"),
    ("1210.2783",  "F3", "Bradshaw-Tsai, Forward discretely self-similar solutions of the Navier-Stokes equations"),
    ("1703.03480", "F3", "Discretely self-similar solutions to the Navier-Stokes equations with Besov space data"),
    # CORRECTION made during the run and left visible: 1910.00173 is CHEN-HOU, not Elgindi.
    # Elgindi's own C^{1,alpha} paper is 1904.04795 and is fetched separately below.
    ("1910.00173", "F4", "Chen-Hou, Finite time blowup of 2D Boussinesq and 3D Euler equations with C^{1,alpha} velocity and boundary"),
    ("1904.04795", "F4", "Elgindi, Finite-time singularity formation for C^{1,alpha} solutions to the incompressible Euler equations on R^3"),
    ("1910.14071", "F4", "Elgindi-Ghoul-Masmoudi, On the stability of self-similar blow-up for C^{1,alpha} solutions"),
    ("2210.07191", "F4", "Chen-Hou, Stable nearly self-similar blowup of the 2D Boussinesq and 3D Euler equations"),
    ("1912.11009", "F5", "Merle-Raphael-Rodnianski-Szeftel, On the implosion of a three dimensional compressible fluid"),
    ("2606.12758", "F5", "OFF-LIST: Self-similar imploding solutions of the 1D compressible Euler equations with far field cutoff"),
    # -- OFF-LIST, added DURING the run and marked as such per SS2.3's last line.  These are
    # -- the closest published thing to SS4's localisation clause actually succeeding for
    # -- INCOMPRESSIBLE Navier-Stokes on R^3: Jia-Sverak's own 2012 "future work" sentence.
    ("2112.03116", "F3-OFFLIST", "OFF-LIST: Albritton-Brue-Colombo, Non-uniqueness of Leray solutions of the forced Navier-Stokes equations"),
    ("2209.03530", "F3-OFFLIST", "OFF-LIST: Albritton-Brue-Colombo, Gluing non-unique Navier-Stokes solutions"),
    ("1103.3718",  "F7", "SECONDARY for Bogovskii 1979 (journal-only): an elementary proof of the continuity of Bogovskii's right inverse of the divergence"),
]


def md5(p: pathlib.Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def fetch(aid: str) -> dict:
    pdf = PAPERS / f"{aid}.pdf"
    txt = PAPERS / f"{aid}.txt"
    rec = {"arxiv_id": aid}
    if not (pdf.exists() and pdf.stat().st_size > 0):
        url = f"https://arxiv.org/pdf/{aid}"
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                rec["http_status"] = r.status
                blob = r.read()
        except Exception as e:                                # noqa: BLE001
            rec["status"] = "UNREACHABLE"
            rec["reason"] = f"{type(e).__name__}: {e}"
            return rec
        if not blob.startswith(b"%PDF"):
            rec["status"] = "UNREACHABLE"
            rec["reason"] = f"response is not a PDF ({blob[:40]!r})"
            return rec
        pdf.write_bytes(blob)
        time.sleep(2.0)
    rec["pdf_bytes"] = pdf.stat().st_size
    rec["pdf_md5"] = md5(pdf)
    if not txt.exists():
        subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=True)
    rec["txt_md5"] = md5(txt)
    rec["txt_lines"] = len(txt.read_text(errors="replace").splitlines())
    rec["status"] = "OK"
    return rec


def main() -> int:
    PAPERS.mkdir(exist_ok=True)
    ids = sys.argv[1:]
    wanted = [w for w in WANTED if not ids or w[0] in ids]
    recs = []
    for aid, fam, title in wanted:
        r = fetch(aid)
        r["family"] = fam
        r["title"] = title
        recs.append(r)
        print(f"{aid:12s} {r['status']:12s} {r.get('txt_lines', '')} {title[:60]}", flush=True)
    if OUT.exists() and ids:
        old = json.loads(OUT.read_text())
        byid = {r["arxiv_id"]: r for r in old.get("fulltexts", [])}
        byid.update({r["arxiv_id"]: r for r in recs})
        recs = [byid[k] for k in sorted(byid)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(
        {"leg": 397, "unit": "L2'",
         "what": "full texts pulled for leg 397; Papers/ is gitignored so this is the committed provenance",
         "fulltexts": recs}, indent=1) + "\n")
    print(f"\nwrote {OUT}")
    bad = [r for r in recs if r["status"] != "OK"]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

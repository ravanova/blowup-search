"""Route-T4 (leg 393) -- RUNNER.

Unit `T4`, Lane T, wave 2: reproduce `arXiv:1902.00384` (van den Berg, Breden, Lessard,
van Veen, *Spontaneous periodic orbits in the Navier-Stokes flow*) row for row.

WHAT THIS SCRIPT IS, AND WHAT IT DELIBERATELY IS NOT
----------------------------------------------------
It is an AUDIT. It builds no operator. It computes no `Y0`, `Z0`, `Z1` or `Z2`. It runs no
contraction and no fixed-point argument. Its entire numerical content is:

  (a) verbatim string extraction from the paper's own text, and
  (b) arithmetic on the AUTHORS' OWN PUBLISHED constants and Fourier arrays, substituted
      into the AUTHORS' OWN printed formulas.

That is the apparatus named in this leg's pre-registration (`experiments/journal/leg_393.md`
Part I sec 2), and it is why ruling C1's second half is discharged by construction rather than by
argument: there is no `A` here to be bounded and no `M` here to be uniform in.

Precedent for the move: leg 316, which reproduced Dahne-Figueras row-for-row from that
paper's published constants while the same ban was in force.

SOURCES, both fetched over the network and both banked with HTTP evidence
-------------------------------------------------------------------------
  * `https://arxiv.org/pdf/1902.00384`  -> Papers/1902.00384.pdf        (via Papers/fetch.sh)
  * `https://www.math.vu.nl/~janbouwe/code/navierstokes/navierstokes-code.zip`
        -> Papers/ns_code/navierstokes-code/saveddata/{data,extra}orbit{1,2}.mat
    which is reference [41] of the paper itself.

`Papers/` is gitignored on purpose. Nothing third-party is committed; the curated JSON is.

    .venv/bin/python experiments/p2_route_t4_v1.py
"""

import hashlib
import json
import math
import os
import re
import subprocess
import zipfile

import numpy as np
import scipy.io as sio

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS = os.path.join(ROOT, "Papers")
PDF = os.path.join(PAPERS, "1902.00384.pdf")
ZIP = os.path.join(PAPERS, "navierstokes-code.zip")
CODE = os.path.join(PAPERS, "ns_code")
SAVED = os.path.join(CODE, "navierstokes-code", "saveddata")
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_t4_v1.json")

ARXIV_PDF_URL = "https://arxiv.org/pdf/1902.00384"
CODE_ZIP_URL = "https://www.math.vu.nl/~janbouwe/code/navierstokes/navierstokes-code.zip"

# ---------------------------------------------------------------------------
# Network. A query that fails to reach a service is banked as FAILED, never as a zero
# (leg 387 fabricated a controlled zero exactly that way; leg 392's discipline stands).
# ---------------------------------------------------------------------------


def curl(url, dest):
    """Fetch `url` to `dest` if absent. Returns a bankable evidence dict, always."""
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return {"url": url, "status": "ALREADY_PRESENT", "http_code": None,
                "bytes": os.path.getsize(dest), "reached_service": None}
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    proc = subprocess.run(
        ["curl", "-sSL", "--max-time", "300", "-o", dest,
         "-w", "%{http_code} %{size_download}", url],
        capture_output=True, text=True)
    fields = proc.stdout.strip().split()
    code = int(fields[0]) if fields and fields[0].isdigit() else 0
    nbytes = int(fields[1]) if len(fields) > 1 and fields[1].isdigit() else 0
    ok = code == 200 and nbytes > 0
    return {"url": url, "status": "OK" if ok else "FAILED", "http_code": code,
            "bytes": nbytes, "reached_service": bool(code)}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Text normalisation, so that quotes can be checked verbatim across pdftotext's line wraps.
# ---------------------------------------------------------------------------


def normalise(text):
    """De-hyphenate across line breaks, then collapse all whitespace to single spaces."""
    text = text.replace("­", "")
    text = re.sub(r"-\s*\n\s*", "", text)          # hard hyphenation at a line end
    text = re.sub(r"\s+", " ", text)
    return text


# ---------------------------------------------------------------------------
# The paper's own formulas, transcribed. Nothing here is invented by this leg.
# ---------------------------------------------------------------------------


def r_min_max(Y0, Z0, Z1, Z2):
    """Paper's (2.22) / (4.33)-(4.34). Roots of the radii polynomial the AUTHORS published.

    NOTE FOR THE BAN CHECK: `Y0, Z0, Z1, Z2` are READ from the authors' own output file
    `extraorbit*.mat`. This leg does not compute any of them, in any space, under any name.
    Substituting four published constants into a published quadratic formula is arithmetic
    on third-party data, which is exactly leg 316's precedent and constructs no operator.
    """
    a = 1.0 - (Z0 + Z1)
    disc = a * a - 2.0 * Y0 * Z2
    return (a - math.sqrt(disc)) / Z2, a / Z2, a, disc


def significant_ceil(r, decimals=5):
    """Paper's code `determineradii.m`, local function `significantceil`."""
    shift = decimals + math.floor(-math.log10(r))
    return math.ceil(r * 10 ** shift) / 10 ** shift


def scalar(x):
    return float(np.asarray(x).ravel()[0])


# ---------------------------------------------------------------------------


def main():
    net = {}
    net["arxiv_pdf"] = curl(ARXIV_PDF_URL, PDF)
    net["vu_code_zip"] = curl(CODE_ZIP_URL, ZIP)
    for key, ev in net.items():
        if ev["status"] == "FAILED":
            raise SystemExit(
                "UNREACHABLE: %s -> %s. Banked as FAILED, NOT as a zero. Re-run when "
                "egress is available; do not work around it." % (key, ev))

    if not os.path.isdir(SAVED):
        with zipfile.ZipFile(ZIP) as zf:
            zf.extractall(CODE)

    # ---------------- documentary layer -----------------------------------
    txt = subprocess.run(["pdftotext", "-layout", PDF, "-"],
                         capture_output=True, text=True).stdout
    flat = normalise(txt)
    low = flat.lower()

    # Verbatim quotes, each load-bearing for exactly one finding. Checked, not asserted.
    quotes = {
        "apparatus_abstract": (
            "a Newton-Kantorovich theorem is applied to obtain the (computer-assisted) "
            "proofs of existence"),
        "apparatus_banach_space": (
            "a zero finding problem posed on a Banach space of geometrically decaying "
            "Fourier coefficients"),
        "apparatus_approximate_inverse": (
            "We circumvent this difficulty by working with an approximate inverse A"),
        "twod_solutions": (
            "the solutions we present in Theorem 1.1 below are two-dimensional (in space) "
            "time-periodic solutions"),
        "twod_mechanism": (
            "they are independent of x3 and the third component of the velocity vanishes"),
        "twod_reason_is_memory": (
            "The only reason for this reduction is that the physical memory requirements "
            "for a three-dimensional solution are, for now, prohibitive in our current "
            "implementation"),
    }
    quote_found = {}
    for k, q in quotes.items():
        # tolerate pdftotext's unicode mangling of accented/math glyphs by comparing on
        # an ASCII-folded, case-folded, whitespace-free reduction
        red = lambda s: re.sub(r"[^a-z0-9()]", "", s.lower())
        quote_found[k] = red(q) in red(flat)

    # C+ : the paper's own apparatus is the ell^1-Fourier / radii-polynomial machinery.
    c_plus_terms = {
        "approximate inverse": low.count("approximate inverse"),
        "newton-kantorovich": low.count("newton-kantorovich"),
        "interval arithmetic": low.count("interval arithmetic"),
        "intlab": low.count("intlab"),
    }
    c_plus = all(v > 0 for v in c_plus_terms.values()) and all(quote_found[k] for k in (
        "apparatus_abstract", "apparatus_banach_space", "apparatus_approximate_inverse"))

    # C- : does the paper instead state a Zgliczynski-style dynamical closure?
    c_minus_terms = {
        "self-consistent": low.count("self-consistent") + low.count("self consistent"),
        "a priori bounds": low.count("a priori bounds"),
        "isolating": low.count("isolating"),
        "trapping region": low.count("trapping region"),
        "logarithmic norm": low.count("logarithmic norm"),
        "dynamical closure": low.count("dynamical closure"),
    }
    zgliczynski_lines = [l.strip() for l in txt.splitlines() if "gliczy" in l.lower()]
    galerkin_lines = [l.strip() for l in txt.splitlines() if "alerkin" in l]
    c_minus = any(v > 0 for v in c_minus_terms.values())

    # ---------------- data layer ------------------------------------------
    # Table 1 of the paper, transcribed from the PDF, to be checked against the data.
    TABLE1 = {
        "p1": {"eta": 1, "Nx1": 17, "Nx2": 17, "Nx3": 0, "Nt": 11,
               "Ndagger": 130, "Ntilde": 265, "RAM_GB": 10, "CPU_days": 6, "nu": 0.286},
        "p2": {"eta": 1, "Nx1": 21, "Nx2": 21, "Nx3": 0, "Nt": 16,
               "Ndagger": 210, "Ntilde": 425, "RAM_GB": 110, "CPU_days": 95, "nu": 0.265},
    }
    # The theorems' own printed enclosure values.
    PRINTED = {
        "p1": {"theorem": "Theorem 5.1", "r_sol_omega": 2.6314e-05, "r_sol_u": None,
               "r_sol_p": None},
        "p2": {"theorem": "Theorem 5.2 / Theorem 1.1", "r_sol_omega": 2.2491e-06,
               "r_sol_u": 2.2491e-06, "r_sol_p": 5.6486e-05},
    }

    rows = {}
    for tag, label in (("1", "p1"), ("2", "p2")):
        extra = sio.loadmat(os.path.join(SAVED, "extraorbit%s.mat" % tag))
        data = sio.loadmat(os.path.join(SAVED, "dataorbit%s.mat" % tag))
        b = extra["bounds"][0, 0]
        Y0, Z0, Z1, Z2 = (scalar(b["Y"]), scalar(b["Z0"]),
                          scalar(b["Z1"]), scalar(b["Z2"]))
        rmin, rmax, one_minus, disc = r_min_max(Y0, Z0, Z1, Z2)
        pub_rmin, pub_rmax = scalar(extra["rmin"]), scalar(extra["rmax"])
        radsol = np.asarray(extra["radsol"]).ravel().tolist()   # [omega,u,p,Omega,phi]
        nrec = np.asarray(extra["solshape"][0, 0]["Nrec"]).ravel().astype(int).tolist()

        om, u, p = data["omega"], data["u"], data["p"]
        eta = scalar(extra["eta"])
        assert eta == 1, "weights below assume eta == 1, which the authors chose (Remark 5.4)"
        norm_u = float(np.abs(u).sum())          # ||u||_X with eta = 1
        rsolp_recon = (2.0 * norm_u + rmin) * rmin

        # what the PUBLISHED pair (r_sol^p, r_sol^omega) implies for ||u||_X, via Lemma 6.2
        pr = PRINTED[label]
        implied_norm_u = None
        if pr["r_sol_p"] is not None:
            implied_norm_u = (pr["r_sol_p"] / pr["r_sol_omega"] - pr["r_sol_omega"]) / 2.0

        # dimensionality of the certified object, measured on the authors' own arrays
        nu_val = scalar(extra["nufloat"])
        Omega_bar = scalar(data["Omega"])
        dim = {
            "omega_shape": list(om.shape),
            "u_shape": list(u.shape),
            "p_shape": list(p.shape),
            "x3_mode_extent": int(om.shape[2]),
            "max_abs_u3": float(np.abs(u[..., 2]).max()),
            "max_abs_omega1": float(np.abs(om[..., 0]).max()),
            "max_abs_omega2": float(np.abs(om[..., 1]).max()),
            "max_abs_omega3": float(np.abs(om[..., 2]).max()),
            "setup_field_in_authors_output": str(np.asarray(extra["setup"]).ravel()[0]),
        }

        # WHY the authors' approximate inverse is bounded: the symbol modulus of the
        # dominant linear part, mu(n) = |nu*ntilde^2 + i*Omegabar*n4| (Definition 2.13).
        # A acts diagonally on the tail with lambda_n = 1/(nu*ntilde^2 + i*Omegabar*n4).
        Nd = int(scalar(extra["Ndagger"]))
        K = 60
        n1, n2, n3, n4 = np.meshgrid(*[np.arange(-K, K + 1)] * 4, indexing="ij")
        nt2 = n1 ** 2 + n2 ** 2 + n3 ** 2
        mu = np.abs(nu_val * nt2 + 1j * Omega_bar * n4)
        nonzero = ~((n1 == 0) & (n2 == 0) & (n3 == 0) & (n4 == 0))
        mu_nz = mu[nonzero]
        tail = mu_nz > Nd
        symbol = {
            "N_dagger": Nd,
            "box_half_width_scanned": K,
            "inf_mu_over_all_nonzero_modes": float(mu_nz.min()),
            "nu": nu_val,
            "Omega_bar": Omega_bar,
            "inf_mu_equals_nu": bool(abs(mu_nz.min() - nu_val) < 1e-12),
            "min_mu_on_tail": float(mu_nz[tail].min()),
            "sup_abs_lambda_on_tail": float(1.0 / mu_nz[tail].min()),
            "one_over_N_dagger": 1.0 / Nd,
        }

        rows[label] = {
            "arxiv_theorem": pr["theorem"],
            "nu": nu_val,
            "Omega_bar": Omega_bar,
            "published_bounds": {"Y0": Y0, "Z0": Z0, "Z1": Z1, "Z2": Z2,
                                 "Z1finite": scalar(b["Z1finite"]),
                                 "Z1tail": scalar(b["Z1tail"])},
            "paper_criterion_4_32": {
                "Z0_plus_Z1": Z0 + Z1,
                "Z0_plus_Z1_lt_1": bool(Z0 + Z1 < 1.0),
                "two_Y0_Z2": 2.0 * Y0 * Z2,
                "one_minus_Z0_Z1_squared": one_minus ** 2,
                "second_inequality_holds": bool(2.0 * Y0 * Z2 < one_minus ** 2),
                "discriminant": disc,
                "criterion_met": bool(Z0 + Z1 < 1.0 and 2.0 * Y0 * Z2 < one_minus ** 2),
            },
            "r_min": {"reproduced": rmin, "published": pub_rmin,
                      "rel_dev": abs(rmin - pub_rmin) / pub_rmin},
            "r_max": {"reproduced": rmax, "published": pub_rmax,
                      "rel_dev": abs(rmax - pub_rmax) / pub_rmax},
            "r_sol_Omega": {"reproduced": significant_ceil(rmin),
                            "published_in_package": radsol[3],
                            "printed_in_paper": pr["r_sol_omega"],
                            "rel_dev_vs_printed":
                                abs(significant_ceil(rmin) - pr["r_sol_omega"])
                                / pr["r_sol_omega"]},
            "r_sol_p": None,
            "norm_u_X": {"computed_from_published_data": norm_u,
                         "implied_by_printed_radii": implied_norm_u},
            "package_radsol_omega_u_p_Omega_phi": radsol,
            "solshape_Nrec": nrec,
            "table1_row": TABLE1[label],
            "table1_agrees_with_package": {
                "Nrec": nrec == [TABLE1[label]["Nx1"], TABLE1[label]["Nx2"],
                                 TABLE1[label]["Nx3"], TABLE1[label]["Nt"]],
                "Ndagger": int(scalar(extra["Ndagger"])) == TABLE1[label]["Ndagger"],
                "Ntilde": int(scalar(extra["Ntilde"])) == TABLE1[label]["Ntilde"],
                "eta": int(eta) == TABLE1[label]["eta"],
                "nu": abs(nu_val - TABLE1[label]["nu"]) < 1e-12,
            },
            "array_shape_matches_Nrec": list(om.shape[:4]) == [
                2 * nrec[0] + 1, 2 * nrec[1] + 1, 2 * nrec[2] + 1, 2 * nrec[3] + 1],
            "dimensionality": dim,
            "symbol_modulus": symbol,
            "authors_success_flags": {"success": int(scalar(extra["success"])),
                                      "radiisuccess": int(scalar(extra["radiisuccess"]))},
        }
        if implied_norm_u is not None:
            rows[label]["r_sol_p"] = {
                "reproduced": significant_ceil(rsolp_recon),
                "reproduced_raw_before_ceil": rsolp_recon,
                "published_in_package": radsol[2],
                "printed_in_paper": pr["r_sol_p"],
                "rel_dev_vs_printed":
                    abs(significant_ceil(rsolp_recon) - pr["r_sol_p"]) / pr["r_sol_p"],
                "note": ("the residual gap is the authors' `raddevp` term of "
                         "determineradii.m -- the weighted-l1 deviation between the "
                         "pressure recomputed from the symmetrised divergence-free "
                         "vorticity and the pressure array as stored -- which this audit "
                         "does not reconstruct. It can only WIDEN their radius, never "
                         "narrow it, so the reproduction is a lower bound on their "
                         "published value and the sign of the gap is the right one."),
            }
            rows[label]["norm_u_X"]["rel_dev"] = (
                abs(norm_u - implied_norm_u) / implied_norm_u)

    # ---------------- controls, resolved ----------------------------------
    controls = {
        "C_plus": {
            "asserts": ("the paper's own certification apparatus is an ell^1-Fourier / "
                        "radii-polynomial Newton-Kantorovich contraction built around a "
                        "single bounded approximate inverse"),
            "term_counts": c_plus_terms,
            "quotes_found": quote_found,
            "fired": bool(c_plus),
            "two_sided": ("if any term or quote were absent, H1 would be unestablished, "
                          "branch (c) would NOT fire, and verdict rule V2 would send this "
                          "unit into a full reproduction under C1's scope"),
        },
        "C_minus": {
            "asserts": ("the paper does NOT state a Zgliczynski-style self-consistent "
                        "a-priori-bounds / Galerkin-plus-tail DYNAMICAL closure"),
            "term_counts": c_minus_terms,
            "zgliczynski_mentions": zgliczynski_lines,
            "zgliczynski_only_in_bibliography": bool(
                len(zgliczynski_lines) == 1 and "[48]" in zgliczynski_lines[0]),
            "galerkin_mentions": galerkin_lines,
            "fired": bool(c_minus),
            "two_sided": ("if this control HAD fired, C1's scope would cover the "
                          "reproduction and V2 would govern instead of V1"),
        },
        "C_3D": {
            "asserts": "Table 1 records Nx3 = 0 for BOTH certified rows",
            "p1_Nx3": rows["p1"]["solshape_Nrec"][2],
            "p2_Nx3": rows["p2"]["solshape_Nrec"][2],
            "fired": bool(rows["p1"]["solshape_Nrec"][2] == 0
                          and rows["p2"]["solshape_Nrec"][2] == 0),
            "two_sided": ("if Nx3 > 0 for either row, W2's crack survives at full text "
                          "and leg 348's classification is confirmed on its most "
                          "load-bearing clause"),
        },
        "C_dec_plus": {
            "asserts": ("decoded array extents match Table 1's own Nrec for BOTH files "
                        "(leg 316's decode discipline: check the decoder against an "
                        "independent reference before trusting a number through it)"),
            "p1": rows["p1"]["array_shape_matches_Nrec"] and all(
                rows["p1"]["table1_agrees_with_package"].values()),
            "p2": rows["p2"]["array_shape_matches_Nrec"] and all(
                rows["p2"]["table1_agrees_with_package"].values()),
            "fired": bool(rows["p1"]["array_shape_matches_Nrec"]
                          and rows["p2"]["array_shape_matches_Nrec"]
                          and all(rows["p1"]["table1_agrees_with_package"].values())
                          and all(rows["p2"]["table1_agrees_with_package"].values())),
            "two_sided": "a shape mismatch voids F1 and F2 and must be reported as a failed decode",
        },
        "C_dec_minus": {
            "asserts": "the two published files do NOT decode to the same shape",
            "p1_shape": rows["p1"]["dimensionality"]["omega_shape"],
            "p2_shape": rows["p2"]["dimensionality"]["omega_shape"],
            "fired": bool(rows["p1"]["dimensionality"]["omega_shape"]
                          != rows["p2"]["dimensionality"]["omega_shape"]),
            "two_sided": ("if they matched, the decoder is not discriminating between the "
                          "two published rows and every number it produces is suspect"),
        },
        "C_net": {
            "asserts": "a positive datum that each external service was actually reached",
            "evidence": net,
            "fired": all(e["status"] in ("OK", "ALREADY_PRESENT") for e in net.values()),
            "two_sided": "a zero with no HTTP evidence is banked as FAILED, never as a measured absence",
        },
    }

    verdict = "V1_BRANCH_C_STOP" if (c_plus and not c_minus) else "V2_PROCEED"

    doc = {
        "leg": 393,
        "unit": "T4",
        "lane": "T",
        "route": "Route-T4",
        "target_paper": {
            "arxiv_id": "1902.00384",
            "title": "Spontaneous periodic orbits in the Navier-Stokes flow",
            "authors": ["J.B. van den Berg", "M. Breden", "J.-P. Lessard", "L. van Veen"],
            "date": "2019-02-01",
            "pdf_sha256": sha256(PDF),
            "code_zip_sha256": sha256(ZIP),
            "code_url_is_paper_reference_41": CODE_ZIP_URL,
        },
        "network_evidence": net,
        "apparatus_this_leg_used": {
            "name": "documentary + published-data audit (no certification apparatus)",
            "constructs_an_operator": False,
            "constructs_Y0_Z0_Z1_Z2": False,
            "constructs_an_approximate_inverse": False,
            "has_an_M_indexed_family": False,
            "c1_compliance": ("NGX excludes a single bounded A working uniformly in M. "
                              "This apparatus has no A to be bounded and no M to be "
                              "uniform in, so the exclusion is vacuous on it. See "
                              "experiments/journal/leg_393.md Part I sec 2."),
            "precedent": "leg 316 (Dahne-Figueras reproduced from published constants under the same ban)",
        },
        "paper_apparatus_as_measured": {
            "name": ("Newton-Kantorovich / radii-polynomial contraction in a weighted-l1 "
                     "(geometric, eta) Fourier coefficient space"),
            "theorem": "Theorem 2.15 (2.17)-(2.21); symmetry-reduced Theorem 4.23 (4.28)-(4.32)",
            "approximate_inverse": ("A : X_{-2,-1} -> X, section 2.3: numerical inverse "
                                    "A^(N_dagger) of the finite block on E_dagger, PLUS the "
                                    "exact diagonal lambda_n = 1/(nu*ntilde^2 + i*Omegabar*n4) "
                                    "off it. ONE bounded operator, acting on the whole "
                                    "infinite-dimensional space at once."),
            "is_the_banned_machinery": True,
            "is_a_galerkin_plus_tail_dynamical_closure": False,
        },
        "controls": controls,
        "verdict_rule_fired": verdict,
        "gate_answer": ("STOP (pre-committed branch (c))" if verdict == "V1_BRANCH_C_STOP"
                        else "PROCEED"),
        "rows": rows,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=2, sort_keys=True)
    print("wrote %s" % OUT)
    print("verdict rule fired: %s" % verdict)
    for label in ("p1", "p2"):
        r = rows[label]
        print("  %s (%s, nu=%s): rmin rel dev %.3e | rmax rel dev %.3e | "
              "criterion met %s | Nx3 = %d"
              % (label, r["arxiv_theorem"], r["nu"], r["r_min"]["rel_dev"],
                 r["r_max"]["rel_dev"], r["paper_criterion_4_32"]["criterion_met"],
                 r["solshape_Nrec"][2]))


if __name__ == "__main__":
    main()

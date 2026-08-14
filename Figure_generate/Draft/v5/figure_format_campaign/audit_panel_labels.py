#!/usr/bin/env python
"""Audit panel labels in the SI and Extended Data figures.

The specification (ED-16 was confirmed by the author to apply to Supplementary
Information as well as to main display items and Extended Data):

    "Separate panels in multi-panelled figures should be labelled with 8-pt
     bold, upright (not italic) and lowercase a, b, c, etc."
    https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/

So a compliant panel label is all four of: lowercase, bold, upright, and 8 pt
AT PRINT SIZE. Print size is computed with the same validated model as
verify_figures.py, which this module imports rather than re-deriving.

Detection is a heuristic: a text span whose entire content is a single letter
a-h or A-H, optionally followed by ')' or '.'. That is how every panel label in
this tree is drawn (no '(a)' forms exist here; checked).

Two filters keep the false-positive rate down, both learned from a first pass
over this tree:

  * ITALIC/OBLIQUE spans are never panel labels. The spec says panel letters
    are upright, and every oblique single letter found here was a mathtext
    variable inside an axis label ('f' in R3_4_mixed_sign_higher_order, 'h' in
    R3_4_mean_variance_grid). Counting those as non-compliant labels would send
    someone to bold a variable name.
  * Candidates are grouped by (font, size) and a group counts as panel labels
    only if its letters are DISTINCT and form a contiguous run from 'a'/'A'.
    Panel letters are always a, b, c, ... in one style; data annotations are
    not. This is what separates the real 'a'-'f' labels of
    natural_taxonomic_distinctness from the 'C'/'D' category marks beside them,
    which repeat as D, C, D, C, D, C in a different weight.
    A geometric "nothing above and to the left" test was tried first and
    rejected: it throws away every label below the first row, because panel a's
    text sits above and to the left of panel c's letter.

Anything still surprising should be eyeballed in the rendered figure before
acting on it; the report prints position and font for exactly that reason.

Usage
-----
    python audit_panel_labels.py                 # every figure in the SI
    python audit_panel_labels.py pool_size       # substring filter
    python audit_panel_labels.py --fail-only
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

from verify_figures import LATEX_DIR, TEX_FILES, parse_tex, TEXTWIDTH_BP

LABEL_PT = 8.0
TOL = 0.25                       # pt; allows 7.75-8.25 at print size
LABEL_RX = re.compile(r"^([a-hA-H])[).]?$")

# fitz span flags: bit 1 italic, bit 4 bold (serif is bit 2, mono bit 3)
FLAG_ITALIC = 1 << 1
FLAG_BOLD = 1 << 4


def find_labels(pdf: Path, scale: float | None):
    """Return a list of candidate panel labels with their measured properties.

    Also returns the count of single letters rejected as mathtext variables, so
    the caller can report that the figure was looked at and deliberately
    skipped rather than silently missed.
    """
    cand = []
    doc = fitz.open(pdf)
    page = doc[0]
    for b in page.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            for s in line["spans"]:
                t = s["text"].strip()
                if not t:
                    continue
                m = LABEL_RX.match(t)
                if not m:
                    continue
                font = s.get("font", "")
                italic = bool(s["flags"] & FLAG_ITALIC) or \
                    any(k in font.lower() for k in ("italic", "oblique"))
                cand.append({
                    "char": m.group(1),
                    "lower": m.group(1).islower(),
                    "bold": bool(s["flags"] & FLAG_BOLD) or "bold" in font.lower(),
                    "italic": italic,
                    "native_pt": round(s["size"], 2),
                    "print_pt": round(s["size"] * scale, 2) if scale else None,
                    "font": font,
                    "bbox": s["bbox"],
                    "at": (round(s["bbox"][0], 1), round(s["bbox"][1], 1)),
                })
    doc.close()

    upright, n_math = [], 0
    for c in cand:
        if c["italic"]:
            n_math += 1
        else:
            upright.append(c)

    groups: dict[tuple, list] = {}
    for c in upright:
        groups.setdefault((c["font"], c["native_pt"]), []).append(c)

    out, n_rejected = [], 0
    for members in groups.values():
        letters = [m["char"] for m in members]
        low = sorted(ch.lower() for ch in letters)
        contiguous = low == list("abcdefgh"[:len(low)])
        if len(set(low)) == len(low) and contiguous:
            out.extend(members)
        else:
            n_rejected += len(members)

    out.sort(key=lambda d: (round(d["at"][1] / 10), d["at"][0]))
    return out, n_math, n_rejected


def judge(lab):
    """Return the list of reasons this label is non-compliant."""
    bad = []
    if not lab["lower"]:
        bad.append("uppercase")
    if not lab["bold"]:
        bad.append("not bold")
    p = lab["print_pt"]
    if p is None:
        bad.append("no scale")
    elif abs(p - LABEL_PT) > TOL:
        bad.append(f"{p:.2f} pt")
    return bad


def main() -> int:
    args = [a for a in sys.argv[1:]]
    fail_only = "--fail-only" in args
    args = [a for a in args if not a.startswith("--")]
    needle = args[0] if args else None

    entries = []
    for t in TEX_FILES:
        entries += parse_tex(t)

    n_fig = n_ok = n_bad = 0
    no_labels = []
    tot_math = tot_inside = 0
    counts = {"uppercase": 0, "not bold": 0, "wrong size": 0}

    for e in entries:
        if needle and needle not in e["file"]:
            continue
        pdf = LATEX_DIR / e["file"]
        if not pdf.exists() or pdf.suffix.lower() != ".pdf":
            continue
        doc = fitz.open(pdf)
        w_bp = doc[0].rect.width
        doc.close()
        mult = e["multiplier"]
        scale = (mult * TEXTWIDTH_BP / w_bp) if mult else None
        # Extended Data publishes standalone at native size, so for those the
        # printed label size IS the native size.
        if "extended_data" in str(pdf):
            scale = 1.0

        labels, n_math, n_inside = find_labels(pdf, scale)
        tot_math += n_math
        tot_inside += n_inside
        n_fig += 1
        if not labels:
            no_labels.append(pdf.name)
            continue

        problems = [(l, judge(l)) for l in labels]
        bad = [(l, b) for l, b in problems if b]
        if bad:
            n_bad += 1
            for _, b in bad:
                for reason in b:
                    counts["wrong size" if reason.endswith("pt") else reason] += 1
        else:
            n_ok += 1
        if fail_only and not bad:
            continue

        tag = "OK" if not bad else "FIX"
        letters = "".join(l["char"] for l in labels)
        print(f"\n{pdf.name:<52} {tag}   labels: {letters}")
        for l, b in problems:
            note = ", ".join(b) if b else "ok"
            print(f"    '{l['char']}'  native {l['native_pt']:>5.2f}  "
                  f"print {l['print_pt'] if l['print_pt'] is not None else float('nan'):>5.2f}  "
                  f"{'bold' if l['bold'] else 'regular':<8}{l['font']:<22} {note}")

    print("\n" + "-" * 78)
    print(f"figures with labels : {n_ok + n_bad}   compliant {n_ok}   needing work {n_bad}")
    print(f"figures with none   : {len(no_labels)} (single-panel, or labels drawn as paths)")
    print("label defects       : " +
          ", ".join(f"{k} {v}" for k, v in counts.items() if v))
    print(f"rejected candidates : {tot_math} italic (mathtext variables), "
          f"{tot_inside} not a contiguous a-b-c run (data annotations)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

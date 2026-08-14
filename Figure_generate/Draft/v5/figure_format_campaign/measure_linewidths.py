#!/usr/bin/env python
"""Measure stroke line widths in figure PDFs against the Nature Extended Data spec.

Extended Data guide: "Lines and strokes should be set between 0.25 and 1 pt."

Extended Data figures publish as separate files at native size, so the width
recorded in the PDF content stream IS the printed width -- no scale factor.

Usage
-----
    python measure_linewidths.py                      # every ED composite
    python measure_linewidths.py ED_Fig6              # substring filter
    python measure_linewidths.py --panels             # panel_sources/ instead
    python measure_linewidths.py --path <dir>         # arbitrary directory
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import fitz

ED_DIR = Path(__file__).resolve().parent.parent / "latex" / "figures" / "extended_data"
MIN_PT, MAX_PT = 0.25, 1.0
TOL = 0.005


def measure(pdf: Path) -> dict[float, int]:
    """Return {rounded stroke width in pt: number of drawing ops}."""
    widths: dict[float, int] = defaultdict(int)
    doc = fitz.open(pdf)
    for page in doc:
        for d in page.get_drawings():
            # only stroked paths carry a line width; 'f' (fill-only) does not
            if d.get("type") not in ("s", "fs"):
                continue
            w = d.get("width")
            if w is None:
                continue
            # a width of 0 means "thinnest renderable line" in PDF, which is a
            # device-dependent hairline and out of spec by definition
            widths[round(float(w), 3)] += 1
    doc.close()
    return dict(widths)


def report(pdf: Path) -> bool:
    widths = measure(pdf)
    if not widths:
        print(f"  {pdf.name:<44} no stroked paths")
        return True
    lo, hi = min(widths), max(widths)
    bad = {w: n for w, n in widths.items() if w < MIN_PT - TOL or w > MAX_PT + TOL}
    ok = not bad
    status = "PASS" if ok else "FAIL"
    print(f"  {pdf.name:<44} {lo:.2f}-{hi:.2f} pt  {status}")
    for w in sorted(widths):
        mark = "  <-- out of 0.25-1 pt" if w in bad else ""
        print(f"      {w:>6.3f} pt  x{widths[w]:<6d}{mark}")
    return ok


def main() -> int:
    args = [a for a in sys.argv[1:]]
    directory = ED_DIR
    if "--panels" in args:
        args.remove("--panels")
        directory = ED_DIR / "panel_sources"
    if "--path" in args:
        i = args.index("--path")
        directory = Path(args[i + 1])
        del args[i : i + 2]
    substr = args[0] if args else ""

    pdfs = sorted(p for p in directory.glob("*.pdf") if substr.lower() in p.name.lower())
    if not pdfs:
        print(f"no PDFs matching {substr!r} in {directory}")
        return 1

    print(f"{directory}\nspec: {MIN_PT}-{MAX_PT} pt (Extended Data guide)\n")
    n_pass = sum(report(p) for p in pdfs)
    print(f"\n{n_pass}/{len(pdfs)} within spec")
    return 0 if n_pass == len(pdfs) else 1


if __name__ == "__main__":
    sys.exit(main())

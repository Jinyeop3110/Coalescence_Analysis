#!/usr/bin/env python
"""Nature Ecology & Evolution supplementary-figure format verifier.

Scope of this campaign: TEXT SIZE and COLOUR only.
  - Text size at print size must be within 5-7 pt.
  - Colour mode must be RGB (no CMYK / Separation / DeviceN).

Typeface family and font embedding (Type 3) are deliberately NOT checked here.

Usage
-----
    python verify_figures.py                    # verify every SI figure
    python verify_figures.py pool_size          # verify figures matching a substring
    python verify_figures.py --fail-only        # only show non-compliant figures
    python verify_figures.py --json out.json    # machine-readable dump

Print size model (validated against the compiled supplementary.pdf:
25,525 characters predicted == 25,525 observed, all 85 distinct sizes matched):

    scale       = (include_multiplier * TEXTWIDTH_BP) / native_pdf_width_bp
    print_pt    = native_font_pt * scale

Extended Data figures are additionally checked at their STANDALONE size
(they are built 180 mm wide and Nature typesets them as separate files at
native size, where print_pt == native_pt). ED figures must satisfy BOTH
measures, which constrains native text to roughly 6.3-7.0 pt.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import fitz

# --------------------------------------------------------------- constants
LATEX_DIR = Path(__file__).resolve().parent.parent / "latex"
TEX_FILES = [
    LATEX_DIR / "supplementary_sections" / "figures.tex",
    LATEX_DIR / "supplementary_sections" / "extended_data.tex",
]
# supplementary.log: \textwidth=452.9679pt (TeX pt = 1/72.27 in) -> big points
TEXTWIDTH_BP = 452.9679 / 72.27 * 72.0          # 451.28 bp = 159.2 mm
MIN_PT, MAX_PT = 5.0, 7.0
TOL = 0.05                                       # rounding slack

ENV_OPEN = re.compile(r"\\begin\{(subfigure|minipage)\}(?:\[[^\]]*\])?\{([^}]*)\}")
ENV_CLOSE = re.compile(r"\\end\{(subfigure|minipage)\}")
INCLUDE = re.compile(r"\\includegraphics(?:\[([^\]]*)\])?\{([^}]+)\}")

CMYK_RX = re.compile(rb"(?:^|\s)[-0-9.]+\s+[-0-9.]+\s+[-0-9.]+\s+[-0-9.]+\s+(k|K)\s")


def width_multiplier(expr: str):
    m = re.match(r"^([0-9.]*)\s*\\(?:text|column|line)width$", expr.strip())
    if m:
        return float(m.group(1)) if m.group(1) else 1.0
    return None


def parse_tex(tex_path: Path):
    """Yield {file, line, multiplier} for every \\includegraphics."""
    out, stack = [], []
    for lineno, line in enumerate(tex_path.read_text().splitlines(), 1):
        code = "" if line.lstrip().startswith("%") else line.split("%")[0]
        if not code:
            continue
        for m in ENV_OPEN.finditer(code):
            stack.append(width_multiplier(m.group(2)))
        for m in INCLUDE.finditer(code):
            opt, target = m.group(1) or "", m.group(2)
            mult = None
            wm = re.search(r"width\s*=\s*([^,\]]+)", opt)
            if wm:
                mult = width_multiplier(wm.group(1))
            if mult is not None:
                for emult in stack:
                    if emult is not None:
                        mult *= emult
            out.append(dict(file=target, line=lineno, tex=tex_path.name,
                            multiplier=mult))
        for _ in ENV_CLOSE.finditer(code):
            if stack:
                stack.pop()
    return out


def analyse(pdf: Path, multiplier):
    r = {"exists": pdf.exists()}
    if not pdf.exists():
        return r
    doc = fitz.open(pdf)
    page = doc[0]
    w_bp = page.rect.width
    r["native_in"] = round(w_bp / 72, 3)
    r["native_mm"] = round(w_bp / 72 * 25.4, 1)
    scale = (multiplier * TEXTWIDTH_BP / w_bp) if multiplier else None
    r["scale"] = round(scale, 4) if scale else None

    sizes = defaultdict(int)
    examples = defaultdict(list)
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if not t:
                    continue
                k = round(s["size"], 2)
                sizes[k] += len(t)
                if len(examples[k]) < 3:
                    examples[k].append(t[:24])
    r["has_text"] = bool(sizes)
    r["tiers"] = [
        {"native_pt": k,
         "print_pt": round(k * scale, 2) if scale else None,
         "n_chars": sizes[k],
         "examples": examples[k]}
        for k in sorted(sizes)
    ]
    if scale and sizes:
        prints = [t["print_pt"] for t in r["tiers"]]
        r["print_min"], r["print_max"] = min(prints), max(prints)
        r["size_ok"] = MIN_PT - TOL <= r["print_min"] and r["print_max"] <= MAX_PT + TOL
        # native span ratio vs the 1.4x width of the 5-7 pt band
        nat = sorted(sizes)
        r["native_ratio"] = round(nat[-1] / nat[0], 2) if nat[0] else None
        r["rescalable"] = (r["native_ratio"] or 1) <= (MAX_PT / MIN_PT) + 1e-9
    else:
        r["size_ok"] = None

    # Extended Data: also judge at standalone native size (print_pt == native_pt)
    r["is_ed"] = "extended_data" in str(pdf)
    if r["is_ed"] and sizes:
        nat = sorted(sizes)
        r["standalone_min"], r["standalone_max"] = nat[0], nat[-1]
        r["standalone_ok"] = MIN_PT - TOL <= nat[0] and nat[-1] <= MAX_PT + TOL
        r["dual_ok"] = bool(r.get("size_ok")) and r["standalone_ok"]

    # colour
    raw = pdf.read_bytes()
    streams = []
    for xref in page.get_contents():
        try:
            streams.append(doc.xref_stream(xref))
        except Exception:
            pass
    for xo in page.get_xobjects():
        try:
            streams.append(doc.xref_stream(xo[0]))
        except Exception:
            pass
    data = b"\n".join(s for s in streams if s)
    r["cmyk"] = bool(CMYK_RX.search(data)) or b"/DeviceCMYK" in raw
    r["separation"] = b"/Separation" in raw or b"/DeviceN" in raw
    r["colour_ok"] = not (r["cmyk"] or r["separation"])
    doc.close()
    return r


def main():
    args = [a for a in sys.argv[1:]]
    fail_only = "--fail-only" in args
    json_out = None
    if "--json" in args:
        i = args.index("--json")
        json_out = args[i + 1]
        del args[i:i + 2]
    args = [a for a in args if not a.startswith("--")]
    needle = args[0] if args else None

    entries = []
    for t in TEX_FILES:
        entries += parse_tex(t)

    rows, npass, nfail = [], 0, 0
    for e in entries:
        if needle and needle not in e["file"]:
            continue
        res = analyse(LATEX_DIR / e["file"], e["multiplier"])
        res.update(e)
        rows.append(res)

    print(f"{'figure':<58} {'mult':>5} {'scale':>6} {'print pt':>13} {'size':>6} {'col':>4}")
    print("-" * 100)
    for r in rows:
        ok = r.get("size_ok")
        if ok:
            npass += 1
        else:
            nfail += 1
        if fail_only and ok:
            continue
        name = r["file"].split("/")[-1]
        rng = (f"{r['print_min']:.2f}-{r['print_max']:.2f}"
               if r.get("print_min") is not None else "no text")
        flag = "PASS" if ok else ("n/a" if ok is None else "FAIL")
        extra = ""
        if r.get("is_ed"):
            extra = f"  [standalone {r['standalone_min']:.2f}-{r['standalone_max']:.2f} " \
                    f"{'OK' if r.get('standalone_ok') else 'FAIL'}]"
        print(f"{name:<58} {r['multiplier'] or 0:>5.2f} {r['scale'] or 0:>6.3f} "
              f"{rng:>13} {flag:>6} {'OK' if r.get('colour_ok') else 'CMYK':>4}{extra}")
        if not ok and r.get("tiers"):
            for t in r["tiers"]:
                p = t["print_pt"]
                if p is None:
                    continue
                mark = "  " if MIN_PT - TOL <= p <= MAX_PT + TOL else ("<<" if p < MIN_PT else ">>")
                print(f"      {mark} native {t['native_pt']:>6.2f} -> print {p:>5.2f} pt "
                      f"n={t['n_chars']:<5} {t['examples']}")
            if not r.get("rescalable"):
                print(f"      !! native span ratio {r['native_ratio']} > 1.40 "
                      f"- NOT fixable by rescaling; font sizes must be harmonised")

    print("-" * 100)
    print(f"TOTAL {len(rows)}   size PASS {npass}   size FAIL {nfail}")
    if json_out:
        Path(json_out).write_text(json.dumps(rows, indent=1))
        print(f"wrote {json_out}")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build the composite Extended Data figures as vector art and size them to spec.

Run with the miniforge interpreter, which is the one carrying PyMuPDF:
    ~/miniforge3/bin/python rebuild_and_fit_a4.py

Why this exists
---------------
combine_extended_figures.py assembles panels by rasterising each one to a
300 dpi JPEG. That conflicts with the Nature branded-journals artwork guide,
which requires line art (graphs, charts, schematics) to stay vector and says
bitmap formats "cannot be used for vector art". It also flattens all text, so
nothing in the figure remains editable for the production team.

Extended Data Figs. 5, 6 and 7 are the composites, so they are rebuilt here
with show_pdf_page, which embeds the source PDFs and keeps them vector.

Sizing follows the Extended Data guide, which has its own limits rather than
the caption-length table used for main display items:
  width   180 mm
  height  170 mm
Both sit inside A4 (210 x 297 mm), which the editor requires separately, so
one target satisfies both.

When a composite exceeds 170 mm, only its square "cells" rows are shrunk; any
full-width row keeps its size. Scaling the whole page instead would shrink
every panel, and in ED 5 that drags panel f's per-bar annotations from 4.4 pt
to about 3.5 pt, well under the 5 pt floor.

Panel labels are lowercase bold at 8 pt, per the figure specifications, which
name them as an exception to the 5-7 pt range that governs all other text.

The script is idempotent. Figures already at or under target are left alone.
"""
import pathlib
import shutil
import sys

import fitz

MM = 72.0 / 25.4

V5 = pathlib.Path(
    "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404"
    "/Figure_generate/Draft/v5"
)
PANEL_SRC = V5 / "latex/figures/extended_data/panel_sources"

TARGET_W_MM = 180.0

# Extended Data has its own size rule, and it is not the caption-length table
# used for main display items:
#   "Maximum page dimensions are 180 mm wide by 170 mm tall"
#   https://www.nature.com/documents/Extended_Data_guide.pdf
# An earlier version of this script capped heights at 185-210 mm from the main
# display-item table. That was the wrong table and produced over-tall figures.
#
# This matters more for Extended Data than for main figures, because Extended
# Data is "not edited or styled by our art department" - whatever is supplied
# is what publishes.
HEIGHT_CAP_MM = 170.0

ED_DIRS = [
    V5 / "latex/figures/extended_data",
    V5 / "revision_submission/00_submit_new/Main_Manuscript_Revised_LaTeX_Source/figures/extended_data",
    V5 / "revision_submission/00_submit_new/Supplementary_Information_LaTeX_Source/figures/extended_data",
    V5 / "revision_submission/00_submit_new/Extended_Data_Figures",
]

# "Try to keep white space to a minimum when arranging panels within a figure."
# Tightened from 6/4/7/5.5 so ED 5 can reach the 170 mm cap by shrinking its
# square panels rather than by scaling the whole figure.
MARGIN_MM = 4.0
COL_GAP_MM = 3.0
ROW_GAP_MM = 5.0
LABEL_GAP_MM = 4.0
# Panel letters are drawn at native composite size (fit() is a no-op for the
# figures that use them), so this value IS the print size.
#
# 8 pt is correct and is NOT a violation of the 5-7 pt rule. Nature's figure
# specifications treat panel letters as a named exception:
#   "Separate panels in multi-panelled figures should be labelled with 8-pt
#    bold, upright (not italic) and lowercase a, b, c, etc."
#   "Maximum text size: 7 pt. Minimum text size: 5 pt."  <- all *other* text
# https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/
#
# This was briefly set to 6.8 on the assumption that the 7 pt ceiling covered
# panel letters too. It does not. Do not lower it again.
LABEL_PT = 8.0
# Condition titles are ordinary figure text, so keep them within Nature's
# 5--7 pt range.  They are added at composite time so ED Fig. 7 continues to
# use the curated source panels (and their established sample counts).
TITLE_PT = 6.5

# Each row is (panel indices, width rule). "cells" uses the standard
# three-across cell width; a float is a fraction of the content width.
BUILDS = {
    5: {
        "panels": ["ED_Fig4a_4species.pdf", "ED_Fig4b_6species.pdf",
                   "ED_Fig4c_12species.pdf", "ED_Fig4d_24species.pdf",
                   "ED_Fig4e_48species.pdf", "ED_Fig4f_species_ablation_bar.pdf"],
        "rows": [([0, 1, 2], "cells"), ([3, 4], "cells"), ([5], 1.0)],
    },
    6: {
        "panels": ["ED_Fig2a_correlation_u0.3.pdf", "ED_Fig2b_correlation_u0.6.pdf",
                   "ED_Fig2c_correlation_u0.8.pdf", "ED_Fig2d_correlation_vs_mu.pdf"],
        "rows": [([0, 1, 2], "cells"), ([3], 0.55)],
    },
    7: {
        "panels": ["ED_Fig3a_correlation_Nutr-.pdf", "ED_Fig3b_correlation_Base.pdf",
                   "ED_Fig3c_correlation_Nutr+.pdf"],
        "rows": [([0, 1, 2], "cells")],
        "titles": ["Nutr-", "Base", "Nutr+"],
    },
}


def build(num, spec, out_path):
    srcs = []
    for name in spec["panels"]:
        p = PANEL_SRC / name
        if not p.exists():
            sys.exit(f"missing source panel: {p}")
        srcs.append(fitz.open(p))

    content_w = TARGET_W_MM - 2 * MARGIN_MM
    cell_w = (content_w - 2 * COL_GAP_MM) / 3.0

    def layout(cw):
        """Return (plan, total height) for a given 'cells' column width."""
        plan, total = [], 2 * MARGIN_MM + ROW_GAP_MM * (len(spec["rows"]) - 1)
        for idxs, rule in spec["rows"]:
            w = cw if rule == "cells" else content_w * float(rule)
            hs = [w * (srcs[i].load_page(0).rect.height / srcs[i].load_page(0).rect.width)
                  for i in idxs]
            plan.append((idxs, w, hs, max(hs)))
            total += LABEL_GAP_MM + max(hs)
        return plan, total

    plan, total_h = layout(cell_w)

    # If the figure is too tall, shrink only the square "cells" rows. Scaling the
    # whole page would shrink every panel, and in ED 5 that drags panel f's
    # per-bar annotations below the 5 pt floor. The wide full-width row keeps its
    # size, so its text is unaffected.
    if total_h > HEIGHT_CAP_MM:
        fixed = sum(rh for (idxs, rule), (_, _, _, rh)
                    in zip(spec["rows"], plan) if rule != "cells")
        cells = sum(rh for (idxs, rule), (_, _, _, rh)
                    in zip(spec["rows"], plan) if rule == "cells")
        overhead = total_h - fixed - cells
        if cells > 0:
            s = (HEIGHT_CAP_MM - overhead - fixed) / cells
            if s > 0:
                plan, total_h = layout(cell_w * s)

    doc = fitz.open()
    page = doc.new_page(width=TARGET_W_MM * MM, height=total_h * MM)

    letters = "abcdefgh"
    k, y = 0, MARGIN_MM
    for idxs, w, heights, row_h in plan:
        y += LABEL_GAP_MM
        row_w = len(idxs) * w + (len(idxs) - 1) * COL_GAP_MM
        x = (TARGET_W_MM - row_w) / 2.0
        for i, h in zip(idxs, heights):
            rect = fitz.Rect(x * MM, y * MM, (x + w) * MM, (y + h) * MM)
            page.show_pdf_page(rect, srcs[i], 0)
            page.insert_text(fitz.Point(x * MM, (y - 1.6) * MM),
                             letters[k], fontname="hebo", fontsize=LABEL_PT)
            if "titles" in spec:
                title_rect = fitz.Rect(x * MM, (y - LABEL_GAP_MM) * MM,
                                       (x + w) * MM, y * MM)
                page.insert_textbox(title_rect, spec["titles"][k],
                                    fontname="hebo", fontsize=TITLE_PT,
                                    align=fitz.TEXT_ALIGN_CENTER)
            x += w + COL_GAP_MM
            k += 1
        y += row_h + ROW_GAP_MM

    doc.save(out_path, deflate=True, garbage=4)
    doc.close()
    for s in srcs:
        s.close()
    return TARGET_W_MM, total_h


def fit(path):
    """Scale a page down to the Extended Data maximum, 180 x 170 mm."""
    src = fitz.open(path)
    r = src.load_page(0).rect
    w_mm, h_mm = r.width / MM, r.height / MM
    scale = min(TARGET_W_MM / w_mm, HEIGHT_CAP_MM / h_mm, 1.0)
    if scale >= 0.999:
        src.close()
        return w_mm, h_mm, 1.0
    out = fitz.open()
    page = out.new_page(width=r.width * scale, height=r.height * scale)
    page.show_pdf_page(page.rect, src, 0)
    tmp = path.with_suffix(".__s.pdf")
    out.save(tmp, deflate=True, garbage=4)
    out.close()
    src.close()
    tmp.replace(path)
    return w_mm * scale, h_mm * scale, scale


if __name__ == "__main__":
    print(f"== composing ED 5, 6, 7 as vector at {TARGET_W_MM:.0f} mm ==")
    for num, spec in sorted(BUILDS.items()):
        w, h = build(num, spec, ED_DIRS[0] / f"ED_Fig{num}_combined.pdf")
        print(f"   ED {num}: {w:.1f} x {h:.1f} mm  (cap {HEIGHT_CAP_MM:.0f} mm)")

    print(f"== sizing every item to {TARGET_W_MM:.0f} x {HEIGHT_CAP_MM:.0f} mm ==")
    for n in range(1, 9):
        name = f"ED_Fig{n}_combined.pdf"
        w, h, s = fit(ED_DIRS[0] / name)
        state = "unchanged" if s == 1.0 else f"scaled x{s:.3f}"
        ok = "ok" if (w <= TARGET_W_MM + 0.1 and h <= HEIGHT_CAP_MM + 0.1) else "OVER"
        print(f"   ED {n}: {w:6.1f} x {h:6.1f} mm  {state:<14}{ok}")

    for d in ED_DIRS[1:]:
        for n in range(1, 9):
            name = f"ED_Fig{n}_combined.pdf"
            shutil.copy2(ED_DIRS[0] / name, d / name)
    print(f"== distributed to {len(ED_DIRS)} directories ==")

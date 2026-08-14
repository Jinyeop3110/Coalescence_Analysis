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

Sizing follows the same guide:
  width   180 mm, the two-column standard for original research
  height  capped per figure by caption length, since the guide's maximum
          height depends on it: <300 words ~185 mm, <150 words ~210 mm,
          <50 words ~225 mm at two-column width
Every item also stays inside A4 (210 x 297 mm), which the editor requires
separately. 180 mm satisfies both.

Panel labels are set lowercase bold, matching every caption in the manuscript
and Nature house style. They are 8 pt: the guide's 5-7 pt range governs text
inside the figure, while panel letters are conventionally set slightly larger.

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

# Maximum height per figure, from caption word count measured against the
# guide's table. Recheck these if a caption crosses 50, 150 or 300 words.
HEIGHT_CAP_MM = {1: 210, 2: 210, 3: 185, 4: 210, 5: 210, 6: 185, 7: 185, 8: 185}

ED_DIRS = [
    V5 / "latex/figures/extended_data",
    V5 / "revision_submission/00_submit_new/Main_Manuscript_Revised_LaTeX_Source/figures/extended_data",
    V5 / "revision_submission/00_submit_new/Supplementary_Information_LaTeX_Source/figures/extended_data",
    V5 / "revision_submission/00_submit_new/Extended_Data_Figures",
]

MARGIN_MM = 6.0
COL_GAP_MM = 4.0
ROW_GAP_MM = 7.0
LABEL_GAP_MM = 5.5
LABEL_PT = 8.0

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

    # First pass: work out each row's panel box, and the total height.
    plan, total_h = [], 2 * MARGIN_MM
    for idxs, rule in spec["rows"]:
        w = cell_w if rule == "cells" else content_w * float(rule)
        heights = [w * (srcs[i].load_page(0).rect.height / srcs[i].load_page(0).rect.width)
                   for i in idxs]
        row_h = max(heights)
        plan.append((idxs, w, heights, row_h))
        total_h += LABEL_GAP_MM + row_h
    total_h += ROW_GAP_MM * (len(plan) - 1)

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
            x += w + COL_GAP_MM
            k += 1
        y += row_h + ROW_GAP_MM

    doc.save(out_path, deflate=True, garbage=4)
    doc.close()
    for s in srcs:
        s.close()
    return TARGET_W_MM, total_h


def fit(path, num):
    """Scale a page down to the 180 mm width and its caption-derived height cap."""
    src = fitz.open(path)
    r = src.load_page(0).rect
    w_mm, h_mm = r.width / MM, r.height / MM
    cap = HEIGHT_CAP_MM[num]
    scale = min(TARGET_W_MM / w_mm, cap / h_mm, 1.0)
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
        print(f"   ED {num}: {w:.1f} x {h:.1f} mm  (cap {HEIGHT_CAP_MM[num]} mm)")

    print(f"== sizing every item to {TARGET_W_MM:.0f} mm and its height cap ==")
    for n in range(1, 9):
        name = f"ED_Fig{n}_combined.pdf"
        w, h, s = fit(ED_DIRS[0] / name, n)
        state = "unchanged" if s == 1.0 else f"scaled x{s:.3f}"
        ok = "ok" if (w <= TARGET_W_MM + 0.1 and h <= HEIGHT_CAP_MM[n] + 0.1) else "OVER"
        print(f"   ED {n}: {w:6.1f} x {h:6.1f} mm  {state:<14}{ok}")

    for d in ED_DIRS[1:]:
        for n in range(1, 9):
            name = f"ED_Fig{n}_combined.pdf"
            shutil.copy2(ED_DIRS[0] / name, d / name)
    print(f"== distributed to {len(ED_DIRS)} directories ==")

#!/usr/bin/env python3
"""Ensure DOCX character styles used by Pandoc conversion are present."""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", W)


STYLES = {
    "RevisionRed": "FF0000",
    "ManuscriptEditRed": "960000",
    "ReviewerBlue": "0096DC",
    "StatusGray": "5A5A5A",
}


def qn(name: str) -> str:
    return f"{{{W}}}{name}"


def attr(name: str) -> str:
    return qn(name)


def make_character_style(style_id: str, color: str) -> ET.Element:
    style = ET.Element(qn("style"))
    style.set(attr("type"), "character")
    style.set(attr("customStyle"), "1")
    style.set(attr("styleId"), style_id)

    name = ET.SubElement(style, qn("name"))
    name.set(attr("val"), style_id)

    based_on = ET.SubElement(style, qn("basedOn"))
    based_on.set(attr("val"), "DefaultParagraphFont")

    priority = ET.SubElement(style, qn("uiPriority"))
    priority.set(attr("val"), "1")
    ET.SubElement(style, qn("qFormat"))

    rpr = ET.SubElement(style, qn("rPr"))
    color_el = ET.SubElement(rpr, qn("color"))
    color_el.set(attr("val"), color)
    return style


def patch_styles(styles_path: Path) -> None:
    tree = ET.parse(styles_path)
    root = tree.getroot()

    for style_id, color in STYLES.items():
        pattern = f".//{qn('style')}[@{attr('styleId')}='{style_id}']"
        existing = root.find(pattern)
        if existing is not None:
            root.remove(existing)
        root.append(make_character_style(style_id, color))

    tree.write(styles_path, encoding="UTF-8", xml_declaration=True)


def patch_docx(input_docx: Path, output_docx: Path) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        with ZipFile(input_docx, "r") as zin:
            zin.extractall(tmpdir_path)

        styles_path = tmpdir_path / "word" / "styles.xml"
        if not styles_path.exists():
            raise RuntimeError(f"{input_docx} does not contain word/styles.xml")
        patch_styles(styles_path)

        tmp_output = output_docx.with_suffix(output_docx.suffix + ".tmp")
        with ZipFile(tmp_output, "w", ZIP_DEFLATED) as zout:
            for path in sorted(tmpdir_path.rglob("*")):
                if path.is_file():
                    zout.write(path, path.relative_to(tmpdir_path).as_posix())
        shutil.move(tmp_output, output_docx)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: ensure_submission_color_styles.py INPUT.docx OUTPUT.docx", file=sys.stderr)
        return 2

    patch_docx(Path(sys.argv[1]), Path(sys.argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

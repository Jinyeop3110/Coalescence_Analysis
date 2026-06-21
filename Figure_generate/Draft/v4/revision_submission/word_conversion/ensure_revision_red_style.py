#!/usr/bin/env python3
"""Ensure a DOCX contains a red character style named RevisionRed."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path


REVISION_STYLE = (
    '<w:style w:type="character" w:customStyle="1" w:styleId="RevisionRed">'
    '<w:name w:val="RevisionRed"/>'
    '<w:basedOn w:val="DefaultParagraphFont"/>'
    '<w:uiPriority w:val="1"/>'
    '<w:qFormat/>'
    '<w:rPr><w:color w:val="FF0000"/></w:rPr>'
    '</w:style>'
)


def patch_styles(styles_xml: str) -> str:
    pattern = re.compile(
        r'<w:style\b[^>]*\bw:styleId="RevisionRed"[\s\S]*?</w:style>'
    )
    if pattern.search(styles_xml):
        return pattern.sub(REVISION_STYLE, styles_xml, count=1)
    return styles_xml.replace("</w:styles>", REVISION_STYLE + "</w:styles>")


def patch_docx(input_path: Path, output_path: Path) -> None:
    with zipfile.ZipFile(input_path, "r") as zin:
        entries = {name: zin.read(name) for name in zin.namelist()}

    styles_name = "word/styles.xml"
    if styles_name not in entries:
        raise RuntimeError(f"{input_path} does not contain {styles_name}")

    styles_xml = entries[styles_name].decode("utf-8")
    entries[styles_name] = patch_styles(styles_xml).encode("utf-8")

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for name, data in entries.items():
            zout.writestr(name, data)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: ensure_revision_red_style.py INPUT.docx OUTPUT.docx", file=sys.stderr)
        return 2
    patch_docx(Path(sys.argv[1]), Path(sys.argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

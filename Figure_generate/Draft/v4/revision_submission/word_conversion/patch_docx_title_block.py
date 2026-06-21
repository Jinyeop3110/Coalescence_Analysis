#!/usr/bin/env python3
"""Patch the converted DOCX title block with author affiliations."""

from __future__ import annotations

import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W}


def qn(namespace: str, tag: str) -> str:
    return f"{{{namespace}}}{tag}"


def paragraph_style(paragraph: ET.Element) -> str | None:
    style = paragraph.find("w:pPr/w:pStyle", NS)
    return None if style is None else style.get(qn(W, "val"))


def text_run(text: str, superscript: bool = False) -> ET.Element:
    run = ET.Element(qn(W, "r"))
    if superscript:
        run_pr = ET.SubElement(run, qn(W, "rPr"))
        vert = ET.SubElement(run_pr, qn(W, "vertAlign"))
        vert.set(qn(W, "val"), "superscript")
    text_el = ET.SubElement(run, qn(W, "t"))
    text_el.set(qn(XML, "space"), "preserve")
    text_el.text = text
    return run


def make_paragraph(style_name: str, runs: list[ET.Element]) -> ET.Element:
    paragraph = ET.Element(qn(W, "p"))
    p_pr = ET.SubElement(paragraph, qn(W, "pPr"))
    style = ET.SubElement(p_pr, qn(W, "pStyle"))
    style.set(qn(W, "val"), style_name)
    for run in runs:
        paragraph.append(run)
    return paragraph


def patch_title_block(document_xml: bytes) -> bytes:
    ET.register_namespace("w", W)
    root = ET.fromstring(document_xml)
    body = root.find("w:body", NS)
    if body is None:
        raise RuntimeError("DOCX document body not found")

    children = list(body)
    title_index = next(
        (index for index, child in enumerate(children) if child.tag == qn(W, "p") and paragraph_style(child) == "Title"),
        None,
    )
    if title_index is None:
        raise RuntimeError("Title paragraph not found")

    author_start = title_index + 1
    author_end = author_start
    while author_end < len(children) and children[author_end].tag == qn(W, "p") and paragraph_style(children[author_end]) == "Author":
        author_end += 1

    if author_end == author_start:
        raise RuntimeError("Author paragraphs not found after title")

    for child in children[author_start:author_end]:
        body.remove(child)

    author_line = make_paragraph(
        "Author",
        [
            text_run("Jinyeop Song"),
            text_run("1", superscript=True),
            text_run(", Jiliang Hu"),
            text_run("1", superscript=True),
            text_run(", and Jeff Gore"),
            text_run("1", superscript=True),
        ],
    )
    affiliation_line = make_paragraph(
        "Author",
        [
            text_run("1", superscript=True),
            text_run("Department of Physics, Massachusetts Institute of Technology, Cambridge, MA, USA"),
        ],
    )

    body.insert(author_start, author_line)
    body.insert(author_start + 1, affiliation_line)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: patch_docx_title_block.py INPUT.docx OUTPUT.docx", file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    target.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(source, "r") as zin:
        document_xml = patch_title_block(zin.read("word/document.xml"))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp_path = Path(tmp.name)
        try:
            with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    data = document_xml if item.filename == "word/document.xml" else zin.read(item.filename)
                    zout.writestr(item, data)
            shutil.move(str(tmp_path), target)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    print("patched title author/affiliation block")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

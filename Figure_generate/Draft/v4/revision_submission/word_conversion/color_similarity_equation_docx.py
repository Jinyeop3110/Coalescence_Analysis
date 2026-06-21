#!/usr/bin/env python3
"""Color the converted cosine-similarity equation red in a DOCX copy."""

from __future__ import annotations

import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"w": W, "m": M}


def qn(namespace: str, tag: str) -> str:
    return f"{{{namespace}}}{tag}"


def ensure_run_revision_red(math_run: ET.Element) -> None:
    insert_at = 0
    if len(math_run) and math_run[0].tag == qn(M, "rPr"):
        insert_at = 1

    run_pr = math_run.find("w:rPr", NS)
    if run_pr is None:
        run_pr = ET.Element(qn(W, "rPr"))
        math_run.insert(insert_at, run_pr)

    if run_pr.find("w:rStyle", NS) is None:
        style = ET.Element(qn(W, "rStyle"))
        style.set(qn(W, "val"), "RevisionRed")
        run_pr.insert(0, style)

    color = run_pr.find("w:color", NS)
    if color is None:
        color = ET.SubElement(run_pr, qn(W, "color"))
    color.set(qn(W, "val"), "FF0000")


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//m:t", NS))


def color_similarity_equation(document_xml: bytes) -> tuple[bytes, int]:
    ET.register_namespace("w", W)
    ET.register_namespace("m", M)

    root = ET.fromstring(document_xml)
    patched_runs = 0

    for paragraph in root.findall(".//w:p", NS):
        text = paragraph_text(paragraph)
        if "Sim(C,A)=" not in text.replace(" ", ""):
            continue
        if "Sim(C,B)=" not in text.replace(" ", ""):
            continue

        for math_run in paragraph.findall(".//m:r", NS):
            ensure_run_revision_red(math_run)
            patched_runs += 1
        break

    if patched_runs == 0:
        raise RuntimeError("Could not find the converted similarity-equation paragraph")

    return ET.tostring(root, encoding="utf-8", xml_declaration=True), patched_runs


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: color_similarity_equation_docx.py INPUT.docx OUTPUT.docx", file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    target.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(source, "r") as zin:
        document_xml, patched_runs = color_similarity_equation(zin.read("word/document.xml"))
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

    print(f"patched {patched_runs} math runs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

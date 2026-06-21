#!/usr/bin/env python3
"""Apply conservative Nature-style formatting to a derived DOCX manuscript.

This script edits only DOCX OOXML style/section metadata and one generated
Pandoc heading. It does not edit the source LaTeX manuscript.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "wp14": "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

W = f"{{{NS['w']}}}"


def qn(local: str) -> str:
    return f"{W}{local}"


def attr(local: str) -> str:
    return qn(local)


def get_or_add(parent: ET.Element, tag: str) -> ET.Element:
    child = parent.find(qn(tag))
    if child is None:
        child = ET.SubElement(parent, qn(tag))
    return child


def remove_children(parent: ET.Element, tags: set[str]) -> None:
    qualified = {qn(tag) for tag in tags}
    for child in list(parent):
        if child.tag in qualified:
            parent.remove(child)


def set_spacing(ppr: ET.Element, *, before: str = "0", after: str = "120", line: str = "480") -> None:
    remove_children(ppr, {"spacing"})
    spacing = ET.SubElement(ppr, qn("spacing"))
    spacing.set(attr("before"), before)
    spacing.set(attr("after"), after)
    spacing.set(attr("line"), line)
    spacing.set(attr("lineRule"), "auto")


def set_justification(ppr: ET.Element, value: str | None) -> None:
    remove_children(ppr, {"jc"})
    if value:
        jc = ET.SubElement(ppr, qn("jc"))
        jc.set(attr("val"), value)


def set_outline_level(ppr: ET.Element, level: str | None) -> None:
    remove_children(ppr, {"outlineLvl"})
    if level is not None:
        outline = ET.SubElement(ppr, qn("outlineLvl"))
        outline.set(attr("val"), level)


def set_run_format(rpr: ET.Element, *, size: str = "24", bold: bool | None = None) -> None:
    remove_children(rpr, {"rFonts", "sz", "szCs", "b", "bCs"})

    fonts = ET.SubElement(rpr, qn("rFonts"))
    fonts.set(attr("ascii"), "Times New Roman")
    fonts.set(attr("hAnsi"), "Times New Roman")
    fonts.set(attr("cs"), "Times New Roman")

    sz = ET.SubElement(rpr, qn("sz"))
    sz.set(attr("val"), size)
    sz_cs = ET.SubElement(rpr, qn("szCs"))
    sz_cs.set(attr("val"), size)

    if bold is True:
        ET.SubElement(rpr, qn("b"))
        ET.SubElement(rpr, qn("bCs"))


def style_by_id(styles_root: ET.Element, style_id: str) -> ET.Element | None:
    for style in styles_root.findall(qn("style")):
        if style.get(attr("styleId")) == style_id:
            return style
    return None


def set_paragraph_style(
    styles_root: ET.Element,
    style_id: str,
    *,
    size: str = "24",
    bold: bool | None = None,
    spacing_line: str = "480",
    spacing_after: str = "120",
    spacing_before: str = "0",
    justification: str | None = None,
    outline_level: str | None = None,
) -> None:
    style = style_by_id(styles_root, style_id)
    if style is None:
        return

    ppr = get_or_add(style, "pPr")
    set_spacing(ppr, before=spacing_before, after=spacing_after, line=spacing_line)
    set_justification(ppr, justification)
    set_outline_level(ppr, outline_level)

    rpr = get_or_add(style, "rPr")
    set_run_format(rpr, size=size, bold=bold)


def normalize_styles(styles_root: ET.Element) -> None:
    doc_defaults = get_or_add(styles_root, "docDefaults")
    rpr_default = get_or_add(doc_defaults, "rPrDefault")
    rpr = get_or_add(rpr_default, "rPr")
    set_run_format(rpr, size="24", bold=None)

    ppr_default = get_or_add(doc_defaults, "pPrDefault")
    ppr = get_or_add(ppr_default, "pPr")
    set_spacing(ppr, line="480")

    for style_id in [
        "Normal",
        "BodyText",
        "FirstParagraph",
        "Abstract",
        "Bibliography",
        "BlockText",
        "Definition",
        "FootnoteText",
    ]:
        set_paragraph_style(styles_root, style_id, size="24", spacing_line="480")

    for style_id in ["Caption", "ImageCaption", "TableCaption", "Figure", "CaptionedFigure"]:
        set_paragraph_style(styles_root, style_id, size="22", spacing_line="360", spacing_after="120")

    set_paragraph_style(
        styles_root,
        "Title",
        size="28",
        bold=True,
        spacing_line="360",
        spacing_after="120",
        justification="center",
    )
    set_paragraph_style(
        styles_root,
        "Author",
        size="24",
        spacing_line="360",
        spacing_after="80",
        justification="center",
    )
    set_paragraph_style(
        styles_root,
        "AbstractTitle",
        size="24",
        bold=True,
        spacing_line="480",
        spacing_after="120",
    )

    for style_id, level in [("Heading1", "0"), ("Heading2", "1"), ("Heading3", "2")]:
        set_paragraph_style(
            styles_root,
            style_id,
            size="24",
            bold=True,
            spacing_line="480",
            spacing_before="240",
            spacing_after="120",
            outline_level=level,
        )


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(text.text or "" for text in paragraph.findall(".//" + qn("t")))


def paragraph_style(paragraph: ET.Element) -> str | None:
    ppr = paragraph.find(qn("pPr"))
    if ppr is None:
        return None
    pstyle = ppr.find(qn("pStyle"))
    if pstyle is None:
        return None
    return pstyle.get(attr("val"))


def remove_generated_introduction_heading(document_root: ET.Element) -> bool:
    # Preserve the LaTeX section structure in the Word submission file.
    # Earlier conversion drafts removed this heading for a journal-style
    # manuscript layout, but the current DOCX should match the source.
    return False


def normalize_section_properties(document_root: ET.Element) -> int:
    count = 0
    for sect in document_root.findall(".//" + qn("sectPr")):
        remove_children(sect, {"lnNumType"})
        ln = ET.SubElement(sect, qn("lnNumType"))
        ln.set(attr("countBy"), "1")
        ln.set(attr("restart"), "continuous")

        pg_mar = sect.find(qn("pgMar"))
        if pg_mar is None:
            pg_mar = ET.SubElement(sect, qn("pgMar"))
        pg_mar.set(attr("top"), "1440")
        pg_mar.set(attr("right"), "1440")
        pg_mar.set(attr("bottom"), "1440")
        pg_mar.set(attr("left"), "1440")
        pg_mar.set(attr("header"), "720")
        pg_mar.set(attr("footer"), "720")
        pg_mar.set(attr("gutter"), "0")
        count += 1
    return count


def patch_docx(input_docx: Path, output_docx: Path) -> tuple[bool, int]:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        with ZipFile(input_docx, "r") as zin:
            zin.extractall(tmpdir_path)

        styles_path = tmpdir_path / "word" / "styles.xml"
        document_path = tmpdir_path / "word" / "document.xml"

        styles_root = ET.parse(styles_path).getroot()
        normalize_styles(styles_root)
        ET.ElementTree(styles_root).write(styles_path, encoding="UTF-8", xml_declaration=True)

        document_tree = ET.parse(document_path)
        document_root = document_tree.getroot()
        removed_intro = remove_generated_introduction_heading(document_root)
        section_count = normalize_section_properties(document_root)
        document_tree.write(document_path, encoding="UTF-8", xml_declaration=True)

        tmp_output = output_docx.with_suffix(output_docx.suffix + ".tmp")
        with ZipFile(tmp_output, "w", ZIP_DEFLATED) as zout:
            for path in sorted(tmpdir_path.rglob("*")):
                if path.is_file():
                    zout.write(path, path.relative_to(tmpdir_path).as_posix())
        shutil.move(tmp_output, output_docx)

    return removed_intro, section_count


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: format_nature_eco_evo_docx.py INPUT.docx OUTPUT.docx", file=sys.stderr)
        return 2

    input_docx = Path(sys.argv[1])
    output_docx = Path(sys.argv[2])
    if not input_docx.exists():
        print(f"Input DOCX not found: {input_docx}", file=sys.stderr)
        return 1

    removed_intro, section_count = patch_docx(input_docx, output_docx)
    print(f"removed_generated_introduction_heading={removed_intro}")
    print(f"sections_with_line_numbers_and_one_inch_margins={section_count}")
    print(f"output={output_docx}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

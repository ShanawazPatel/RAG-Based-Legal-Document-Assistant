#!/usr/bin/env python3
"""Generate a PDF containing the project's README and source files.

Usage:
    pip install -r requirements.txt
    python generate_project_pdf.py

Output:
    project_details.pdf (created in the current directory)
"""
import os
import sys
from pathlib import Path

try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
except Exception as e:
    print("Missing dependency: reportlab. Install with: pip install reportlab")
    raise


def collect_files(root: Path):
    # Include README and all Python files in the root directory
    candidates = []
    readme = root / "README.md"
    if readme.exists():
        candidates.append(readme)

    for p in sorted(root.glob("*.py")):
        candidates.append(p)

    # Optionally include other docs
    for p in sorted(root.glob("*.md")):
        if p.name.upper() != "README.MD":
            candidates.append(p)

    return candidates


def make_pdf(files, out_path: Path, project_name: str):
    doc = SimpleDocTemplate(str(out_path), pagesize=letter,
                            rightMargin=36, leftMargin=36,
                            topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = ParagraphStyle("Heading", parent=styles["Heading2"], spaceBefore=12, spaceAfter=6)
    code_style = ParagraphStyle("Code", fontName="Courier", fontSize=8, leading=10)

    elems = []
    elems.append(Paragraph(f"Project Details: {project_name}", title_style))
    elems.append(Spacer(1, 12))

    for path in files:
        elems.append(Paragraph(f"File: {path.name}", heading_style))
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            try:
                text = path.read_text(encoding="latin-1")
            except Exception:
                text = "<Could not read file>"

        # Ensure the Preformatted block is not enormous per page; reportlab will wrap.
        elems.append(Preformatted(text, code_style))
        elems.append(Spacer(1, 12))

    doc.build(elems)


def main():
    root = Path.cwd()
    out = root / "project_details.pdf"
    files = collect_files(root)
    if not files:
        print("No files found to include. Make sure you're in the project root.")
        sys.exit(1)

    project_name = root.name
    print(f"Generating PDF with {len(files)} files into: {out}")
    make_pdf(files, out, project_name)
    print(f"Done. Open '{out.name}' to view the project details.")


if __name__ == "__main__":
    main()

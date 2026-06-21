#!/usr/bin/env python3
"""
Combine individual subplot PDFs into single Extended Data figures.
Uses PyMuPDF (fitz) for PDF handling.
Adds subplot labels (a, b, c, ...) to each panel.
"""

import os
import shutil
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import io


FIGDIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_DIR = os.path.join(FIGDIR, 'archive')


def pdf_to_image(pdf_path, dpi=300):
    """Convert PDF to PIL Image using PyMuPDF."""
    doc = fitz.open(pdf_path)
    page = doc[0]
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))
    doc.close()
    return img


def add_label_to_image(img, label, font_size=60, margin_size=80):
    """Add a bold label (a, b, c, etc.) by adding a margin on top-left corner."""
    # Create new image with margin on left and top
    new_width = img.width + margin_size
    new_height = img.height + margin_size
    new_img = Image.new('RGB', (new_width, new_height), 'white')

    # Paste original image offset by margin
    new_img.paste(img, (margin_size, margin_size))

    draw = ImageDraw.Draw(new_img)

    # Try to use a bold font, fall back to default if not available
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()

    # Draw the label in the margin area (top-left)
    label_offset = (15, 15)
    draw.text(label_offset, label, fill='black', font=font)

    return new_img


def resize_image(img, scale_factor):
    """Resize image by a scale factor."""
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)
    return img.resize((new_width, new_height), Image.LANCZOS)


def combine_images_grid(images, grid_layout, labels=None, spacing=40, row_scales=None):
    """
    Combine images in a grid layout with optional labels.

    images: list of PIL Images
    grid_layout: list of lists, each inner list contains indices for that row
    labels: list of labels (e.g., ['a', 'b', 'c', ...]) or None
    spacing: pixels between images
    row_scales: dict mapping row index to scale factor (e.g., {0: 1.5, 1: 1.5} to enlarge rows 0 and 1)
    """
    # Apply labels to images
    labeled_images = []
    for i, img in enumerate(images):
        if labels and i < len(labels):
            labeled_img = add_label_to_image(img, labels[i])
            labeled_images.append(labeled_img)
        else:
            labeled_images.append(img)

    # Apply row scaling if specified
    if row_scales:
        scaled_images = labeled_images.copy()
        for row_idx, row_indices in enumerate(grid_layout):
            if row_idx in row_scales:
                scale = row_scales[row_idx]
                for img_idx in row_indices:
                    scaled_images[img_idx] = resize_image(labeled_images[img_idx], scale)
        labeled_images = scaled_images

    # Calculate row dimensions
    rows_data = []
    max_width = 0

    for row_indices in grid_layout:
        row_images = [labeled_images[i] for i in row_indices]
        row_height = max(img.height for img in row_images)
        row_width = sum(img.width for img in row_images) + spacing * (len(row_images) - 1)
        max_width = max(max_width, row_width)
        rows_data.append((row_images, row_width, row_height))

    total_height = sum(r[2] for r in rows_data) + spacing * (len(rows_data) - 1)

    # Create combined image
    combined = Image.new('RGB', (max_width, total_height), 'white')

    y_offset = 0
    for row_images, row_width, row_height in rows_data:
        x_start = (max_width - row_width) // 2
        x_offset = x_start
        for img in row_images:
            y_img_offset = y_offset + (row_height - img.height) // 2
            combined.paste(img, (x_offset, y_img_offset))
            x_offset += img.width + spacing
        y_offset += row_height + spacing

    return combined


def combine_figure(input_files, grid_layout, output_name, labels=None, dpi=300, row_scales=None):
    """
    Combine multiple PDF files into a single figure with labels.

    input_files: list of PDF file paths (relative to ARCHIVE_DIR)
    grid_layout: list of lists indicating image indices per row
    output_name: output PDF filename
    labels: list of labels for each panel (e.g., ['a', 'b', 'c'])
    row_scales: dict mapping row index to scale factor
    """
    print(f"Creating {output_name}...")

    # Convert all PDFs to images
    images = []
    for f in input_files:
        # Check archive folder first, then main folder
        filepath = os.path.join(ARCHIVE_DIR, f)
        if not os.path.exists(filepath):
            filepath = os.path.join(FIGDIR, f)

        if os.path.exists(filepath):
            img = pdf_to_image(filepath, dpi=dpi)
            images.append(img)
            print(f"  Loaded: {f}")
        else:
            print(f"  WARNING: File not found: {f}")
            return False

    # Generate default labels if not provided
    if labels is None:
        labels = [chr(ord('a') + i) for i in range(len(images))]

    # Combine images
    combined = combine_images_grid(images, grid_layout, labels=labels, spacing=50, row_scales=row_scales)

    # Save as PDF
    output_path = os.path.join(FIGDIR, output_name)
    combined.save(output_path, 'PDF', resolution=300)
    print(f"  Saved: {output_name}\n")
    return True


def copy_file(src_name, dst_name):
    """Copy a file from archive to main folder."""
    src = os.path.join(ARCHIVE_DIR, src_name)
    if not os.path.exists(src):
        src = os.path.join(FIGDIR, src_name)
    dst = os.path.join(FIGDIR, dst_name)
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"Copied: {src_name} -> {dst_name}\n")
        return True
    else:
        print(f"WARNING: Source not found: {src_name}\n")
        return False


def main():
    print("=" * 60)
    print("Combining Extended Data figures with labels...")
    print("=" * 60 + "\n")

    # ED Fig 1: Taxonomy color map (from supplementary_figs)
    copy_file('../../supplementary_figs/taxonomy_color_map.pdf', 'ED_Fig1_combined.pdf')

    # (Time series moved to Supplementary)

    # ED Fig 2: Robustness across similarity metrics
    copy_file('ED_Fig7_robustness_metrics.pdf', 'ED_Fig2_combined.pdf')

    # ED Fig 3: Event-matched additive null model
    copy_file('../../supplementary_figs/Fig_R3_2_additive_null_comparison.pdf', 'ED_Fig3_combined.pdf')

    # ED Fig 4: Species number ablation (5 phase diagrams + 1 bar plot)
    combine_figure(
        input_files=[
            'ED_Fig4a_4species.pdf',
            'ED_Fig4b_6species.pdf',
            'ED_Fig4c_12species.pdf',
            'ED_Fig4d_24species.pdf',
            'ED_Fig4e_48species.pdf',
            'ED_Fig4f_species_ablation_bar.pdf',
        ],
        grid_layout=[[0, 1, 2], [3, 4], [5]],
        output_name='ED_Fig4_combined.pdf',
        labels=['a', 'b', 'c', 'd', 'e', 'f'],
        row_scales={0: 1.8, 1: 1.8}  # Scale up rows 0 and 1 (phase diagrams)
    )

    # ED Fig 5: Pairwise selection correlation simulation (3 bar plots + 1 line plot)
    combine_figure(
        input_files=[
            'ED_Fig2a_correlation_u0.3.pdf',
            'ED_Fig2b_correlation_u0.6.pdf',
            'ED_Fig2c_correlation_u0.8.pdf',
            'ED_Fig2d_correlation_vs_mu.pdf',
        ],
        grid_layout=[[0, 1, 2], [3]],
        output_name='ED_Fig5_combined.pdf',
        labels=['a', 'b', 'c', 'd']
    )

    # ED Fig 6: Pairwise selection correlation experimental (3 panels)
    combine_figure(
        input_files=[
            'ED_Fig3a_correlation_Nutr-.pdf',
            'ED_Fig3b_correlation_Base.pdf',
            'ED_Fig3c_correlation_Nutr+.pdf',
        ],
        grid_layout=[[0, 1, 2]],
        output_name='ED_Fig6_combined.pdf',
        labels=['a', 'b', 'c']
    )

    # ED Fig 7: Assembly effect simulation (already single file, no label needed)
    copy_file('ED_Fig5_assembly_effect_simulation.pdf', 'ED_Fig7_combined.pdf')

    # ED Fig 8: pH vs outcome (already single file, has a/b panels already)
    copy_file('ED_Fig8_pH_vs_outcome.pdf', 'ED_Fig8_combined.pdf')

    print("=" * 60)
    print("Done! Combined figures created with subplot labels.")
    print("=" * 60)


if __name__ == '__main__':
    main()

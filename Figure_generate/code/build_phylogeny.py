"""
Phylogenetic Tree Builder
Builds a phylogenetic tree from 16S rRNA sequences in Species_phylogeny.xlsx
Uses Neighbor-Joining with distance-based method.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from Bio import SeqIO, Phylo
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.Align import MultipleSeqAlignment
import random
import os


def settingTheColor(seed=4):
    """Generate and shuffle color palette for ASV visualization.
    Uses inferno colormap to match pie charts in generate_pie_plots.py."""
    np.random.seed(seed)
    try:
        inferno = plt.colormaps.get_cmap('inferno').resampled(50)
    except AttributeError:
        from matplotlib import cm as mpl_cm
        inferno = mpl_cm.get_cmap('inferno', 50)
    colors = [inferno(i)[:3] for i in range(50)]
    np.random.shuffle(colors)
    return colors


def load_phylogeny_data(filepath):
    """Load Species_phylogeny.xlsx with 50 ASVs and their 16S sequences."""
    df = pd.read_excel(filepath, sheet_name='Organized')
    print(f"Loaded {len(df)} ASVs from phylogeny data")
    return df


def create_fasta_file(df, output_path):
    """Create FASTA file from 16S rRNA sequences."""
    records = []
    for idx, row in df.iterrows():
        asv_id = str(row['ASV index'])
        genus = str(row['Genus']) if pd.notna(row['Genus']) else 'Unknown'
        sequence = str(row['16s rRNA'])

        # Create header with ASV and genus
        header = f"{asv_id}|{genus}"
        record = SeqRecord(Seq(sequence), id=asv_id, description=genus)
        records.append(record)

    # Write FASTA file
    SeqIO.write(records, output_path, "fasta")
    print(f"Created FASTA file: {output_path} with {len(records)} sequences")
    return records


def create_metadata_tsv(df, output_path):
    """Generate metadata TSV from taxonomy columns."""
    metadata = df[['ASV index', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus']].copy()
    metadata.to_csv(output_path, sep='\t', index=False)
    print(f"Created metadata TSV: {output_path}")
    return metadata


def create_color_mapping_tsv(df, output_path):
    """Generate ASV color mapping TSV."""
    color_map = settingTheColor()

    color_data = []
    for idx, row in df.iterrows():
        asv_id = str(row['ASV index'])
        color = color_map[idx]
        # Convert RGB tuple to hex
        hex_color = '#%02x%02x%02x' % (int(color[0]*255), int(color[1]*255), int(color[2]*255))
        color_data.append({'ASV': asv_id, 'Color': hex_color})

    color_df = pd.DataFrame(color_data)
    color_df.to_csv(output_path, sep='\t', index=False)
    print(f"Created color mapping TSV: {output_path}")
    return color_df


def compute_distance_matrix(records):
    """Compute pairwise distance matrix using BioPython."""
    # Pad sequences to same length (for alignment)
    sequences = [str(rec.seq) for rec in records]
    max_len = max(len(s) for s in sequences)

    # Pad shorter sequences with gaps
    padded_sequences = []
    for seq in sequences:
        if len(seq) < max_len:
            seq = seq + '-' * (max_len - len(seq))
        padded_sequences.append(Seq(seq))

    # Create alignment object
    alignment = MultipleSeqAlignment([SeqRecord(seq, id=rec.id) for seq, rec in zip(padded_sequences, records)])

    # Calculate distance matrix
    calculator = DistanceCalculator('identity')  # or 'blastn' for more sophisticated
    dm = calculator.get_distance(alignment)

    print(f"Computed distance matrix: {len(dm.names)} x {len(dm.names)}")
    return dm


def build_neighbor_joining_tree(distance_matrix):
    """Build Neighbor-Joining tree from distance matrix."""
    constructor = DistanceTreeConstructor()
    tree = constructor.nj(distance_matrix)

    print("Built Neighbor-Joining tree")
    return tree


def export_distance_matrix_excel(distance_matrix, output_path):
    """Export distance matrix to Excel file."""
    # Convert to DataFrame
    matrix_data = []
    for i, name1 in enumerate(distance_matrix.names):
        row = [name1]
        for j, name2 in enumerate(distance_matrix.names):
            row.append(distance_matrix[i, j])
        matrix_data.append(row)

    df = pd.DataFrame(matrix_data, columns=['ASV'] + distance_matrix.names)
    df.to_excel(output_path, index=False)
    print(f"Exported distance matrix to: {output_path}")


def export_tree_newick(tree, output_path):
    """Export tree to Newick format."""
    Phylo.write(tree, output_path, 'newick')
    print(f"Exported tree to Newick: {output_path}")


def get_asv_abundances(df_phylo, processed_sequences_path):
    """Extract abundances for phylogeny ASVs from processed sequences."""
    # Load processed sequences
    df_seq = pd.read_excel(processed_sequences_path)

    # Extract ASV columns (NormalizedAbundance1, NormalizedAbundance2, etc.)
    abundance_cols = [col for col in df_seq.columns if col.startswith('NormalizedAbundance')]

    # Create abundance matrix for phylogeny ASVs
    abundances = {}
    for idx, row in df_phylo.iterrows():
        asv_id = str(row['ASV index'])
        # Extract ASV number (e.g., ASV1 -> 1)
        asv_num = int(asv_id.replace('ASV', ''))

        # Get corresponding abundance column
        col_name = f'NormalizedAbundance{asv_num}'
        if col_name in abundance_cols:
            # Calculate mean abundance across all samples
            abundances[asv_id] = df_seq[col_name].mean()
        else:
            abundances[asv_id] = 0.0

    return abundances


def plot_phylogeny_tree(tree, df_phylo, abundances, colors, output_path, figure_title="Phylogenetic Tree"):
    """
    Plot phylogenetic tree with colored rectangles for abundances.
    """
    fig, (ax_tree, ax_bars) = plt.subplots(1, 2, figsize=(12, 10),
                                            gridspec_kw={'width_ratios': [3, 1]})

    # Draw tree using BioPython
    Phylo.draw(tree, axes=ax_tree, do_show=False, show_confidence=False)
    ax_tree.set_title(figure_title, fontsize=12, fontweight='bold')
    ax_tree.spines['top'].set_visible(False)
    ax_tree.spines['right'].set_visible(False)
    ax_tree.spines['bottom'].set_visible(False)
    ax_tree.set_xlabel('Distance')

    # Get terminal (leaf) nodes in order from tree
    terminals = tree.get_terminals()
    terminal_names = [term.name for term in terminals]

    # Draw abundance bars
    y_positions = np.arange(len(terminal_names))
    bar_heights = [abundances.get(name, 0) for name in terminal_names]

    # Get colors for each ASV
    asv_colors = []
    color_map = settingTheColor()
    for name in terminal_names:
        # Find index in original dataframe
        try:
            idx = df_phylo[df_phylo['ASV index'] == name].index[0]
            asv_colors.append(color_map[idx])
        except:
            asv_colors.append((0.5, 0.5, 0.5))  # Gray for missing

    # Plot horizontal bars
    ax_bars.barh(y_positions, bar_heights, color=asv_colors, height=0.8)
    ax_bars.set_yticks(y_positions)
    ax_bars.set_yticklabels([])  # Remove labels (already on tree)
    ax_bars.set_xlabel('Mean Abundance', fontsize=10)
    ax_bars.set_title('Abundance', fontsize=10, fontweight='bold')
    ax_bars.spines['top'].set_visible(False)
    ax_bars.spines['right'].set_visible(False)
    ax_bars.set_xlim(0, max(bar_heights) * 1.1 if max(bar_heights) > 0 else 1)

    plt.tight_layout()
    plt.savefig(output_path, format='svg', bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved phylogeny figure to: {output_path}")


def build_phylogeny_tree_advanced(tree, df_phylo, abundances, output_path):
    """
    Create a more sophisticated rectangular phylogram with abundance rectangles.
    Uses same color mapping as taxonomy_color_map.svg (sorted by ASV number).
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import matplotlib.lines as mlines

    # Sort df_phylo by ASV number (same as taxonomy colormap)
    df_phylo_sorted = df_phylo.copy()
    df_phylo_sorted['ASV_num'] = df_phylo_sorted['ASV index'].str.replace('ASV', '').astype(int)
    df_phylo_sorted = df_phylo_sorted.sort_values('ASV_num').reset_index(drop=True)

    # Remap to consecutive numbering (ASV1, ASV2, ASV3...ASV50 without gaps)
    df_phylo_sorted['ASV_remapped'] = ['ASV' + str(i+1) for i in range(len(df_phylo_sorted))]

    # Create color map matching taxonomy_color_map.svg (using inferno)
    np.random.seed(4)
    try:
        inferno = plt.colormaps.get_cmap('inferno').resampled(len(df_phylo_sorted))
    except AttributeError:
        from matplotlib import cm as mpl_cm
        inferno = mpl_cm.get_cmap('inferno', len(df_phylo_sorted))
    colors = [inferno(i)[:3] for i in range(len(df_phylo_sorted))]
    np.random.shuffle(colors)
    color_map_sorted = colors[::-1]

    # Create dictionaries mapping original ASV ID to color and remapped ID
    asv_color_dict = {}
    asv_remap_dict = {}
    for idx, row in df_phylo_sorted.iterrows():
        asv_id_original = row['ASV index']
        asv_id_remapped = row['ASV_remapped']
        asv_color_dict[asv_id_original] = color_map_sorted[idx]
        asv_remap_dict[asv_id_original] = asv_id_remapped

    # Get all terminals (leaves)
    terminals = tree.get_terminals()
    n_terminals = len(terminals)

    # Create figure with more space on the right for ASV labels
    fig, ax = plt.subplots(figsize=(12, max(8, n_terminals * 0.3)))

    # Calculate positions for leaves
    leaf_positions = {}
    y_current = 0
    for terminal in terminals:
        leaf_positions[terminal.name] = y_current
        y_current += 1

    # Recursive function to draw tree
    def get_x_positions(clade, x=0):
        """Calculate x positions (distances from root)."""
        if clade.is_terminal():
            return x
        else:
            x_positions = {}
            for child in clade.clades:
                branch_length = child.branch_length if child.branch_length else 0
                x_positions[child.name] = get_x_positions(child, x + branch_length)
            return max(x_positions.values()) if x_positions else x

    def draw_clade(clade, x=0, ax=ax):
        """Recursively draw tree branches."""
        if clade.is_terminal():
            y = leaf_positions[clade.name]
            # Draw leaf label
            genus = df_phylo[df_phylo['ASV index'] == clade.name]['Genus'].values
            genus_name = genus[0] if len(genus) > 0 and pd.notna(genus[0]) else 'Unknown'
            label = f"{clade.name} ({genus_name})"
            ax.text(x + 0.005, y, label, va='center', ha='left', fontsize=8)
            return y, y
        else:
            # Draw internal node
            y_positions_children = []
            for child in clade.clades:
                branch_length = child.branch_length if child.branch_length else 0.01
                x_child = x + branch_length

                y_min, y_max = draw_clade(child, x_child, ax)
                y_positions_children.append((y_min + y_max) / 2)

                # Draw horizontal line to child
                y_child = (y_min + y_max) / 2
                ax.plot([x, x_child], [y_child, y_child], 'k-', linewidth=0.8)

            # Draw vertical line connecting children
            y_min_clade = min(y_positions_children)
            y_max_clade = max(y_positions_children)
            ax.plot([x, x], [y_min_clade, y_max_clade], 'k-', linewidth=0.8)

            return y_min_clade, y_max_clade

    # Draw the tree
    draw_clade(tree.root, 0, ax)

    # Add abundance rectangles with matching colors
    max_x = max([tree.distance(tree.root, term) for term in terminals])
    rect_x_start = max_x + 0.01
    rect_width = max_x * 0.15
    label_x_start = rect_x_start + rect_width + 0.005

    for i, terminal in enumerate(terminals):
        y = leaf_positions[terminal.name]
        abundance = abundances.get(terminal.name, 0)

        # Get color from sorted color map (matching taxonomy_color_map.svg)
        color = asv_color_dict.get(terminal.name, (0.8, 0.8, 0.8))

        # Draw rectangle with height proportional to abundance
        rect_height = 0.8
        alpha = min(1.0, abundance * 5) if abundance > 0 else 0.1  # Scale alpha by abundance
        rect = Rectangle((rect_x_start, y - rect_height/2), rect_width, rect_height,
                         facecolor=color, edgecolor='black', linewidth=0.5, alpha=alpha)
        ax.add_patch(rect)

        # Add ASV label on the right side with matching color (only remapped ID)
        asv_remapped = asv_remap_dict.get(terminal.name, terminal.name)
        ax.text(label_x_start, y, asv_remapped, va='center', ha='left',
                fontsize=7, fontweight='bold', color=color)

    # Set axis properties
    ax.set_ylim(-0.5, n_terminals - 0.5)
    ax.set_xlim(0, label_x_start + 0.02)  # Extra space for ASV labels
    ax.set_yticks([])
    ax.set_xlabel('Evolutionary Distance', fontsize=10)
    ax.set_title('Phylogenetic Tree of 50 Bacterial Isolates (16S rRNA)',
                 fontsize=12, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path, format='svg', bbox_inches='tight', dpi=600)

    # Also save as PDF
    pdf_path = output_path.replace('.svg', '.pdf')
    plt.savefig(pdf_path, format='pdf', bbox_inches='tight', dpi=600)
    print(f"Saved advanced phylogeny figure to: {output_path}")
    print(f"Saved PDF version to: {pdf_path}")

    # Copy to supplementary_figs directory
    import shutil
    script_dir = os.path.dirname(os.path.abspath(__file__))
    supp_dir = os.path.join(script_dir, '..', 'Draft', 'v3', 'latex', 'supplementary_figs')
    supp_dir = os.path.normpath(supp_dir)
    os.makedirs(supp_dir, exist_ok=True)
    supp_svg_path = os.path.join(supp_dir, os.path.basename(output_path))
    supp_pdf_path = os.path.join(supp_dir, os.path.basename(pdf_path))
    shutil.copy2(output_path, supp_svg_path)
    shutil.copy2(pdf_path, supp_pdf_path)
    print(f"Copied to supplementary_figs: {supp_svg_path}")
    print(f"Copied to supplementary_figs: {supp_pdf_path}")

    plt.close()


def main(output_dir='Figure/Fig1_1_Plots', data_dir='Data'):
    """Main function to build phylogenetic tree."""
    print("\n" + "="*60)
    print("Building Phylogenetic Tree from Species_phylogeny.xlsx")
    print("="*60 + "\n")

    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    # Load phylogeny data
    phylo_path = os.path.join(data_dir, 'Species_phylogeny.xlsx')
    df_phylo = load_phylogeny_data(phylo_path)

    # Create FASTA file
    fasta_path = os.path.join(data_dir, 'phylogeny_sequences.fasta')
    records = create_fasta_file(df_phylo, fasta_path)

    # Create metadata TSV
    metadata_path = os.path.join(data_dir, 'phylogeny_metadata.tsv')
    create_metadata_tsv(df_phylo, metadata_path)

    # Create color mapping TSV
    colors_path = os.path.join(data_dir, 'phylogeny_colors.tsv')
    color_df = create_color_mapping_tsv(df_phylo, colors_path)

    # Compute distance matrix
    distance_matrix = compute_distance_matrix(records)

    # Export distance matrix to Excel
    distance_excel_path = os.path.join(data_dir, 'phylogeny_distances.xlsx')
    export_distance_matrix_excel(distance_matrix, distance_excel_path)

    # Build Neighbor-Joining tree
    tree = build_neighbor_joining_tree(distance_matrix)

    # Export tree to Newick format
    newick_path = os.path.join(output_dir, 'phylogeny_tree.newick')
    export_tree_newick(tree, newick_path)

    # Get abundances from processed sequences
    processed_seq_path = '../../Postprocessed/processed_Sequences_synthetic.xlsx'
    abundances = get_asv_abundances(df_phylo, processed_seq_path)

    # Plot phylogeny tree (advanced version)
    figure_path = os.path.join(output_dir, 'Fig_1-3_phylogeny_tree.svg')
    build_phylogeny_tree_advanced(tree, df_phylo, abundances, figure_path)

    print("\n" + "="*60)
    print("Phylogenetic tree generation complete!")
    print("="*60 + "\n")

    return tree, df_phylo, abundances


if __name__ == "__main__":
    tree, df_phylo, abundances = main()

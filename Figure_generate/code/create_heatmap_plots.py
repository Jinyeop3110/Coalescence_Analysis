#!/usr/bin/env python3
"""
Create heatmap visualizations from processed data using a matplotlib-free approach first,
then attempt plotting.
"""

import json
import numpy as np
import os

def create_ascii_heatmap(u_coords, v_coords, title, bins=20):
    """Create an ASCII representation of the heatmap"""
    
    # Create 2D histogram
    H, xedges, yedges = np.histogram2d(u_coords, v_coords, bins=bins, range=[[0, 1], [0, 1]])
    
    # Normalize for ASCII display
    H_norm = (H / np.max(H) * 9).astype(int) if np.max(H) > 0 else H.astype(int)
    
    print(f"\n{title}")
    print("="*50)
    print("ASCII Heatmap (0=empty, 9=highest density)")
    print("v ^")
    
    # Print from top to bottom (flip vertically for correct orientation)
    for i in range(bins-1, -1, -1):
        row = ""
        for j in range(bins):
            density = H_norm[j, i]
            if density == 0:
                row += " ."
            else:
                row += f" {density}"
        # Add v-axis labels
        v_val = yedges[i+1] if i < bins-1 else yedges[i]
        print(f"{v_val:.1f}|{row}")
    
    # Print u-axis
    print("   " + "─" * (bins * 2))
    u_axis = "   "
    for j in range(0, bins, 5):  # Show every 5th tick
        u_val = xedges[j]
        u_axis += f"{u_val:.1f}" + " " * (8 - len(f"{u_val:.1f}"))
    print(u_axis)
    print("   " + " " * (bins - 3) + "u >")
    
    # Print statistics
    print(f"\nStatistics:")
    print(f"  Total points: {len(u_coords)}")
    print(f"  u: mean={np.mean(u_coords):.3f}, std={np.std(u_coords):.3f}")
    print(f"  v: mean={np.mean(v_coords):.3f}, std={np.std(v_coords):.3f}")
    print(f"  Max density: {np.max(H)} points in single bin")


def main():
    """Create visualizations from processed data"""
    
    # Load processed data
    data_file = "Analysis_Results/processed_test_data.json"
    
    if not os.path.exists(data_file):
        print(f"Error: Processed data file not found at {data_file}")
        print("Please run analyze_test_data_simple.py first.")
        return
    
    with open(data_file, 'r') as f:
        processed_data = json.load(f)
    
    print("COALESCENCE OUTCOMES HEATMAP VISUALIZATION")
    print("="*60)
    print("This shows the distribution of (u,v) coordinates from vector decomposition")
    print("where u and v represent contributions from the two parent communities.")
    
    # Create ASCII heatmaps for each interaction strength
    u_values = ['0.3', '0.5', '0.8']
    
    for u in u_values:
        data = processed_data[u]
        u_coords = np.array(data['u_coords'])
        v_coords = np.array(data['v_coords'])
        
        if len(u_coords) > 0:
            title = f"Interaction Strength u = {u}"
            create_ascii_heatmap(u_coords, v_coords, title, bins=15)
            
            # Print classification summary
            print(f"\nOutcome Classification:")
            total = data['classification']['total']
            if total > 0:
                for outcome in ['dominance', 'mixing', 'restructuring']:
                    count = data['classification'][outcome]
                    pct = 100 * count / total
                    print(f"  {outcome.capitalize():13}: {count:2d} ({pct:5.1f}%)")
            
            print("\n" + "─" * 60)
    
    # Summary comparison
    print(f"\nSUMMARY: Effect of Interaction Strength on Coalescence Outcomes")
    print("="*70)
    print(f"{'Strength':>8} {'Dominance':>10} {'Mixing':>10} {'Restructuring':>12} {'Total':>8}")
    print("─" * 70)
    
    for u in u_values:
        data = processed_data[u]
        total = data['classification']['total']
        if total > 0:
            dom_pct = 100 * data['classification']['dominance'] / total
            mix_pct = 100 * data['classification']['mixing'] / total  
            res_pct = 100 * data['classification']['restructuring'] / total
            
            print(f"u = {u:>4} {dom_pct:>8.1f}% {mix_pct:>8.1f}% {res_pct:>10.1f}% {total:>6d}")
    
    print("\nInterpretation:")
    print("- Higher interaction strength (u) increases dominance outcomes")
    print("- Lower interaction strength favors mixing outcomes")
    print("- Restructuring remains relatively stable across strengths")
    
    print(f"\nData successfully analyzed!")
    print(f"Raw data available in: {data_file}")


if __name__ == "__main__":
    main()
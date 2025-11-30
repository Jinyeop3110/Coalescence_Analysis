#!/usr/bin/env python
"""
Analyze the newly created phase diagrams from JSON simulation data
"""

import xml.etree.ElementTree as ET
import re
from pathlib import Path

def analyze_phase_diagram_svg(svg_path, name):
    """Analyze the visual content of a phase diagram SVG"""
    
    print(f"📊 Analyzing: {name}")
    print(f"   File: {svg_path}")
    
    if not Path(svg_path).exists():
        print(f"   ❌ File not found")
        return
    
    try:
        # Read and parse SVG
        with open(svg_path, 'r') as f:
            svg_content = f.read()
        
        root = ET.fromstring(svg_content)
        
        # Find filled regions (phase areas)
        fill_colors = []
        for elem in root.iter():
            if 'style' in elem.attrib:
                style = elem.attrib['style']
                if 'fill:' in style and 'fill-opacity' in style:
                    fill_match = re.search(r'fill:\s*([^;]+)', style)
                    if fill_match:
                        color = fill_match.group(1).strip()
                        if color not in fill_colors and color != '#ffffff':
                            fill_colors.append(color)
        
        # Color interpretations
        color_meanings = {
            '#e57373': '🔴 Red (Dominance)',
            '#81c784': '🟢 Green (Restructuring)', 
            '#ba68c8': '🟣 Purple (Mixing)'
        }
        
        print(f"   📈 Phase regions found: {len(fill_colors)}")
        for color in fill_colors:
            meaning = color_meanings.get(color, f'Unknown: {color}')
            print(f"      {meaning}")
        
        # Check if it's a proper multi-phase diagram
        if len(fill_colors) >= 3:
            print(f"   ✅ Multi-phase diagram (good!)")
        elif len(fill_colors) == 1:
            print(f"   ⚠️  Single-phase diagram (may need more data)")
        else:
            print(f"   🔍 Partial diagram ({len(fill_colors)} phases)")
        
        return len(fill_colors)
        
    except Exception as e:
        print(f"   ❌ Error analyzing SVG: {e}")
        return 0

def main():
    """Analyze both new phase diagrams"""
    
    print("🔍 ANALYZING NEW PHASE DIAGRAMS FROM JSON SIMULATION DATA")
    print("=" * 65)
    
    diagrams = [
        {
            "name": "48species_500reps (500 reps × 3 intensities)", 
            "file": "Figure/PhaseDiagram/Fig_phase_diagram_48species_500reps.svg"
        },
        {
            "name": "48species_200reps_fine (200 reps × fine intervals)",
            "file": "Figure/PhaseDiagram/Fig_phase_diagram_48species_200reps_fine.svg"
        }
    ]
    
    total_phases = 0
    for diagram in diagrams:
        phases = analyze_phase_diagram_svg(diagram["file"], diagram["name"])
        total_phases += phases
        print()
    
    print("📋 SUMMARY:")
    print(f"   • Both diagrams use full Lotka-Volterra dynamics with defined pools")
    print(f"   • Data comes from vector decomposition of coalescence events")
    print(f"   • Classification: Dominance, Mixing, Restructuring phases")
    print(f"   • Total phase regions detected: {total_phases}")
    
    if total_phases >= 6:  # 3 phases × 2 diagrams
        print(f"   ✅ Both diagrams show proper multi-phase structure!")
    else:
        print(f"   ⚠️  Some diagrams may need more simulation data")
        print(f"      (Simulations are still running in background)")

if __name__ == "__main__":
    main()
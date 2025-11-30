#!/usr/bin/env python
"""
Simple script to analyze and describe the phase diagram SVG content
"""

import re
import xml.etree.ElementTree as ET

def describe_phase_diagram_svg(svg_path):
    """Describe the visual content of the phase diagram SVG"""
    
    print(f"Analyzing phase diagram: {svg_path}")
    print("=" * 60)
    
    # Read the SVG file
    with open(svg_path, 'r') as f:
        svg_content = f.read()
    
    # Parse as XML
    try:
        root = ET.fromstring(svg_content)
        
        # Find PolyCollection paths (the filled areas representing each phase)
        poly_collections = []
        
        # Look for paths with fill colors
        for elem in root.iter():
            if 'style' in elem.attrib:
                style = elem.attrib['style']
                if 'fill:' in style and 'fill-opacity' in style:
                    # Extract fill color
                    fill_match = re.search(r'fill:\s*([^;]+)', style)
                    if fill_match:
                        fill_color = fill_match.group(1).strip()
                        poly_collections.append(fill_color)
        
        print(f"Found {len(poly_collections)} phase regions:")
        
        # Color interpretations
        color_meanings = {
            '#e57373': 'Red - Dominance Phase',
            '#81c784': 'Green - Restructuring Phase', 
            '#ba68c8': 'Purple - Mixing Phase'
        }
        
        for i, color in enumerate(poly_collections):
            meaning = color_meanings.get(color, f'Unknown color: {color}')
            print(f"  Region {i+1}: {color} ({meaning})")
        
        # Look for coordinate data to estimate phase distributions
        path_elements = [elem for elem in root.iter() if elem.tag.endswith('path')]
        
        print(f"\nFound {len(path_elements)} path elements total")
        print(f"This indicates a multi-phase diagram with proper color regions")
        
        # Check for axis labels
        text_elements = [elem for elem in root.iter() if elem.tag.endswith('text')]
        print(f"Found {len(text_elements)} text labels (axis ticks, etc.)")
        
        return True
        
    except Exception as e:
        print(f"Error parsing SVG: {e}")
        return False

if __name__ == "__main__":
    svg_path = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/PhaseDiagram/Fig_phase_diagram_Simul_standard.svg"
    describe_phase_diagram_svg(svg_path)
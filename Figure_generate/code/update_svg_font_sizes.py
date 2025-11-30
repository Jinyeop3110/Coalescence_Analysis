#!/usr/bin/env python3
"""
Update font sizes in SVG files for community averaged single model figures
"""
import re
import sys

def update_svg_font_sizes(svg_file_path):
    """Update font sizes in an SVG file."""
    try:
        with open(svg_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Backup original content
        original_content = content
        
        # Update R² text font size (usually in text elements with "R²")
        # Look for patterns like: font-size:10px or font-size="10"
        content = re.sub(r'(R²[^<]*?font-size[:\s]*["\']?)(\d+(?:\.\d+)?)(px)?', 
                        lambda m: m.group(1) + '20' + (m.group(3) or ''), 
                        content)
        
        # Also handle cases where font-size comes before R²
        content = re.sub(r'(font-size[:\s]*["\']?)(\d+(?:\.\d+)?)(px)?([^>]*?R²)', 
                        lambda m: m.group(1) + '20' + (m.group(3) or '') + m.group(4), 
                        content)
        
        # Update tick label font sizes (π/4, π/2, 0)
        # These are typically in text elements
        tick_patterns = [r'π/4', r'π/2', r'0']
        
        for pattern in tick_patterns:
            # Pattern 1: font-size after the text
            content = re.sub(f'({pattern}[^<]*?font-size[:\\s]*["\']?)(\d+(?:\.\d+)?)(px)?', 
                            lambda m: m.group(1) + '18' + (m.group(3) or ''), 
                            content)
            
            # Pattern 2: font-size before the text
            content = re.sub(f'(font-size[:\\s]*["\']?)(\d+(?:\.\d+)?)(px)?([^>]*?{pattern})', 
                            lambda m: m.group(1) + '18' + (m.group(3) or '') + m.group(4), 
                            content)
        
        # Save the updated content
        with open(svg_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {svg_file_path}")
        return True
        
    except Exception as e:
        print(f"Error updating {svg_file_path}: {e}")
        return False

def main():
    # Target files
    svg_files = [
        "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Predictability_single_model/Fig_predictability_community_averaged_single_model_M.svg",
        "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Predictability_single_model/Fig_predictability_community_averaged_single_model_H.svg"
    ]
    
    for svg_file in svg_files:
        update_svg_font_sizes(svg_file)

if __name__ == "__main__":
    main()
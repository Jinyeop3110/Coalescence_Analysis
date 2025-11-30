#!/usr/bin/env python3
"""
Fix SVG viewBox to show complete content without cutting off
"""
import xml.etree.ElementTree as ET

def fix_svg_viewbox(svg_file_path):
    """Fix the viewBox to show complete content."""
    try:
        # Read the SVG file
        with open(svg_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse as XML
        root = ET.fromstring(content)
        
        # Keep the 2x2 inch dimensions but fix the viewBox to show all content
        root.set('width', '144pt')
        root.set('height', '144pt')
        
        # Set viewBox to show the complete original figure
        # The original figure area should be preserved
        root.set('viewBox', '0 0 213.11625 177.23625')
        
        # Convert back to string
        updated_content = ET.tostring(root, encoding='unicode')
        
        # Add XML declaration if it was present in original
        if content.startswith('<?xml'):
            updated_content = '<?xml version="1.0" encoding="utf-8"?>\n' + updated_content
        
        # Write the updated content
        with open(svg_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Fixed viewBox for {svg_file_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing {svg_file_path}: {e}")
        return False

def main():
    # Target files
    svg_files = [
        "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Predictability_single_model/Fig_predictability_community_averaged_single_model_M.svg",
        "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Predictability_single_model/Fig_predictability_community_averaged_single_model_H.svg"
    ]
    
    for svg_file in svg_files:
        fix_svg_viewbox(svg_file)

if __name__ == "__main__":
    main()
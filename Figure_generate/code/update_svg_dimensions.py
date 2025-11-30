#!/usr/bin/env python3
"""
Update SVG dimensions to 2x2 inches (144x144 pixels at 72 DPI)
"""
import re
import xml.etree.ElementTree as ET

def update_svg_dimensions(svg_file_path):
    """Update dimensions in an SVG file to 2x2 inches."""
    try:
        # Read the SVG file
        with open(svg_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse as XML to handle dimensions properly
        root = ET.fromstring(content)
        
        # Update width and height attributes
        # 2 inches = 144 pixels at 72 DPI
        root.set('width', '144pt')  # pt for points (72 points = 1 inch)
        root.set('height', '144pt')
        
        # Update viewBox if present to maintain aspect ratio
        viewbox = root.get('viewBox')
        if viewbox:
            # Extract current viewBox values
            vb_values = viewbox.split()
            if len(vb_values) == 4:
                # Keep the same aspect ratio but update to square
                min_x, min_y, width, height = map(float, vb_values)
                # Make it square by using the smaller dimension
                new_size = min(width, height)
                # Center the viewBox
                offset_x = (width - new_size) / 2
                offset_y = (height - new_size) / 2
                new_viewbox = f"{min_x + offset_x} {min_y + offset_y} {new_size} {new_size}"
                root.set('viewBox', new_viewbox)
        
        # Convert back to string
        updated_content = ET.tostring(root, encoding='unicode')
        
        # Add XML declaration if it was present in original
        if content.startswith('<?xml'):
            updated_content = '<?xml version="1.0" encoding="utf-8"?>\n' + updated_content
        
        # Write the updated content
        with open(svg_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Updated dimensions for {svg_file_path} to 2x2 inches")
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
        update_svg_dimensions(svg_file)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Remove title and legend from polarized SVG files
"""

import re
import os

def remove_title_and_legend_from_svg(input_file, output_file):
    """Remove title (text_7) and legend (legend_1) from SVG file"""
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Remove the title section (text_7)
    # Find the complete text_7 group including all its child elements
    title_pattern = r'<g id="text_7">.*?</g>'
    content = re.sub(title_pattern, '', content, flags=re.DOTALL)
    
    # Remove the legend section (legend_1)
    # Find the complete legend_1 group including all its child elements
    legend_pattern = r'<g id="legend_1">.*?</g>'
    content = re.sub(legend_pattern, '', content, flags=re.DOTALL)
    
    # Also remove any standalone comments about titles
    comment_pattern = r'<!-- .* - All Species Pools -->'
    content = re.sub(comment_pattern, '', content)
    
    # Clean up any extra whitespace that might have been left
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    return True

def main():
    """Remove titles and legends from all three polarized SVG files"""
    
    print("Removing titles and legends from polarized SVG files...")
    
    base_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_exp_merged"
    
    files_to_process = [
        "Metric_metric3_HN_all_pools_exp_Polarized.svg",
        "Metric_metric3_LN_all_pools_exp_Polarized.svg", 
        "Metric_metric3_MN_all_pools_exp_Polarized.svg"
    ]
    
    processed_count = 0
    
    for filename in files_to_process:
        input_file = os.path.join(base_dir, filename)
        output_file = input_file  # Overwrite the original file
        
        if os.path.exists(input_file):
            print(f"Processing {filename}...")
            
            success = remove_title_and_legend_from_svg(input_file, output_file)
            
            if success:
                processed_count += 1
                print(f"✅ Removed title and legend from {filename}")
            else:
                print(f"❌ Failed to process {filename}")
        else:
            print(f"❌ File not found: {filename}")
    
    print(f"\n" + "="*60)
    print(f"TITLE AND LEGEND REMOVAL COMPLETE!")
    print(f"="*60)
    print(f"📄 Files processed: {processed_count}/{len(files_to_process)}")
    print(f"🎯 Changes applied:")
    print(f"   - Removed title text from all plots")
    print(f"   - Removed legend box and all legend items")
    print(f"   - Cleaned up extra whitespace")
    print(f"   - Preserved all data points and axes")

if __name__ == "__main__":
    main()
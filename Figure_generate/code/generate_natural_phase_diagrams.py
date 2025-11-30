#!/usr/bin/env python3
"""
generate_natural_phase_diagrams.py

Purpose: Master script to generate all natural community phase diagrams
Key features:
- Runs both phase diagram and pie chart generation for natural communities
- Provides comprehensive output for natural coalescence data analysis
- Complements existing synthetic community phase diagrams

Outputs:
- Figure/PhaseDiagram/Fig_phase_diagram_natural.svg
- Figure/PhaseDiagram/Fig_phase_diagram_natural_pie.svg

Author: Gore Lab Analysis Team
Date: January 2025
"""

import sys
import os
from pathlib import Path

# Add current directory to path to import our modules
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Main function to generate all natural phase diagrams."""
    
    print("="*80)
    print("NATURAL COMMUNITY PHASE DIAGRAM GENERATION")
    print("="*80)
    
    try:
        # Import and run natural phase diagram generation
        print("\n1. Generating natural community phase diagrams...")
        from plot_phase_diagram_natural import main as generate_natural
        generate_natural()
        
        print("\n" + "-"*60)
        
        # Import and run natural pie chart generation
        print("\n2. Generating natural community pie charts...")
        from plot_phase_diagram_natural_pie import main as generate_natural_pie
        generate_natural_pie()
        
        print("\n" + "="*80)
        print("✅ ALL NATURAL COMMUNITY PHASE DIAGRAMS GENERATED SUCCESSFULLY!")
        print("="*80)
        
        # List generated files
        output_dir = Path("Figure/PhaseDiagram")
        natural_files = list(output_dir.glob("*natural*"))
        
        if natural_files:
            print(f"\n📁 Generated files in {output_dir}:")
            for file in sorted(natural_files):
                print(f"  ✓ {file.name}")
        else:
            print(f"\n⚠️  No natural community files found in {output_dir}")
            
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("Make sure you're running this script from the correct directory with access to common_setup.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
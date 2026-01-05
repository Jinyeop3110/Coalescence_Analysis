#!/usr/bin/env python3
"""
Minimal cartoon plot showing interaction strength concept
"""

import numpy as np

# Try different matplotlib backends
def try_matplotlib():
    backends_to_try = ['Agg', 'svg', 'pdf', 'ps']
    
    for backend in backends_to_try:
        try:
            import matplotlib
            matplotlib.use(backend)
            import matplotlib.pyplot as plt
            print(f"Successfully loaded matplotlib with {backend} backend!")
            return True, plt
        except ImportError as e:
            print(f"Backend {backend} failed: {e}")
            continue
    
    return False, None

# Try to load matplotlib
PLOTTING_AVAILABLE, plt = try_matplotlib()

def uniform_distribution(u, o=0):
    """Generate uniform random interaction strength (same as simulation)"""
    return (2*u + 2*o) * np.random.random() - o

if not PLOTTING_AVAILABLE:
    print("❌ Cannot create plot - matplotlib not available")
    exit(1)

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(1, 0.5))

# Plot one case (u = 0.5)
u = 0.5
color = 'grey'

# Plot uniform distribution from 0 to 2*u
x = np.linspace(0, 2*u, 100)
y = np.ones_like(x) / (2*u)  # Uniform distribution height

# Fill the area under the curve
ax.fill_between(x, 0, y, color=color, alpha=0.7)
ax.plot(x, y, color='black', linewidth=0.5)

# Set axes - extend both axes 20% beyond actual range
x_max = 2*u  # actual x range is 0 to 2*u
y_max = 1/(2*u)  # actual y range is 0 to 1/(2*u)

x_limit = x_max * 1.3  # 30% more than actual range
y_limit = y_max * 1.3  # 30% more than actual range

ax.set_xlim(0, x_limit)
ax.set_ylim(0, y_limit)

# Remove all spines first
for spine in ax.spines.values():
    spine.set_visible(False)

# Add arrows for x and y axes - extend to near the limits
ax.annotate('', xy=(x_limit * 0.95, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color='black', lw=1))
ax.annotate('', xy=(0, y_limit * 0.95), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color='black', lw=1))

# Remove tick labels but keep ticks
ax.set_xticks([])
ax.set_yticks([])

# Create output directory
output_dir = '/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/cartoon'
import os
os.makedirs(output_dir, exist_ok=True)

# Save to the specified directory in both PNG and SVG formats
output_file_png = f"{output_dir}/interaction_strength_cartoon.png"
output_file_svg = f"{output_dir}/interaction_strength_cartoon.svg"

plt.savefig(output_file_png, dpi=300, bbox_inches='tight')
plt.savefig(output_file_svg, bbox_inches='tight')
plt.show()

print(f"✅ Cartoon plot saved as: {output_file_png}")
print(f"✅ Cartoon plot saved as: {output_file_svg}")
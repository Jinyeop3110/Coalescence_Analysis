import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Create some test data
np.random.seed(42)
pred = np.random.uniform(0.2, 0.8, 20)
true = pred * 0.8 + 0.1 + np.random.normal(0, 0.05, 20)

# Calculate regression
slope, intercept, r_value, p_value, std_err = stats.linregress(pred, true)

# Create plot
fig, ax = plt.subplots(figsize=(5, 5))

# Plot data
ax.scatter(pred, true, color='blue', alpha=0.6, label='Data')

# Plot regression line
x_line = np.array([0, 1])
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, 'r-', linewidth=2, label=f'Regression: y={slope:.2f}x+{intercept:.2f}')

# Plot perfect prediction line
ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='y=x (perfect)')

# Verify a few points on regression line
test_x = [0.3, 0.5, 0.7]
for x in test_x:
    y_calc = slope * x + intercept
    ax.plot(x, y_calc, 'go', markersize=8)
    print(f"At x={x}: y={y_calc:.3f} (should be on red line)")

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel('Predicted')
ax.set_ylabel('True')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_title('Regression Line Test')

plt.savefig('regression_test.png')
print(f"\nRegression: slope={slope:.3f}, intercept={intercept:.3f}")
print(f"R² = {r_value**2:.3f}")
print("\nPlot saved as regression_test.png")
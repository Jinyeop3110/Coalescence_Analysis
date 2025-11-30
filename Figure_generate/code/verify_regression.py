import numpy as np
from scipy import stats

# Simulate Medium M-like data
pred = np.array([0.270, 0.5, 0.7, 0.976])
true = np.array([0.041, 0.5, 0.8, 0.999])

print("Data ranges:")
print(f"Predicted: [{pred.min():.3f}, {pred.max():.3f}], range = {pred.max()-pred.min():.3f}")
print(f"True: [{true.min():.3f}, {true.max():.3f}], range = {true.max()-true.min():.3f}")
print(f"True range / Pred range = {(true.max()-true.min())/(pred.max()-pred.min()):.3f}")

# Test different regression orders
print("\nRegression with pred as x, true as y (correct for our plot):")
slope1, intercept1, r1, p1, se1 = stats.linregress(pred, true)
print(f"slope = {slope1:.3f}, intercept = {intercept1:.3f}")

print("\nRegression with true as x, pred as y (wrong for our plot):")
slope2, intercept2, r2, p2, se2 = stats.linregress(true, pred)
print(f"slope = {slope2:.3f}, intercept = {intercept2:.3f}")

print("\nExpected slope ≈ true_range/pred_range ≈", (true.max()-true.min())/(pred.max()-pred.min()))
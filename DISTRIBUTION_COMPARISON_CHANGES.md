# RETENTION ASYMMETRICITY: DISTRIBUTION COMPARISON APPROACH

## ✅ **CHANGES IMPLEMENTED**

### **🎯 Key Change: From Event-wise to Distribution Comparison**

**BEFORE:** 
- Each coalescence event tested individually with permutation test
- P-value calculated for each event (is this specific event significantly asymmetric?)
- Reported "X% of events are significant"

**NOW IMPLEMENTED:**
- Calculate asymmetricity for all events (no individual p-values)
- Compare entire DISTRIBUTIONS: experimental vs null models
- Statistical tests: Mann-Whitney U test comparing distributions
- Ask: "Is the experimental distribution different from null expectations?"

---

## 📊 **NEW STATISTICAL APPROACH**

### **Distribution Comparison Tests:**

1. **Mann-Whitney U Test** (non-parametric)
   - Tests if experimental distribution differs from null distribution
   - No assumptions about normality
   - P-value indicates if distributions are significantly different

2. **Kolmogorov-Smirnov Test** (also implemented)
   - Tests if two distributions come from same underlying distribution
   - Sensitive to differences in shape, location, and scale

3. **Effect Size (Cohen's d)**
   - Measures practical significance beyond p-values
   - Small (<0.5), Medium (0.5-0.8), Large (>0.8)

---

## 🔬 **WHAT THIS MEANS BIOLOGICALLY**

### **Old Question (Event-wise):**
"Is this specific coalescence event more asymmetric than expected by chance?"

### **New Question (Distribution):**
"Do coalescence events in condition X show systematically different asymmetricity patterns than expected under null models?"

**This is better because:**
- Tests overall biological patterns, not individual variations
- More statistical power from using all data together
- Directly addresses whether experimental conditions create different outcomes than null expectations

---

## 📈 **EXAMPLE OUTPUT**

```
=== RETENTION ASYMMETRICITY ANALYSIS SUMMARY ===
📊 Now comparing DISTRIBUTIONS between experimental and null models
(No longer testing individual event significance)

LN Condition:
  Retention Asymmetricity TYPE1:
    Experimental: n=15, mean=0.329, std=0.241
    vs neutral_mixing: mean=0.187, p=0.0234 *
    vs random_selection_v1: mean=0.201, p=0.0412 *
    vs random_selection_v2: mean=0.195, p=0.0387 *
```

**Interpretation:**
- LN experimental distribution (mean=0.329) is significantly different from all null models
- P < 0.05 (*) indicates experimental asymmetricity is systematically higher than null expectations
- This suggests biological factors (not just random retention) drive asymmetricity in LN conditions

---

## 🚀 **ADVANTAGES OF THIS APPROACH**

1. **More Appropriate Test**: Tests what we really care about - are experimental patterns different from null expectations?

2. **Greater Statistical Power**: Uses all events together rather than testing each individually

3. **Clearer Interpretation**: One p-value per condition/null model comparison instead of many individual p-values

4. **Biological Relevance**: Tests systematic differences in coalescence patterns, not individual event variations

5. **Robust Statistics**: Non-parametric tests don't assume normal distributions

---

## 📊 **NEW PLOTS GENERATED**

1. **Distribution Histograms**: 
   - Overlaid experimental vs null model distributions
   - Visual comparison of distribution shapes and centers

2. **Box Plot Comparisons**:
   - Side-by-side experimental vs null models
   - Shows median, quartiles, and outliers
   - P-values annotated on plots

3. **Detailed Breakdown**:
   - Still maintains medium × species pool granularity
   - But compares distributions within each category

---

## ✅ **IMPLEMENTATION COMPLETE**

The analysis now:
- Calculates asymmetricity values without individual p-values
- Compares experimental vs null model DISTRIBUTIONS
- Uses Mann-Whitney U test for statistical comparison
- Reports distribution-level p-values
- Provides more biologically meaningful results

**This approach better answers the fundamental question: Do experimental coalescence events show different asymmetricity patterns than expected by chance?**
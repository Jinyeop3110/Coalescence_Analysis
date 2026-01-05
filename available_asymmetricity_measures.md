# Available Asymmetricity Measures

Based on the codebase analysis, here are all the available asymmetricity measures:

## 1. **Similarity-Based Asymmetricity**
**Function:** `calculate_similarity_asymmetricity(sim1, sim2)`
**Formula:** `|sim1 - sim2| / (sim1 + sim2)`
**Available Metrics:**
- Bray-Curtis similarity
- Jensen-Shannon similarity  
- Cosine similarity
- Jaccard similarity
- Euclidean similarity

**Interpretation:** Measures how differently the mixed community resembles each parent based on various similarity metrics.

## 2. **Vector-Based Asymmetricity** 
**Function:** `calculate_vector_asymmetricity(magA, magB)`
**Formula:** `|arctan(magA/magB) - π/4| / (π/4)`
**Interpretation:** Uses arctangent to measure deviation from perfect symmetry (45° angle). Based on vector decomposition of the mixed community.

## 3. **Diversity-Based Asymmetricity (Type 1)**
**Function:** `calculate_diversity_asymmetricity_type1(div1, div2, div_mixed)`
**Formula:** `|min(div1, div_mixed) - min(div2, div_mixed)| / div_mixed`
**Interpretation:** Measures asymmetricity based on species richness, excluding overlaps. Focuses on how much diversity each parent contributes.

## 4. **Diversity-Based Asymmetricity (Type 2)**
**Function:** `calculate_diversity_asymmetricity_type2(div1, div2, div_mixed)`  
**Formula:** `|min(div1, div_mixed) - min(div2, div_mixed)| / (div_mixed - min(div1, div2))`
**Interpretation:** Alternative diversity measure that normalizes by "novel" diversity gained through coalescence.

## 5. **Retention-Based Asymmetricity (Type 1) - NEW!**
**Function:** `calculate_retention_asymmetricity_type1(parent1, parent2, mixed)`
**Formula:** `|retention_rate1 - retention_rate2|` (unique species only)
**Interpretation:** Tests if parents differ in retaining their unique species. Includes statistical significance testing.

## 6. **Retention-Based Asymmetricity (Type 2) - NEW!**
**Function:** `calculate_retention_asymmetricity_type2(parent1, parent2, mixed)`
**Formula:** `|retention_rate1 - retention_rate2|` (all species)  
**Interpretation:** Tests overall species retention differences. Includes statistical significance testing.

## 7. **Other Asymmetricity Measures**
**Found in other files:**
- `VariousMetrics.py`: `calculate_asymmetricity(coeff_parent1, coeff_parent2, residual)`
- `DiversityAsymmetricityAnalysis.py`: Origin tracking versions of diversity asymmetricity

## **Current Analysis Pipeline**
The main analysis function `analyze_multiple_coalescence_asymmetricity()` includes:
1. **Similarity-based** (all metrics)
2. **Vector-based** 
3. **Diversity-based Type 1 & Type 2**
4. **Retention-based Type 1 & Type 2** (newly added)

## **Statistical Testing**
- **Traditional measures (1-4):** Descriptive only, no statistical significance
- **Retention-based measures (5-6):** Include permutation tests for statistical significance (p-values)
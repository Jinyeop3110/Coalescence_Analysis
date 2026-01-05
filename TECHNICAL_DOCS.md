# Technical Documentation

## Mathematical Methods and Formulations

### 1. Community Similarity Measures

#### Bray-Curtis Similarity
```
BC(A,B) = Σ min(Ai, Bi) / Σ max(Ai, Bi)
```
Where A and B are abundance vectors after applying threshold filtering.

#### Jaccard Similarity
```
J(A,B) = |A ∩ B| / |A ∪ B|
```
Based on presence/absence after threshold filtering.

#### Jensen-Shannon Similarity
```
JS(A,B) = 1 - √(0.5 * KL(A||M) + 0.5 * KL(B||M))
```
Where M = (A+B)/2 and KL is Kullback-Leibler divergence.

#### Dot Product Similarity
```
DP(A,B) = Σ (Ai/||A||) * (Bi/||B||)
```
Normalized dot product of abundance vectors.

### 2. Asymmetry Quantification

#### Method 1: Similarity-based Asymmetry
```
Asym_BC = 2 * |BC(C,A)/(BC(C,A) + BC(C,B)) - 0.5|
```
Where C is the coalesced community, A and B are parent communities.

#### Method 2: Abundance-based Asymmetry  
```
Asym2 = |Σ(C*(A>t) - C*(B>t))| / Σ(C*(A>t) + C*(B>t) - C*(A>t)*(B>t))
```
Where t is the abundance threshold.

#### Method 3: Sign-based Asymmetry
```
Asym3 = |Σ(C*(A>t) - C*(B>t))| / Σ(C*(A>t) + C*(B>t) - 2*C*(A>t)*(B>t))
```

### 3. Species Additivity Measures

#### Additivity 1: Richness-based
```
Add1 = S_observed / (S_A + S_B - S_overlap)
```
Where S_x is the number of species above threshold in community x.

#### Additivity 2: Overlap fraction
```
Add2 = S_observed_overlap / S_expected_overlap
```

#### Additivity 3: Total species fraction
```
Add3 = S_observed_overlap / (S_A + S_B)
```

### 4. Generalized Lotka-Volterra Model

#### Differential Equation System
```
dxi/dt = gi * xi * (1 - Σj(Iij * xj)/ki)
```

Where:
- `xi` = abundance of species i
- `gi` = intrinsic growth rate of species i  
- `ki` = carrying capacity of species i
- `Iij` = interaction strength from species j to species i

#### Implementation Details
- **Integration method**: RK23 (Runge-Kutta)
- **Time span**: 0 to 2500 time units
- **Evaluation points**: 7500 points for dynamics, final point for equilibrium
- **Threshold**: Species below 1e-4 abundance set to 0

### 5. Experimental Design Structure

#### Sample Naming Convention
```
P[Plate]-[Sample]: e.g., P7-01
```

#### Community Type Encoding
- **F**: Final timepoint (day 7)
- **S/N**: Synthetic/Natural origin
- **L/M/H**: Low/Medium/High nutrient levels
- **S/C**: Single/Coalesced communities
- **1/2**: Replicate number

#### Species Pool Organization
- **6 species pools**: Communities 1-9 (single), 1-14 (coalesced)
- **12 species pools**: Communities 10-18 (single), 15-41 (coalesced) 
- **24 species pools**: Communities 19-30 (single), 42-47 (coalesced)

### 6. Statistical Analysis Framework

#### Threshold Analysis
Multiple abundance thresholds tested:
- 0.1, 0.033, 0.01, 0.0033, 0.001

#### Null Model Generation
For each coalescence event:
1. Randomly assign species to parent communities
2. Maintain total abundance distributions
3. Calculate metrics for null communities
4. Compare observed vs. null distributions

#### Exception Handling
Excluded samples due to:
- Low read counts (< 500 reads)
- Missing subcommunity data
- Contamination indicators
- Technical failures

### 7. Data Processing Pipeline

#### Sequence Processing
1. **Raw OTU tables** → Quality filtering → **Filtered counts**
2. **Taxonomy assignment** → **ASV identification**
3. **Abundance normalization** → **Relative abundances**
4. **Threshold application** → **Binary presence/absence**

#### Experimental Data Integration
1. **Growth curves** → **Growth rate calculation**
2. **pH measurements** → **Time series analysis**
3. **Optical density** → **Biomass estimation**
4. **Metadata integration** → **Sample annotation**

### 8. Figure Generation Specifications

#### Plot Types
- **Scatter plots**: Community composition visualization
- **Box plots**: Statistical distributions
- **Heat maps**: Similarity matrices
- **Vector plots**: Asymmetry visualization
- **Time series**: Growth dynamics

#### Color Schemes
- **Community origin**: Synthetic (blue) vs Natural (orange)
- **Nutrient levels**: Low (light) to High (dark)
- **Significance**: p < 0.05 highlighted

### 9. Computational Requirements

#### Memory Usage
- **MATLAB**: ~8GB RAM for full analysis
- **Python**: ~4GB RAM for figure generation
- **Storage**: ~10GB for complete dataset

#### Processing Time
- **Sequence processing**: ~30 minutes
- **Coalescence analysis**: ~2 hours  
- **Simulation runs**: ~4 hours
- **Figure generation**: ~1 hour

### 10. Quality Control Measures

#### Data Validation
- Cross-validation between replicates
- Comparison with published datasets
- Internal consistency checks
- Statistical power analysis

#### Reproducibility
- Fixed random seeds for simulations
- Version-controlled analysis scripts
- Documented parameter settings
- Automated testing procedures 
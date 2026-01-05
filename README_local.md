# Microbial Community Coalescence Analysis

A comprehensive analysis pipeline for studying microbial community coalescence dynamics through experimental data processing, computational modeling, and statistical analysis.

## 📋 Overview

This project investigates **microbial community coalescence** - the process of combining two distinct microbial communities and analyzing the resulting community dynamics. The research combines:

- **Experimental data** from synthetic and natural microbial communities
- **16S rRNA sequencing analysis** for community composition
- **Lotka-Volterra modeling** for theoretical predictions
- **Statistical analysis** of coalescence outcomes
- **Publication-quality figure generation**

## 🔬 Scientific Background

Community coalescence is a fundamental ecological process that occurs when previously separated communities interact. This project quantifies:

- **Asymmetry** in coalescence outcomes
- **Species additivity** during community mixing
- **Environmental effects** on coalescence dynamics
- **Predictability** of coalescence outcomes

## 📁 Project Structure

```
Coalescence_session_20230404/
├── Main_natural.m              # Natural community analysis workflow
├── Main_synthetic.m            # Synthetic community analysis workflow
├── AnalyzeCoalescence_*.m      # Core coalescence analysis scripts
├── ExperimentalResult/         # Experimental data processing
│   ├── Data/                   # Raw experimental measurements
│   ├── Functions/              # Data processing utilities
│   └── ExperimentalDataProcessing.m
├── Figure_generate/            # Publication figure generation
│   ├── Main_Fig_1/ through Main_Fig_9/
│   ├── code/                   # Shared analysis code
│   └── Functions_for_FigureGeneration.py
├── SimulationResult/           # Computational modeling
│   ├── Simulation/             # Lotka-Volterra simulations
│   └── result_*/               # Simulation outputs
├── SEQanalysis/               # 16S rRNA sequencing data
├── Postprocessed/             # Processed data files
└── Analyzed/                  # Analysis results
```

## 🛠️ Requirements

### Software Dependencies
- **MATLAB** (R2019b or later)
- **Python** (3.7+) with packages:
  - `numpy`, `pandas`, `matplotlib`, `seaborn`
  - `scipy`, `openpyxl`, `jupyter`

### Data Dependencies
- 16S rRNA sequencing data (OTU tables, taxonomy)
- Experimental measurements (optical density, pH, growth rates)
- Pre-computed interaction matrices for simulations

## 🚀 Quick Start

### 1. Setup Environment
```matlab
% In MATLAB, navigate to project directory
addpath(genpath(pwd))
```

### 2. Run Main Analysis

**For Synthetic Communities:**
```matlab
Main_synthetic
```

**For Natural Communities:**
```matlab
Main_natural
```

### 3. Generate Figures
```python
# Navigate to Figure_generate/Main_Fig_X/
jupyter notebook Generate_FigX_Y.ipynb
```

## 📊 Key Features

### Coalescence Metrics
- **Similarity Measures**: Bray-Curtis, Jaccard, Jensen-Shannon, Dot Product
- **Asymmetry Quantification**: Multiple mathematical formulations
- **Species Additivity**: Track ASV (species) gain/loss during coalescence
- **Environmental Dependencies**: Nutrient levels (Low/Medium/High)

### Experimental Design
- **Species Pool Sizes**: 6, 12, 24 species communities
- **Nutrient Conditions**: LN (Low), MN (Medium), HN (High) nutrients
- **Community Types**: Single (S) vs Coalesced (C) communities
- **Origins**: Synthetic (S) vs Natural (N) communities

### Computational Modeling
- **Generalized Lotka-Volterra** dynamics simulation
- **Species interaction matrices** with varying interaction strengths
- **Null model comparisons** for statistical validation

## 📈 Data Processing Pipeline

1. **Raw Data Import** → Sequencing files and experimental measurements
2. **Preprocessing** → Normalization and quality control
3. **Metadata Generation** → Sample information and experimental design
4. **Coalescence Analysis** → Pairwise community comparisons
5. **Statistical Analysis** → Metrics calculation across conditions
6. **Visualization** → Publication-ready figures

## 🔄 Workflow Examples

### Basic Coalescence Analysis
```matlab
% Load processed data
global ProcessedSeq Metadata CoalRecipe;
ProcessedSeq = readtable('Postprocessed/processed_Sequences_synthetic.xlsx');
Metadata = readtable('Postprocessed/Metadata.xlsx');

% Analyze coalescence for medium nutrient, 12 species
ID_list = CommunityPermutate("F","S", "M", "C");
for idx = 1:length(ID_list)
    S = GetCommunity(ID_list(idx));
    [S1,S2] = GetSubcommunities(ID_list(idx));
    % Calculate metrics...
end
```

### Simulation Analysis
```python
from LV import run_lotka_volterra
import numpy as np

# Run Lotka-Volterra simulation
y0 = np.random.rand(24) * 0.1  # Initial abundances
t = np.linspace(0, 2500, 7500)  # Time points
result = run_lotka_volterra(y0, t, species_mask, I, g, k)
```

## 📋 Key Output Files

### Processed Data
- `processed_Sequences_*.xlsx` - Normalized abundance matrices
- `processed_CoalescenceEvent_*.xlsx` - Coalescence metrics
- `processed_Communities_*.xlsx` - Community-level statistics

### Analysis Results
- Similarity matrices across experimental conditions
- Asymmetry measurements for each coalescence pair
- Species additivity scores
- Environmental effect quantifications

## 📚 Key Functions

### MATLAB Functions
- `AnalyzeCoalescence_*()` - Main analysis workflows
- `SimilarityBC()`, `SimilarityJ()` - Community similarity measures
- `Assymetricity*()` - Asymmetry quantification methods
- `GetCommunity()`, `GetSubcommunities()` - Data retrieval utilities

### Python Functions
- `run_lotka_volterra()` - ODE simulation execution
- `getCoalescence()` - Data filtering and selection
- `CommunityPermutate()` - Experimental design utilities

## 🎯 Applications

This pipeline enables analysis of:
- **Ecological restoration** outcomes
- **Microbiome therapy** effectiveness
- **Fermentation** process optimization
- **Environmental remediation** strategies

## 📖 Citation

If you use this code in your research, please cite:
```
[Paper citation to be added upon publication]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions about the code or methodology:
- **Primary Investigator**: [Contact information]
- **Code Maintainer**: [Contact information]
- **Issues**: Please use the GitHub issue tracker

## 🔗 Related Resources

- [Microbiome analysis tutorials](link)
- [Lotka-Volterra modeling guides](link)
- [Community ecology resources](link)

---

**Note**: This project contains both experimental data and computational models. Ensure you have appropriate computational resources for large-scale simulations and figure generation. 
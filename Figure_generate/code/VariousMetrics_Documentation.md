# VariousMetrics.py - Comprehensive Documentation

## Overview

The `VariousMetrics.py` module provides a complete suite of ecological metrics and analysis functions specifically designed for studying microbial community coalescence. This refactored module centralizes all similarity, diversity, and specialized coalescence metrics into a single, well-documented Python module.

## Key Features

- **Diversity Metrics**: Species richness, Shannon diversity, Simpson diversity, evenness measures
- **Similarity Metrics**: Bray-Curtis, Jensen-Shannon, Jaccard, Cosine, Euclidean, Morisita-Horn
- **Advanced Ecological Metrics**: Hill numbers, Pielou evenness, Berger-Parker dominance, Chao1 estimator
- **Coalescence-Specific Analysis**: Relative similarity, additivity metrics, vector decomposition
- **Population-Level Analysis**: Bias analysis, success rate calculations, multi-event summaries
- **Utility Functions**: Data preprocessing, visualization helpers, summary statistics

## Quick Start

```python
import VariousMetrics as vm
import numpy as np

# Create sample communities
parent1 = np.array([10, 8, 5, 3, 2, 1, 0, 0])
parent2 = np.array([2, 3, 8, 6, 4, 2, 1, 0])
offspring = np.array([6, 5, 7, 4, 3, 1, 0, 0])

# Analyze a single coalescence event
result = vm.analyze_coalescence_event(offspring, parent1, parent2, 
                                    metrics=['bray_curtis', 'jensen_shannon'])

# Print key results
print(f"Bray-Curtis similarity to parent1: {result['similarities']['bray_curtis']['to_parent1']:.3f}")
print(f"Relative similarity to parent1: {result['relative_similarities']['bray_curtis']['relative_similarity_parent1']:.3f}")
```

## Core Metrics

### Diversity Metrics

| Function | Description | Range |
|----------|-------------|-------|
| `richness(A, threshold=0)` | Species richness (number of species) | [0, ∞) |
| `shannon_diversity(A, threshold=0)` | Shannon diversity index | [0, ∞) |
| `simpson_diversity(A, threshold=0)` | Inverse Simpson diversity | [1, ∞) |
| `evenness_pielou(A, threshold=0)` | Pielou's evenness index | [0, 1] |
| `berger_parker_dominance(A, threshold=0)` | Dominance of most abundant species | [0, 1] |

### Similarity Metrics

| Function | Description | Range |
|----------|-------------|-------|
| `bray_curtis_similarity(A, B, threshold=0)` | Bray-Curtis similarity | [0, 1] |
| `jensen_shannon_similarity(A, B, threshold=0)` | Jensen-Shannon similarity | [0, 1] |
| `jaccard_similarity(A, B, threshold=0)` | Jaccard similarity index | [0, 1] |
| `cosine_sim(A, B, threshold=0)` | Cosine similarity | [0, 1] |
| `euclidean_similarity(A, B, threshold=0)` | Euclidean distance converted to similarity | [0, 1] |
| `morisita_horn_similarity(A, B, threshold=0)` | Morisita-Horn similarity | [0, 1] |

### Advanced Ecological Metrics

| Function | Description |
|----------|-------------|
| `hill_numbers(A, threshold=0, q_values=[0,1,2])` | Hill numbers for different q values |
| `chao1_richness_estimator(A, threshold=0)` | Chao1 estimator for total richness |
| `mcintosh_evenness(A, threshold=0)` | McIntosh evenness index |

## Coalescence Analysis Functions

### Single Event Analysis

```python
# Comprehensive analysis of a single coalescence event
result = vm.analyze_coalescence_event(
    offspring, parent1, parent2, 
    threshold=0,
    metrics=['bray_curtis', 'jensen_shannon', 'jaccard'],
    include_vector_decomp=True,
    include_additivity=True
)

# Access results
diversity_metrics = result['diversity_offspring']
similarities = result['similarities']['bray_curtis']
relative_sim = result['relative_similarities']['bray_curtis']
additivity = result['additivity']
vector_decomp = result['vector_decomposition']
```

### Multiple Events Analysis

```python
# Analyze multiple coalescence events
population_results = vm.analyze_multiple_coalescence_events(
    offspring_list, parent1_list, parent2_list,
    threshold=0,
    metrics=['bray_curtis', 'jensen_shannon'],
    include_bias_analysis=True
)

# Access population-level statistics
summary_stats = population_results['summary_statistics']['bray_curtis']
bias_analysis = population_results['bias_analysis']['bray_curtis']
```

## Utility Functions

### Data Preparation

```python
# Normalize abundance vectors
normalized_A = vm.normalize_abundance(A, method='total')  # Sum to 1
normalized_A = vm.normalize_abundance(A, method='max')    # Max value to 1

# Filter low abundance species
filtered_A = vm.filter_low_abundance(A, threshold=0.001)

# Prepare data for plotting
plot_data = vm.prepare_plotting_data(similarities_p1, similarities_p2, "Bray-Curtis")
```

### Summary Statistics

```python
# Calculate comprehensive summary statistics
stats = vm.calculate_summary_stats(similarity_values)
# Returns: mean, median, std, min, max, q25, q75, count

# Calculate deviation statistics
dev_stats = vm.calculate_deviation_statistics(relative_similarities, target=0.5)
# Returns: mean_deviation, fraction_above_target, etc.
```

## Metric Registry System

The module includes a registry system for easy access to all available metrics:

```python
# List all available metrics
available = vm.list_available_metrics()
print(available['similarity_metrics'])  # All similarity functions
print(available['diversity_metrics'])   # All diversity functions
print(available['analysis_functions'])  # All analysis functions

# Get specific functions by name
bray_curtis_func = vm.get_similarity_function('bray_curtis')
shannon_func = vm.get_diversity_function('shannon')
```

## Specialized Coalescence Metrics

### Relative Similarity Analysis

```python
# Analyze relative similarity to parents
rel_analysis = vm.relative_similarity_analysis(
    offspring, parent1, parent2, 
    threshold=0, 
    metric='bray_curtis'
)

# Returns:
# - relative_similarity_parent1: [0, 1]
# - relative_similarity_parent2: [0, 1]  
# - deviation_from_equal: [0, 0.5]
# - absolute similarities to both parents
```

### Additivity Metrics

```python
# Three different additivity measures
additivity1 = vm.Additivity1(offspring, parent1, parent2, threshold=0)  # Richness-based
additivity2 = vm.Additivity2(offspring, parent1, parent2, threshold=0)  # Union-based
additivity3 = vm.Additivity3(offspring, parent1, parent2, threshold=0)  # Normalized
```

### Vector Decomposition

```python
# Decompose offspring vector relative to parent
decomp = vm.vector_decomposition_metrics(offspring, parent1, threshold=0)

# Returns:
# - magnitude_A, magnitude_B: Vector magnitudes
# - angle_radians, angle_degrees: Angle between vectors
# - projection_magnitude: Magnitude of projection
# - orthogonal_magnitude: Magnitude of orthogonal component
# - cosine_similarity: Cosine of angle
```

## Population-Level Analysis

### Bias Analysis

```python
# Analyze bias towards one parent across multiple events
bias_results = vm.coalescence_bias_analysis(
    offspring_list, parent1_list, parent2_list,
    threshold=0, metric='bray_curtis'
)

# Returns:
# - bias_direction: "Parent 1" or "Parent 2"
# - bias_magnitude: [0, 0.5]
# - mean_relative_similarity_parent1: Overall bias metric
# - arrays of individual relative similarities and deviations
```

### Success Rate Analysis

```python
# Calculate coalescence success rate
success_results = vm.coalescence_success_rate(
    offspring_list, parent1_list, parent2_list,
    threshold=0, similarity_threshold=0.5
)

# Returns:
# - success_rate: Fraction of successful events
# - mean similarities to both parents
# - arrays of individual similarities
```

## Integration with Jupyter Notebooks

The module is designed for seamless integration with Jupyter notebooks for interactive analysis:

```python
# In Jupyter notebook
import sys
sys.path.append('/path/to/your/code/directory')
import VariousMetrics as vm

# Load your data
# data = pd.read_excel('your_data.xlsx')

# Perform analysis
# results = vm.analyze_coalescence_event(...)

# Use built-in plotting helpers
# plot_data = vm.prepare_plotting_data(similarities_p1, similarities_p2)
# sns.boxplot(data=plot_data, x='Parent', y='Similarity')
```

## Legacy Compatibility

The module maintains backward compatibility with original function names:

- `Diversity1`, `Diversity2`, `Diversity3` → Use `richness`, `shannon_diversity`, `simpson_diversity`
- `SimilarityBC`, `SimilarityJS`, `SimilarityJ` → Use `bray_curtis_similarity`, `jensen_shannon_similarity`, `jaccard_similarity`

## Error Handling

The module includes robust error handling for common issues:

- Division by zero protection with small epsilon values
- Validation of input arrays and parameters
- Graceful handling of edge cases (empty communities, single species, etc.)
- Clear error messages for invalid metric names or parameters

## Performance Considerations

- All functions are vectorized using NumPy for optimal performance
- Threshold filtering is applied efficiently to avoid unnecessary computations
- Large-scale analyses use memory-efficient algorithms
- Optional parameters allow users to skip expensive computations when not needed

## Examples and Use Cases

### Example 1: Basic Community Comparison

```python
import numpy as np
import VariousMetrics as vm

# Two microbial communities
community_A = np.array([15, 10, 8, 5, 3, 2, 1, 0])
community_B = np.array([12, 8, 6, 7, 4, 2, 1, 1])

# Calculate all similarities
similarities = vm.calculate_all_similarities(community_A, community_B)
for metric, value in similarities.items():
    print(f"{metric}: {value:.3f}")

# Calculate all diversities
div_A = vm.calculate_all_ecological_metrics(community_A)
print(f"Community A Shannon diversity: {div_A['shannon']:.3f}")
print(f"Community A Pielou evenness: {div_A['evenness_pielou']:.3f}")
```

### Example 2: Coalescence Event Analysis

```python
# Coalescence experiment data
parent1 = np.array([20, 15, 10, 5, 3, 2, 1, 0])  # Parent community 1
parent2 = np.array([5, 8, 12, 15, 8, 4, 2, 1])   # Parent community 2
offspring = np.array([12, 11, 11, 10, 5, 3, 1, 0])  # Resulting community

# Comprehensive analysis
result = vm.analyze_coalescence_event(offspring, parent1, parent2)

# Print key findings
bc_sim = result['similarities']['bray_curtis']
print(f"Similarity to parent 1: {bc_sim['to_parent1']:.3f}")
print(f"Similarity to parent 2: {bc_sim['to_parent2']:.3f}")

rel_sim = result['relative_similarities']['bray_curtis']
print(f"Relative preference for parent 1: {rel_sim['relative_similarity_parent1']:.3f}")
print(f"Deviation from equal similarity: {rel_sim['deviation_from_equal']:.3f}")
```

### Example 3: Population Study

```python
# Multiple coalescence events
n_events = 50
results_list = []

for i in range(n_events):
    # Load or generate data for event i
    # offspring_i, parent1_i, parent2_i = load_event_data(i)
    
    result = vm.analyze_coalescence_event(offspring_i, parent1_i, parent2_i, 
                                        metrics=['bray_curtis'])
    results_list.append(result)

# Population-level analysis
population_analysis = vm.analyze_multiple_coalescence_events(
    offspring_list, parent1_list, parent2_list,
    metrics=['bray_curtis', 'jensen_shannon'],
    include_bias_analysis=True
)

# Summarize findings
for metric in ['bray_curtis', 'jensen_shannon']:
    bias = population_analysis['bias_analysis'][metric]
    print(f"{metric}: Bias towards {bias['bias_direction']} "
          f"(magnitude: {bias['bias_magnitude']:.3f})")
```

This comprehensive module provides all the tools needed for sophisticated analysis of microbial community coalescence while maintaining ease of use and clear documentation.

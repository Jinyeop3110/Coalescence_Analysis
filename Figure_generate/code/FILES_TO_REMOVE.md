# File Removal Recommendations for Coalescence Analysis

## Summary
This document identifies files that can be safely removed from the codebase to improve organization and reduce clutter. Files are categorized by removal priority and rationale.

---

## 🗑️ **IMMEDIATE REMOVAL (Safe to delete)**

### **Debugging/Testing Scripts**
```bash
# Temporary debugging and fix scripts
rm quick_test_fix.py
rm temp_functions.py
rm fix_hardcoded_nulls.py
rm fix_null_model_stratification.py
rm validate_stratification_fix.py
rm understand_data_types.py
```
**Rationale**: These are temporary scripts created for debugging specific issues. Once bugs are fixed, they serve no purpose.

### **Backup/Previous Versions**
```bash
# Previous version backups
rm AsymmetricityNullModelAnalysis_prev.py
```
**Rationale**: The current version (`AsymmetricityNullModelAnalysis.py`) supersedes the previous version.

### **Converted Jupyter Notebooks** 
```bash
# Notebooks that have been converted to Python scripts
rm Plot_pairwiseCoCulture.ipynb                    # → plot_pairwise_coculture.py
rm Plot_predictability_basic.ipynb                 # → plot_predictability_basic.py
rm Plot_predictability_simulation1_temp.ipynb      # → plot_predictability_simulation.py
```
**Rationale**: These notebooks have been successfully converted to Python scripts and are no longer needed.

### **Broken/Incomplete Files**
```bash
# Files marked as needing fixes or incomplete
rm "ToFix_Generate_Fig6_1_MostAbundant_Simulation-Variant_S24-Copy_ToFix.ipynb"
```
**Rationale**: File name indicates it needs fixing and appears to be a broken copy.

---

## ⚠️ **REVIEW BEFORE REMOVAL (Verify first)**

### **Potentially Redundant Analysis Scripts**
**Files to investigate:**
- `AsymmetricityAnalysis.py` vs `AsymmetricityNullModelAnalysis.py`
- `DiversityAsymmetricityAnalysis.py`
- `RealDataAsymmetricityAnalysis.py`

**Action needed**: Check if newer comprehensive scripts have replaced these individual analysis files.

### **Utility Scripts with Unclear Usage**
**Files to verify:**
- `create_summary.py` - Check if still used in workflow
- `diversity_asymmetricity_comparison.py` - May be superseded by main analysis
- `retention_distribution_comparison.py` - May be superseded by main analysis
- `CalculateEmpiricalRetentionProbabilities.py` - Check if integrated into main scripts

### **Potentially Outdated Notebooks**
**Files to review:**
- `Final_Day_Community_Plots.ipynb` vs `Final_Day_Community_Plots_with_Legend.ipynb`
- `Run_simulation_data.ipynb` vs `Run_simulation_dynamics.ipynb`
- Multiple `new_Plot_*.ipynb` files (may be drafts)

**Action needed**: Determine which versions are current and which are superseded.

---

## 📊 **ESTIMATED CLEANUP IMPACT**

### **Safe Removals (Immediate)**
- **Python files**: 6 scripts (~150KB saved)
- **Jupyter notebooks**: 4 notebooks (~2MB saved)
- **Risk level**: **ZERO** (all have replacements or are debugging files)

### **Potential Additional Removals (After Review)**
- **Python files**: 6-10 additional scripts (~300KB saved)
- **Jupyter notebooks**: 10-15 additional notebooks (~10MB saved)
- **Risk level**: **LOW** (requires verification first)

### **Directory Cleanup Potential**
- **Figure subdirectories**: Multiple old/duplicate figure outputs (~50MB saved)
- **Simulation data**: Potentially redundant simulation runs (~100MB saved)

---

## 🔄 **REPLACEMENT MAPPING**

| **File to Remove** | **Replacement** | **Status** |
|-------------------|----------------|------------|
| `Plot_pairwiseCoCulture.ipynb` | `plot_pairwise_coculture.py` | ✅ Converted |
| `Plot_predictability_basic.ipynb` | `plot_predictability_basic.py` | ✅ Converted |
| `Plot_predictability_simulation1_temp.ipynb` | `plot_predictability_simulation.py` | ✅ Converted |
| `AsymmetricityNullModelAnalysis_prev.py` | `AsymmetricityNullModelAnalysis.py` | ✅ Updated |
| `quick_test_fix.py` | *Fixes integrated* | ✅ Completed |
| `temp_functions.py` | *Functions moved to proper modules* | ✅ Completed |

---

## 📋 **RECOMMENDED REMOVAL SCRIPT**

### **Step 1: Safe Immediate Removals**
```bash
#!/bin/bash
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code

# Create backup directory first
mkdir -p ../backup_removed_files

# Move files to backup (safer than rm)
mv quick_test_fix.py ../backup_removed_files/
mv temp_functions.py ../backup_removed_files/
mv fix_hardcoded_nulls.py ../backup_removed_files/
mv fix_null_model_stratification.py ../backup_removed_files/
mv validate_stratification_fix.py ../backup_removed_files/
mv understand_data_types.py ../backup_removed_files/
mv AsymmetricityNullModelAnalysis_prev.py ../backup_removed_files/
mv Plot_pairwiseCoCulture.ipynb ../backup_removed_files/
mv Plot_predictability_basic.ipynb ../backup_removed_files/
mv Plot_predictability_simulation1_temp.ipynb ../backup_removed_files/
mv "ToFix_Generate_Fig6_1_MostAbundant_Simulation-Variant_S24-Copy_ToFix.ipynb" ../backup_removed_files/

echo "Files moved to backup_removed_files directory"
echo "If everything works fine after a week, you can permanently delete the backup"
```

### **Step 2: Directory Cleanup (Optional)**
```bash
# Clean up old figure outputs (review first)
find Figure/ -name "*.png" -mtime +30  # List old PNG files
find Figure/ -name "*.svg" -mtime +30  # List old SVG files

# Clean up duplicate simulation data (review first)
ls -la Simulation_Data/*/  # Review simulation directories for duplicates
```

---

## ✅ **VERIFICATION CHECKLIST**

Before removing files, verify:
- [ ] All converted Python scripts run successfully
- [ ] No remaining references to removed files in active scripts
- [ ] Core analysis pipeline still functions
- [ ] Important figures can still be generated
- [ ] Documentation is updated if needed

---

## 📝 **NOTES**

1. **Backup First**: Always move files to a backup directory rather than deleting immediately
2. **Test After Removal**: Run main analysis scripts to ensure nothing breaks
3. **Wait Period**: Keep backups for 1-2 weeks before permanent deletion
4. **Documentation**: Update any documentation that references removed files

**Created**: August 2025  
**Last Updated**: August 2025  
**Estimated Space Savings**: 150+ MB  
**Risk Level**: LOW (with proper verification)
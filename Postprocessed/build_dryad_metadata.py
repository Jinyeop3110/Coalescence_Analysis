"""Build Sample_Sheet.xlsx for Dryad submission.

Joins Postprocessed/Metadata.xlsx, CoalescenceRecipe.xlsx, and the two
processed_Sequences_*.xlsx files into a single self-describing workbook.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT  = ROOT / "Sample_Sheet.xlsx"

ORIGIN  = {"S": "Synthetic", "N": "Natural"}
MEDIUM  = {"L": "Nutr-",     "M": "Base",   "H": "Nutr+"}
SAMPTYP = {"S": "Subcommunity", "C": "Coalescence"}
TIMEPT  = {"F": "Final"}

# Exception annotations from Generate_Fig2_v1.0.ipynb:649
NOTES = {
    **{s: "no reads in coalescence result" for s in ["P4-02","P4-03","P4-23","P4-24","P7-97","P8-12"]},
    "P8-91": "no file",
    **{s: "MN E7 missing" for s in ["P5-73","P5-69","P5-64","P5-61","P5-59","P5-56"]},
    **{s: "MN24 CC, excess unwanted ASVs (likely mislabel)" for s in ["P5-47","P5-50"]},
    **{s: "ASV not in subcommunities at >0.3 abundance" for s in ["P5-39","P5-87","P5-54","P6-02","P6-47","P6-74","P6-57"]},
}

meta = pd.read_excel(ROOT / "Metadata.xlsx")
recipe_syn = pd.read_excel(ROOT / "CoalescenceRecipe.xlsx", sheet_name=0)
recipe_nat = pd.read_excel(ROOT / "CoalescenceRecipe.xlsx", sheet_name=1)
tax_syn = pd.read_excel(ROOT / "processed_Sequences_synthetic.xlsx", sheet_name=1)
tax_nat = pd.read_excel(ROOT / "processed_Sequences_natural.xlsx",   sheet_name=1)

# ---------- samples sheet ----------
df = meta.copy()
df["replicate"] = df["Replicate"].astype(int)
df["community_origin"] = df["CommunityOrigin"].map(ORIGIN)
df["medium"]           = df["Medium"].map(MEDIUM)
df["sample_type"]      = df["CoalescenceType"].map(SAMPTYP)
df["timepoint"]        = df["Timepoint"].map(TIMEPT)
df["community_idx"]    = df["CommunityIDX"].astype(int)

# Build sub-community lookup: (origin, medium, replicate, community_idx) -> sample_id
sub_lookup = (
    df[df["sample_type"] == "Subcommunity"]
      .set_index(["community_origin", "medium", "replicate", "community_idx"])["SampleIDX"]
      .to_dict()
)

# Build coalescence -> (sub1_idx, sub2_idx) map per origin
recipe_syn = recipe_syn.rename(columns={
    "CommunityIDX_Coal": "coal_idx", "CommunityIDX_Sub1": "sub1_idx", "CommunityIDX_Sub2": "sub2_idx",
})
recipe_nat = recipe_nat.rename(columns={
    "CommunityIDX_Coal_natural": "coal_idx", "CommunityIDX_Sub1_natural": "sub1_idx", "CommunityIDX_Sub2_natural": "sub2_idx",
})
recipe_syn["community_origin"] = "Synthetic"
recipe_nat["community_origin"] = "Natural"
recipe = pd.concat([recipe_syn, recipe_nat], ignore_index=True)
recipe_map = recipe.set_index(["community_origin", "coal_idx"])[["sub1_idx", "sub2_idx"]].to_dict("index")

def parents(row):
    if row["sample_type"] != "Coalescence":
        return pd.Series([pd.NA, pd.NA, pd.NA, pd.NA])
    key = (row["community_origin"], row["community_idx"])
    if key not in recipe_map:
        return pd.Series([pd.NA, pd.NA, pd.NA, pd.NA])
    s1, s2 = recipe_map[key]["sub1_idx"], recipe_map[key]["sub2_idx"]
    p1 = sub_lookup.get((row["community_origin"], row["medium"], row["replicate"], int(s1)))
    p2 = sub_lookup.get((row["community_origin"], row["medium"], row["replicate"], int(s2)))
    return pd.Series([int(s1), int(s2), p1, p2])

df[["parent_1_community_idx","parent_2_community_idx",
    "parent_1_sample_id","parent_2_sample_id"]] = df.apply(parents, axis=1)

od_cols = [f"fieldOD{i}" for i in range(1, 8)]
ph_cols = [f"fieldPH{i}" for i in range(1, 8)]
gc_cols = [f"fieldGC{i}" for i in range(1, 4)]
df["OD_final_mean"]       = df[od_cols].mean(axis=1)
df["OD_final_std"]        = df[od_cols].std(axis=1)
df["pH_final_mean"]       = df[ph_cols].mean(axis=1)
df["pH_final_std"]        = df[ph_cols].std(axis=1)
df["growth_curve_AUC_mean"] = df[gc_cols].mean(axis=1)

df["notes"] = df["SampleIDX"].map(NOTES).fillna("")

samples = df[[
    "SampleIDX",            # rename below
    "community_origin","medium","sample_type","replicate","community_idx","timepoint",
    "parent_1_community_idx","parent_2_community_idx",
    "parent_1_sample_id","parent_2_sample_id",
    "OD_final_mean","OD_final_std",
    "pH_final_mean","pH_final_std",
    "growth_curve_AUC_mean",
    *od_cols, *ph_cols, *gc_cols,
    "notes",
]].rename(columns={"SampleIDX":"sample_id"})
samples["community_origin"] = pd.Categorical(samples["community_origin"], ["Synthetic","Natural"], ordered=True)
samples["medium"]           = pd.Categorical(samples["medium"],           ["Nutr-","Base","Nutr+"], ordered=True)
samples["sample_type"]      = pd.Categorical(samples["sample_type"],      ["Subcommunity","Coalescence"], ordered=True)
samples = samples.sort_values(
    ["community_origin","medium","sample_type","replicate","community_idx"]
).reset_index(drop=True)
samples["community_origin"] = samples["community_origin"].astype(str)
samples["medium"]           = samples["medium"].astype(str)
samples["sample_type"]      = samples["sample_type"].astype(str)

# ---------- coalescence_recipe sheet ----------
recipe_out = recipe[["community_origin","coal_idx","sub1_idx","sub2_idx"]].rename(columns={
    "coal_idx":"coalescence_community_idx",
    "sub1_idx":"parent_1_community_idx",
    "sub2_idx":"parent_2_community_idx",
}).reset_index(drop=True)
recipe_out.insert(0, "event_id", range(1, len(recipe_out) + 1))

# ---------- asv_taxonomy sheet ----------
tax_syn = tax_syn.rename(columns={"UniqueSeuquences":"unique_sequence"}).copy()
tax_nat = tax_nat.rename(columns={"UniqueSeuquences":"unique_sequence"}).copy()
tax_syn["community_origin"] = "Synthetic"
tax_nat["community_origin"] = "Natural"
asv_tax = pd.concat([tax_syn, tax_nat], ignore_index=True)[
    ["community_origin","ASV","Kingdom","Phylum","Class","Order","Family","Genus","unique_sequence"]
].rename(columns=str.lower).rename(columns={"asv":"asv_id"})

with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
    samples.to_excel(xw,     sheet_name="samples",            index=False)
    recipe_out.to_excel(xw,  sheet_name="coalescence_recipe", index=False)
    asv_tax.to_excel(xw,     sheet_name="asv_taxonomy",       index=False)

print(f"Wrote {OUT}")
print(f"  samples:            {len(samples)} rows")
print(f"  coalescence_recipe: {len(recipe_out)} rows")
print(f"  asv_taxonomy:       {len(asv_tax)} rows")
print(f"  flagged samples:    {(samples['notes'] != '').sum()}")

from common_setup import *

print('Testing species availability:')
for species_num in [6, 12, 24]:
    for medium in ["L", "M", "H"]:
        try:
            IDX_list = Community_PermutateList("F", "S", medium, "C", species_num, -1)
            print(f'Species {species_num}, Medium {medium}: {len(IDX_list)} samples')
        except Exception as e:
            print(f'Species {species_num}, Medium {medium}: ERROR - {str(e)[:100]}')
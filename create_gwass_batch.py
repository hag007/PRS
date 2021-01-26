import numpy as np
import pandas as pd
import os
import constants
import shutil

root='/specific/elkon/hagailevi/PRS/_HAGAI/'
all_gwass=os.listdir(root)

for g in all_gwass:
    print(f'cur gwas: {g}')
    g_name=f"D_{'_'.join(g.split('_')[:3])}"
    g_path=os.path.join(constants.GWASS_PATH, g_name)
    try:
        os.mkdir(g_path)    
    except OSError:
        pass

    shutil.move(os.path.join(root, g), os.path.join(g_path, 'gwas_raw.tsv'))    
    
    


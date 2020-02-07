#Copied from Jupyter NB as a backup during hub maintenance

from fuzzywuzzy import process, fuzz
import pandas as pd
import numpy as np
import re

import os
cwd = os.getcwd()
filename = 'process_in_python.xlsx'
filepath = cwd + "/" + filename

locs = pd.read_excel(filepath)

locs['sn_sa'] = locs.apply(lambda row: fuzz.token_sort_ratio(row['SiteName'], row['Street Address 1']), axis =1)
locs['sn_name'] = locs.apply(lambda row: fuzz.token_sort_ratio(row['SiteName'], row['Partner Organization Name']), axis =1)

locs_prep = locs

locs_prep['clean_sitename'] = np.where((locs['SiteName'].notnull()) & (locs['special_desig'] == 0) &
                    ((locs['sn_sa'] >= 80) | (locs['sn_name'] >= 80) | (locs['loc_owner_code'] == 840)), True, False)
                    
def sitename_cleaner(x, y):
    if x is True:
        return re.sub(r'([\w\d\D])','', y)
    else:
        return y
        
locs_prep['SiteName'] = locs_prep.apply(lambda row: sitename_cleaner(row['clean_sitename'], row['SiteName']), axis =1)

locs_grouped = locs_prep
locs_grouped['group_id'] = locs_prep.groupby(['Partner', 'Street Address 1', 'SiteName']).ngroup()


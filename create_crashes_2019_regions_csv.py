# This script creates a new .csv file containing the 2019 crashes data with an added REGION_ID attribute

import pandas as pd
import numpy as np


# %%
# Load the Congestion 2019 data set
congestion_data = pd.read_csv('./data/congestion_2019.csv')

# %%
# Extract a list of unique region IDs
region_ids = congestion_data['REGION_ID'].unique()

# %%
# Create a dictionary of regions with ID and corner locations

regions = []
for region_id in region_ids:
    region_specimen = congestion_data.loc[congestion_data['REGION_ID'] == region_id].iloc[0]
    nw_loc = (region_specimen['WEST'], region_specimen['NORTH'])
    se_loc = (region_specimen['EAST'], region_specimen['SOUTH'])
    regions.append({
        'id': region_id,
        'nw': nw_loc,
        'se': se_loc,
    })


# %%
def is_crash_in_region(crash_loc, region_nw_loc, region_se_loc):
    """Given the location of a crash and the corners of a region, return true if the crash took place within the region, false otherwise."""
    foo = min(region_nw_loc[0], region_se_loc[0]) < crash_loc[0] < max(region_nw_loc[0], region_se_loc[0])
    bar = min(region_nw_loc[1], region_se_loc[1]) < crash_loc[1] < max(region_nw_loc[1], region_se_loc[1])
    return foo and bar


# %%
# Load the Crashes 2019 data set
crashes_data = pd.read_csv('./data/crashes_2019.csv')
N = len(crashes_data)

# %%
# Create a list with a region ID for each row (defaulting to -1)

crashes_region_ids = np.full(N, -1)
for idx, row in crashes_data.iterrows():
    crashes_region_ids[idx] = -1
    loc = (row['LONGITUDE'], row['LATITUDE'])
    for region in regions:
        if is_crash_in_region(loc, region['nw'], region['se']):
            crashes_region_ids[idx] = region['id']
            break

# %%
# Add a REGION_ID attribute to the data set
crashes_data['REGION_ID'] = crashes_region_ids

# %%
# Write a new version of the data set to disk
crashes_data.to_csv('data/crashes_2019_regions.csv', index=False)

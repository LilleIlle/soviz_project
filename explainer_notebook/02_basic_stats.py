# %% [markdown]
# # 2. Basic Stats
#
# ### Data Cleaning
# The Crashes data set has 49 attributes and—at the time of writing—404000 data objects.
#  In the format of a CSV file it takes up 222 MB of storage.
# Gathering of the data began in 2015 and has since been updated daily.
# It is thus a fairly large data set and we early on in the process deemed necessary to narrow down in "scope" - both in terms of time and attributes.
# For this project, traffic is analyzed over the course of a full year to be able to analyze the temporal variations throughout a full year.
# Thus, only crashes that took place during 2019 (the most recent full year) are considered:
# %%
import pandas as pd
import datetime
import numpy as np

# %%
# Load the Crashes data set:
data = pd.read_csv('./data/Traffic_Crashes_-_Crashes.csv')

# %%
# Filter to only consider rows where CRASH_DATE is within the year of 2019
is_after_start_date = datetime.date(2019, 1, 1) <= pd.to_datetime(data['CRASH_DATE']).dt.date
is_before_end_date = pd.to_datetime(data['CRASH_DATE']).dt.date < datetime.date(2020, 1, 1)

# %% [markdown]
# As the location of each crash plays an important role in this project,
# data objects with empty values for location are removed:
#
# %%
# Filter out rows where LOCATION is nan
data = data.dropna(subset=['LOCATION'])
# TODO: Show how many rows were removed

# %% [markdown]
#
# Several attributes were removed; either because they were deemed irrelevant or because
# contained too many empty values:
#
# %%
# Remove unused columns
filter_columns = ['STATEMENTS_TAKEN_I', 'CRASH_DATE_EST_I', 'PHOTOS_TAKEN_I', 'WORKERS_PRESENT_I', 'WORK_ZONE_I',
                  'WORK_ZONE_TYPE', 'DATE_POLICE_NOTIFIED', 'REPORT_TYPE', 'LANE_CNT']

data = data.drop(columns=filter_columns)

# %%
# Create a new .csv file that only contains data from 2019
data.loc[is_after_start_date & is_before_end_date].to_csv('data/crashes_2019.csv', index=False)
data = None

# %% [markdown]
# The Congestion data set has 17 attributes and—at the time of writing—3.07 million data objects.
# In the format of a CSV file it takes up 669 MB of storage.
# Gathering of data began in 2018 and has since been updated every 10 minutes—hence the large size of the set.
# As with the Crashes data set, only data for 2019 is considered:
#
# %%
# Load the Congestion data set:
data = pd.read_csv('./data/Chicago_Traffic_Tracker_-_Historical_Congestion_Estimates_by_Region_-_2018-Current.csv')

# %%
# Filter to only consider rows where TIME is within the year of 2019
is_after_start_date = datetime.date(2019, 1, 1) <= pd.to_datetime(data['TIME']).dt.date
is_before_end_date = pd.to_datetime(data['TIME']).dt.date < datetime.date(2020, 1, 1)

# %%
# Create a new .csv file that only contains data from 2019
data.loc[is_after_start_date & is_before_end_date].to_csv('data/congestion_2019.csv', index=False)
data = None

# %% [markdown]
# With the two data sets cleaned and filtered to only contain data for 2019,
# their combined size is now reduced to 377 MB.
#
#
# ### Preprocessing
#
# The Congestion data set holds information on estimated congestion at 10 minute intervals for each region of the City of
# Chicago.
# A region is defined in terms of an ID, a name as well as long- and latitudes defining its bounds.
# Given the long- and latitude of crash, it is possible to find the region within which the crash took place.
# The found region ID is then added as an attribute to the Crashes data set for each crash.
#
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

# %% [markdown]
# ### Basic statistics
#
# > TODO: Insert map with region numbers
#
# > TODO: Basic stats bokeh plots
# %%


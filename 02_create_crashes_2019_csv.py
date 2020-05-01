import pandas as pd
import datetime


# Load the Crashes data set, available here:
# https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if
filename = './data/Traffic_Crashes_-_Crashes.csv'
data = pd.read_csv(filename)

# %%
# Filter to only consider rows where CRASH_DATE is within the year of 2019

is_after_start_date = datetime.date(2019, 1, 1) <= pd.to_datetime(data['CRASH_DATE']).dt.date
is_before_end_date = pd.to_datetime(data['CRASH_DATE']).dt.date < datetime.date(2020, 1, 1)

# %%
# Create a new .csv file that only contains data from 2019

data.loc[is_after_start_date & is_before_end_date].to_csv('data/crashes_2019.csv', index=False)

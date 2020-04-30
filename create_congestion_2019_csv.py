import pandas as pd
import datetime


# Load the Congestion data set, available here:
# https://data.cityofchicago.org/dataset/Chicago-Traffic-Tracker-Historical-Congestion-Esti/kf7e-cur8
filename = './data/Chicago_Traffic_Tracker_-_Historical_Congestion_Estimates_by_Region_-_2018-Current.csv'
data = pd.read_csv(filename)

# %%
# Filter to only consider rows where TIME is within the year of 2019

is_after_start_date = datetime.date(2019, 1, 1) <= pd.to_datetime(data['TIME']).dt.date
is_before_end_date = pd.to_datetime(data['TIME']).dt.date < datetime.date(2020, 1, 1)

# %%
# Create a new .csv file that only contains data from 2019

data.loc[is_after_start_date & is_before_end_date].to_csv('data/congestion_2019.csv', index=False)

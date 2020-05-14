# 2. Basic Stats

### Data Cleaning
The Crashes data set has 49 attributes and—at the time of writing—404000 data objects.
 In the format of a CSV file it takes up 222 MB of storage.
Gathering of the data began in 2015 and has since been updated daily.
It is thus a fairly large data set and we early on in the process deemed necessary to narrow down in "scope" - both in terms of time and attributes.
For this project, traffic is analyzed over the course of a full year to be able to analyze the temporal variations throughout a full year.
Thus, only crashes that took place during 2019 (the most recent full year) are considered:

> code showing filtering: `02_create_crashes_2019_csv.py`

As the location of each crash plays an important role in this project,
data objects with empty values for location are removed:

> TODO: Show how many rows were removed  
> code showing filtering: `02_create_crashes_2019_csv.py`

Several attributes were removed; either because they were deemed irrelevant or because
contained too many empty values: 

> code showing filtering: `02_create_crashes_2019_csv.py`

The Congestion data set has 17 attributes and—at the time of writing—3.07 million data objects.
In the format of a CSV file it takes up 669 MB of storage.
Gathering of data began in 2018 and has since been updated every 10 minutes—hence the large size of the set.
As with the Crashes data set, only data for 2019 is considered:

> code showing filtering: `02_create_congestion_2019_csv.py`

With the two data sets cleaned and filtered to only contain data for 2019,
their combined size is now reduced to 377 MB.


### Preprocessing

The Congestion data set holds information on estimated congestion at 10 minute intervals for each region of the City of
Chicago.
A region is defined in terms of an ID, a name as well as long- and latitudes defining its bounds.
Given the long- and latitude of crash, it is possible to find the region within which the crash took place.
The found region ID is then added as an attribute to the Crashes data set for each crash.

> code showing preprocessing: `02_create_crashes_2019_regions_csv.py`

### Basic statistics

> TODO: Insert map with region numbers

> TODO: Basic stats bokeh plots


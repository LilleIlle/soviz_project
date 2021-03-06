# %% [markdown]
# # 2. Basic Stats
#
# ### Data Cleaning
# Before we break down out data cleaning of the Chicago data sets, we quickly want to mention that we initially planned to analyze
# New York City traffic (as shown in our project video). However, after a short period of time into the data cleaning process of
# the NYC data set, we found that the quality of the data set was low; use of manually typed labels where they
# should have used categorized labels, missing data etc.. We later found the Chicago data set which had a much higher quality,
# so we decided to pivot, but keep the overall topic of the project.
#
# The Crashes data set has 49 attributes and—at the time of writing—404000 data objects.
#  In the format of a CSV file it takes up 222 MB of storage.
# Gathering of the data began in 2015 and has since been updated daily.
# It is thus a fairly large data set and we early on in the process deemed necessary to narrow down in "scope" - both in terms of time and attributes.
# For this project, traffic is analyzed over the course of a full year to be able to analyze the temporal variations throughout a full year.
# Thus, only crashes that took place during 2019 (the most recent full year) are considered:
# %%
# Load the Crashes data set:
if dev:
    data = pd.read_csv('../data/Traffic_Crashes_-_Crashes.csv')

    # Filter to only consider rows where CRASH_DATE is within the year of 2019
    is_after_start_date = datetime.date(
        2019, 1, 1) <= pd.to_datetime(data['CRASH_DATE']).dt.date
    is_before_end_date = pd.to_datetime(
        data['CRASH_DATE']).dt.date < datetime.date(2020, 1, 1)

# %% [markdown]
# As the location of each crash plays an important role in this project,
# data objects with empty values for location are removed:
#
# %%
# Filter out rows where LOCATION is nan
if dev:
    data = data.dropna(subset=['LOCATION'])

# %% [markdown]
#
# Several attributes were removed; either because they were deemed irrelevant or because
# contained too many empty values:
#
# %%
if dev:
    # Remove unused columns
    filter_columns = ['STATEMENTS_TAKEN_I', 'CRASH_DATE_EST_I', 'PHOTOS_TAKEN_I', 'WORKERS_PRESENT_I', 'WORK_ZONE_I',
                      'WORK_ZONE_TYPE', 'DATE_POLICE_NOTIFIED', 'REPORT_TYPE', 'LANE_CNT']

    data = data.drop(columns=filter_columns)

    # Create a new .csv file that only contains data from 2019
    data.loc[is_after_start_date & is_before_end_date].to_csv(
        '../data/crashes_2019.csv', index=False)
    data = None

# %% [markdown]
# The Congestion data set has 17 attributes and—at the time of writing—3.07 million data objects.
# In the format of a CSV file it takes up 669 MB of storage.
# Gathering of data began in 2018 and has since been updated every 10 minutes—hence the large size of the set.
# As with the Crashes data set, only data for 2019 is considered:
#
# %%
if dev:
    # Load the Congestion data set:
    data = pd.read_csv(
        '../data/Chicago_Traffic_Tracker_-_Historical_Congestion_Estimates_by_Region_-_2018-Current.csv')

    # Filter to only consider rows where TIME is within the year of 2019
    is_after_start_date = datetime.date(
        2019, 1, 1) <= pd.to_datetime(data['TIME']).dt.date
    is_before_end_date = pd.to_datetime(
        data['TIME']).dt.date < datetime.date(2020, 1, 1)

    # Create a new .csv file that only contains data from 2019
    data.loc[is_after_start_date & is_before_end_date].to_csv(
        '../data/congestion_2019.csv', index=False)
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
if dev:
    # Load the Congestion 2019 data set
    congestion_data = pd.read_csv('../data/congestion_2019.csv')

    # Extract a list of unique region IDs
    region_ids = congestion_data['REGION_ID'].unique()

    # Create a dictionary of regions with ID and corner locations

    regions = []
    for region_id in region_ids:
        region_specimen = congestion_data.loc[congestion_data['REGION_ID']
                                              == region_id].iloc[0]
        nw_loc = (region_specimen['WEST'], region_specimen['NORTH'])
        se_loc = (region_specimen['EAST'], region_specimen['SOUTH'])
        regions.append({
            'id': region_id,
            'nw': nw_loc,
            'se': se_loc,
        })

    def is_crash_in_region(crash_loc, region_nw_loc, region_se_loc):
        """Given the location of a crash and the corners of a region, return true if the crash took place within the region, false otherwise."""
        foo = min(region_nw_loc[0], region_se_loc[0]) < crash_loc[0] < max(
            region_nw_loc[0], region_se_loc[0])
        bar = min(region_nw_loc[1], region_se_loc[1]) < crash_loc[1] < max(
            region_nw_loc[1], region_se_loc[1])
        return foo and bar

    # Load the Crashes 2019 data set
    crashes_data = pd.read_csv('../data/crashes_2019.csv')
    N = len(crashes_data)

    # Create a list with a region ID for each row (defaulting to -1)

    crashes_region_ids = np.full(N, -1)
    for idx, row in crashes_data.iterrows():
        loc = (row['LONGITUDE'], row['LATITUDE'])
        for region in regions:
            if is_crash_in_region(loc, region['nw'], region['se']):
                crashes_region_ids[idx] = region['id']
                break

    # Add a REGION_ID attribute to the data set
    crashes_data['REGION_ID'] = crashes_region_ids

    # Write a new version of the data set to disk
    crashes_data.to_csv('../data/crashes_2019_regions.csv', index=False)

# %% [markdown]
# ### Basic statistics
#

# %%
if dev:
    crashes = pd.read_csv("../data/crashes_2019_regions.csv")
    regions = pd.read_csv("../data/congestion_2019.csv")

    cols = ['LATITUDE', 'LONGITUDE', 'REGION_ID']
    locations = crashes.loc[:, cols]

    # Calculate center for each region
    region_idx = np.sort(regions.REGION_ID.unique())
    centers = []
    for i in region_idx:
        # First row for the region
        regions[(regions.REGION_ID == 2)].iloc[0]
        north = regions[(regions.REGION_ID == i)].iloc[0].NORTH
        south = regions[(regions.REGION_ID == i)].iloc[0].SOUTH
        east = regions[(regions.REGION_ID == i)].iloc[0].EAST
        west = regions[(regions.REGION_ID == i)].iloc[0].WEST
        centers.append({
            'id': i,
            'center_x': (east + west)/2,
            'center_y': (north+south)/2
        })
    # idx = np.arange(0, 255, int(256 / 29))
    # colors = np.array(Turbo256)[idx]
    colors = np.append(Category20[20], Category20b[10])
    lon = -87.6298
    lat = 41.8281
    CHI_map = folium.Map([lat, lon], tiles="Stamen Toner", zoom_start=10.5)

    for i, row in locations.iterrows():
        # TODO: Only for hand-in..
        break
        region = row.REGION_ID
        if region == -1:
            continue

        loc = (row['LATITUDE'], row['LONGITUDE'])
        folium.CircleMarker((loc[0], loc[1]),
                            radius=.15,
                            fill=True,
                            opacity=.6,
                            color=colors[int(row.REGION_ID)]).add_to(CHI_map)

    for region in centers:
        folium.Marker(location=(region["center_y"], region["center_x"]),
                      icon=folium.DivIcon(
            html=f"""<div style="background-color:rgba(255,255,255,.7); border-radius:50%; width:20px">
                                        <div style="color:black; font-size:14px; width:fit-content; margin:auto; font-weight: 600">{region["id"]}</div>
                                    </div>""")
        ).add_to(CHI_map)
    # CHI_map.save("../web/folium/chi_regions.html")
Image('../web/folium/pngs/regions.png')
# %% [markdown]
# As described in the *Motivation* section, Chicago is divided into 29 regions in order to estimate traffic congestion around the city.
# To visualize this partition, all crashes has been plotted with a unique color for each region.
# To ease the relation between future findings and location of the regions, the unique IDs are added to the figure.
# %%
if dev:
    crashes = pd.read_csv("../data/crashes_2019_regions.csv")
    # BASIC PRIMARY CAUSE PLOT
    output_file("../web/bokeh/primary_cause_bar_chart.html")

    crashes_primary = crashes[(crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'UNABLE TO DETERMINE')
                              & (crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'NOT APPLICABLE')]
    cp = crashes[(crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'UNABLE TO DETERMINE')
                 & (crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'NOT APPLICABLE')].PRIM_CONTRIBUTORY_CAUSE.unique()
    counts = None
    counts = crashes_primary['PRIM_CONTRIBUTORY_CAUSE'].value_counts(
    ).sort_values()

    TOOLTIPS = [
        ("Number of crashes", "@top")
    ]

    p = figure(x_range=counts.index.values,
               plot_height=1050,
               plot_width=1050,
               toolbar_location=None,
               tools='',
               tooltips=TOOLTIPS,
               y_axis_label='Number of Crashes',
               min_border_right=250)
    # frame_width=1600)
    # y_axis_type="log")

    p.vbar(x=counts.index.values, top=counts, width=0.5, fill_alpha=0.25,
           fill_color='#000000', line_color='#000000', bottom=0.01)
    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = -0.4 * math.pi/2
    p.y_range.start = 0
    #plots = bokeh.gridplot([[p]], sizing_mode='scale_width')
    show(p)
display(HTML("<iframe src='https://chicago-traffic.netlify.app/bokeh/primary_cause_bar_chart.html' height='750' width='1000'></iframe>"))
# %% [markdown]
# One interesting attribute of the Crashes data set is the 'PRIMARY CONTRIBUTORY CAUSE'.
# The figure above shows the distribution of causes over all crashes of 2019.
# It is seen that the two most common causes by far are 'FAILING TO YIELD RIGHT-OF-WAY' and 'FOLLOWING TOO CLOSELY'.

# The large range in number of crashes in the figure makes it difficult to read the values of the left most part.
# The tooltip functionality of Bokeh is of no use because the bars are so small.
# This can be remedied by using a log scale for the y-axis:
# %%
# BASIC PRIMARY CAUSE PLOT (LOG Y-AXIS)
if dev:
    output_file("../web/bokeh/primary_cause_bar_chart_log.html")

    crashes_primary = crashes[(crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'UNABLE TO DETERMINE')
                              & (crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'NOT APPLICABLE')]
    cp = crashes[(crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'UNABLE TO DETERMINE')
                 & (crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'NOT APPLICABLE')].PRIM_CONTRIBUTORY_CAUSE.unique()
    counts = None
    counts = crashes_primary['PRIM_CONTRIBUTORY_CAUSE'].value_counts(
    ).sort_values()

    TOOLTIPS = [
        ("Number of crashes", "@top")
    ]

    p = figure(x_range=counts.index.values,
               plot_height=1050,
               plot_width=1050,
               toolbar_location=None,
               tools='',
               tooltips=TOOLTIPS,
               y_axis_label='Number of Crashes',
               y_axis_type="log",
               min_border_right=250)

    p.vbar(x=counts.index.values, top=counts, width=0.5, fill_alpha=0.25,
           fill_color='#000000', line_color='#000000', bottom=0.01)
    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = -0.4 * math.pi/2
    p.y_range.start = 10**(0)
    show(p)
display(HTML("<iframe src='https://chicago-traffic.netlify.app/bokeh/primary_cause_bar_chart_log.html' height='750' width='1000'></iframe>"))
# %% [markdown]
# The figure above shows the same data as the previous figure, but with a log-10 scale for the y-axis resulting in
# in a more readable chart. Now, all the bars are tall enough to afford the tooltip functionality of Bokeh—hovering the
# cursor over the bar for _Motorcycle advancing legally on red light_ reveals a total number of crashes of 6.
# %%
# BASIC REGION CRASH BAR CHART
if dev:
    output_file("../web/bokeh/region_bar_chart.html")

    congestion = pd.read_csv("../data/congestion_2019.csv")
    crashes = crashes[crashes['REGION_ID'] != -1]

    region_id_region = congestion.groupby(
        ['REGION_ID', 'REGION']).size().index.values
    region_dict = dict(region_id_region)
    crashes['REGION_PRETTY'] = [str(x) + ": " + region_dict.get(x)
                                for x in crashes['REGION_ID']]
    congestion['REGION_PRETTY'] = [
        str(x) + ": " + region_dict.get(x) for x in congestion['REGION_ID']]

    counts = None
    counts = crashes.groupby('REGION_PRETTY').size().sort_values()
    cx = counts.index.values.astype(str)

    TOOLTIPS = [
        ("Number of crashes", "@top")
    ]

    p = figure(x_range=cx,
               plot_height=500,
               plot_width=700,
               toolbar_location=None,
               tools='',
               tooltips=TOOLTIPS,
               y_axis_label='Number of Crashes',
               x_axis_label='Region',
               min_border_right=150)

    p.vbar(x=cx, top=counts, width=0.5, fill_alpha=0.25,
           fill_color='#000000', line_color='#000000'),  # bottom=0.01)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = -0.4 * math.pi/2
    #p.xaxis.ticker = list(range(1, 30))
    show(p)
display(HTML("<iframe src='https://chicago-traffic.netlify.app/bokeh/region_bar_chart.html' height='750' width='1000'></iframe>"))
# %% [markdown]
# The figure above shows the distribution of crashes over all 29 regions for 2019.
# It is seen that the region _South West Side_ (with ID 18) is suffering the most from crashes,
# whereas _Riverdale-Hegewisch_ (with ID 28) is the region with the least crashes.
# %%
# BASIC REGION AVG SPEED BAR CHART
if dev:
    output_file("../web/bokeh/region_avg_speed_bar_chart.html")

    congestion = pd.read_csv("../data/congestion_2019.csv")

    region_id_region = congestion.groupby(
        ['REGION_ID', 'REGION']).size().index.values
    region_dict = dict(region_id_region)
    crashes['REGION_PRETTY'] = [str(x) + ": " + region_dict.get(x)
                                for x in crashes['REGION_ID']]
    congestion['REGION_PRETTY'] = [
        str(x) + ": " + region_dict.get(x) for x in congestion['REGION_ID']]

    avg_speed = congestion.groupby('REGION_PRETTY')[
        'SPEED'].mean().sort_values()
    counts = None
    counts = avg_speed
    cx = counts.index.values.astype(str)

    TOOLTIPS = [
        ("Average speed (mph)", "@top")
    ]
    # np.sort(congestion['REGION_ID'].unique, axis=None
    p = figure(  # x_range=(1, 29),
        # FactorRange(factors=str(counts.index.values)),
        # x_range=counts.index.values.astype(str),
        x_range=cx,
        plot_height=500,
        plot_width=700,
        toolbar_location=None,
        tools='',
        tooltips=TOOLTIPS,
        y_axis_label='Average Speed (mph)',
        x_axis_label='Region',
        min_border_right=150)

    p.vbar(x=cx, top=counts, width=0.5, fill_alpha=0.25,
           fill_color='#000000', line_color='#000000'),  # bottom=0.01)
    p.xgrid.grid_line_color = None
    p.y_range.start = 15
    p.xaxis.major_label_orientation = -0.4 * math.pi/2
    #p.xaxis.ticker = list(range(1, 30))
    show(p)
display(HTML("<iframe src='https://chicago-traffic.netlify.app/bokeh/region_avg_speed_bar_chart.html' height='750' width='1000'></iframe>"))
# %% [markdown]
# The figure above shows the average speed for public transportation buses for all 29 regions for 2019.
# It is seen that buses servicing the region _Chicago Loop_ (with ID 13) has the lowest average speed,
# whereas buses in the region _Washington Hts-Roseland-Pullman_ (with ID 26) has the highest average speed.
# Chicago Loop is Chicago's official downtown area, which is "celebrated for its dynamic architecture and big city buzz" according
# to the tourist web site https://www.choosechicago.com/. It features a high population density of 8200/km<sup>2</sup> (according to this report https://www.cmap.illinois.gov/documents/10180/126764/The+Loop.pdf from Chicago Metropolitan Agency for Planning (CMAP).
# On the other hand, areas further away from the Loop, e.g. _Washington Hts-Roseland-Pullman_ (with ID 26) with the highest average speed,
# has a much lower population density with 3373/km<sup>2</sup> (according to this report https://www.cmap.illinois.gov/documents/10180/126764/Roseland.pdf also from CMAP).
# The average speed of the buses is considered a measure for the level of traffic congestion across the regions, as the level of congestion is correlated to the amount of traffic on the
# streets—the lower the average speed, the more vehicles on the streets.
# In summary, we see higher average speeds outside downtown Chicago as these areas has less traffic congestion, not least due to
# much lower population density. Later we will consider the severity (i.e. the mortality and injuries suffered) in the different regions.

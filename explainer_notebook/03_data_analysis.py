# %%
import pandas as pd
import numpy as np
from bokeh.palettes import Category20, Category20b, Turbo256, Reds
from bokeh.io import output_file, show, save, output_notebook
from bokeh.models import ColumnDataSource, FactorRange, Legend, LinearAxis, Range1d
import seaborn as sns
from bokeh.transform import dodge
from bokeh.plotting import figure
import matplotlib as plt
import folium
import bokeh
from folium.plugins import HeatMap, HeatMapWithTime
from folium import plugins
import math
from IPython.display import Image

# %%
output_notebook()
# %% [markdown]
# # 3. Data Analysis
# %%
crashes = pd.read_csv("../data/crashes_2019_regions.csv")
# %%
#
# ### Monthly and Weekly Temporal Patterns
#
# %% [markdown]
# ##############################################################################################################
# ### CRASH COUNT MONTHS PLOT
# %%
output_file("../web/bokeh/months_barchart.html")
x = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
     'August', 'September', 'October', 'November', 'December']
counts = crashes['CRASH_MONTH'].value_counts().sort_index()

TOOLTIPS = [
    #("Hour", "$index"),
    #("Day", "@x"),
    ("Number of crashes", "@top")
]

p = figure(x_range=x,
           plot_height=450,
           plot_width=800,
           title="Monthly Crash Distribution",
           toolbar_location=None,
           tools='',
           tooltips=TOOLTIPS,
           y_axis_label='Number of Crashes',
           x_axis_label='Month')

p.vbar(x=x, top=counts, width=0.5, fill_alpha=0.25,
       fill_color='#000000', line_color='#000000')

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)
# %% [markdown]
# ##############################################################################################################
# ### CRASH COUNT DAYS PLOT
# %%
output_file("../web/bokeh/days_barchart.html")

weekdays = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']
counts = crashes['CRASH_DAY_OF_WEEK'].value_counts().sort_index()

TOOLTIPS = [
    #("Hour", "$index"),
    #("Day", "@x"),
    ("Number of crashes", "@top")
]

p = figure(x_range=weekdays,
           plot_height=450,
           toolbar_location=None,
           tools='',
           tooltips=TOOLTIPS,
           y_axis_label='Number of Crashes',
           x_axis_label='Day of the Week')

p.vbar(x=weekdays, top=counts, width=0.5, fill_alpha=0.25,
       fill_color='#000000', line_color='#000000')

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)
# %%
# > TODO: Heat map of weekly pattern
#
# ### Daily Temporal Patterns
#
# %% [markdown]
# ##############################################################################################################
# ### HOUR PLOT HISTOGRAM
# %%
output_file("../web/bokeh/hours_barchart.html")

hours = pd.DataFrame({'CRASH_HOUR': np.arange(0, 24)})

x = np.sort(crashes['CRASH_HOUR'].unique()).tolist()
xx = x.copy()
xx.append(24)
counts = crashes['CRASH_HOUR'].value_counts().sort_index()

TOOLTIPS = [
    ("Crashes", "@top"),
]

p = figure(plot_height=450,
           plot_width=800,
           title="Hourly Crash Distribution",
           toolbar_location=None,
           tools='',
           tooltips=TOOLTIPS,
           y_axis_label='Number of Crashes',
           x_axis_label='Hour')

p.quad(top=counts, left=xx[:-1], right=xx[1:], width=0.5,
       fill_color='#000000', line_color='#000000', fill_alpha=0.25)

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.ticker = list(range(0, 24))

show(p)
# %% [markdown]
# ##############################################################################################################
# ### HOUR PLOT HISTOGRAM WITH AVERAGE SPEED TREND LINE
# %%
congestion = pd.read_csv("../data/congestion_2019.csv")
output_file("../web/bokeh/hours_congestion_barchart.html")

congestion = congestion[congestion['SPEED'] > 0.0]
regions_congestion = congestion.groupby(['REGION_ID', 'HOUR'])['SPEED'].mean()
hour_congestion = congestion.groupby('HOUR')['SPEED'].mean()


hours = pd.DataFrame({'CRASH_HOUR': np.arange(0, 24)})

x = np.sort(crashes['CRASH_HOUR'].unique()).tolist()
xx = x.copy()
xx.append(24)
counts = crashes['CRASH_HOUR'].value_counts().sort_index()

# TOOLTIPS = [
#    ("Crashes", "@top"),
# ]


p = figure(  # x_range=(-0.5,23.5),
    plot_height=450,
    plot_width=800,
    title="Hourly Crash Distribution",
    toolbar_location=None,
    tools='',
    # tooltips=TOOLTIPS,
    y_axis_label='Number of Crashes',
    x_axis_label='Hour')

#p.yaxis.axis_line_color = "navy"
# p.vbar(x=x, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000')
p.quad(top=counts, left=xx[:-1], right=xx[1:], width=0.5,
       fill_color='#000000', line_color='#000000', fill_alpha=0.25)

p.extra_y_ranges = {'SPEED': Range1d(
    start=(hour_congestion.min()-0.25), end=(hour_congestion.max())+0.25)}
p.add_layout(LinearAxis(y_range_name='SPEED',
                        axis_label="Average mph", axis_line_color='red'), 'right')

extra_value_y = pd.Series([hour_congestion[0]], index=[24])
hour_congestion = hour_congestion.append(extra_value_y)
p.line(xx, hour_congestion.array, line_width=1,
       y_range_name='SPEED', line_color="red")


p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.ticker = list(range(0, 24))

show(p)
# %% [markdown]
# ##############################################################################################################
# ### CRASH COUNT VS. AVERAGE SPEED SCATTERPLOT
# %%
# TODO: Don't use hardcoded dicts
region_crashes_tally = {3: 5199, 15: 4024, 18: 7739, 19: 4021, 2: 4114, 8: 6159, 26: 3923, 6: 4895, 7: 4922, 20: 3413,
                        13: 5461, 22: 2267, 10: 6406, 5: 6591, 11: 6782, 4: 2940, 14: 4409, 16: 2847, 28: 1049, 9: 2873,
                        23: 4908, 12: 4140, 21: 3190, 24: 3625, 1: 2592, 17: 1288, 27: 1477, 25: 1832, 29: 2407,
                        -1: 801}

region_speed_means = {1: 20.577022889511255, 2: 26.68329213080924, 6: 22.633488102758474, 21: 23.674691823369628,
                      7: 21.460690040008423, 18: 25.10555749752574, 29: 19.161841900229525, 22: 27.68232664406494,
                      10: 23.731599250384285, 14: 24.040862286797218, 3: 23.235282065320387, 23: 24.224279517361918,
                      28: 20.995748278548717, 13: 18.773307222573173, 8: 20.809373144385255, 4: 20.18918570616353,
                      19: 26.006200593821728, 17: 24.532245198787063, 12: 19.132034112444728, 27: 28.521725241634904,
                      24: 24.968908799932617, 9: 22.66006338042998, 20: 25.892239044831435, 5: 22.866837583440375,
                      16: 24.206990186994606, 11: 22.74667487892188, 25: 25.541196908757822, 26: 28.672279475246896,
                      15: 25.74476016003369}

x = np.zeros(29)
for key, val in region_crashes_tally.items():
    if key == -1:
        break
    x[key - 1] = val

y = np.zeros(29)
for key, val in region_speed_means.items():
    y[key - 1] = val

TOOLTIPS = [
    ("Region ID", "$index"),
    ("Number of crashes", "@x"),
    ("Avg. speed (mph)", "@y{(0.0)}"),
]

# create a new plot with a title and axis labels
p = figure(
    x_axis_label='Number of Crashes',
    y_axis_label='Avg. Speed',
    toolbar_location=None,
    tools='',
    tooltips=TOOLTIPS,
    sizing_mode='stretch_both',
)

p.circle(x, y, size=18, fill_color="black",
         fill_alpha=0.25, line_color="black")

# Output to static HTML file
output_file("../web/bokeh/crash_count_vs_avg_speed.html")
show(p)
# %% [markdown]
# ##############################################################################################################
# ### PRIMARY CAUSE BOKEH
# %%
crashes = pd.read_csv("../data/crashes_2019_regions.csv")
# %%
output_file("../web/bokeh/primary_cause.html")
# %%
# Filtering the primary causes 'UNABLE TO DETERMINE' and 'NOT APPLICABLE' as we deem this irrelevant for the purpose of the plot
crashes_primary = crashes[(crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'UNABLE TO DETERMINE')
                          & (crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'NOT APPLICABLE')]
# %%
# Filtering all primary causes that have 150 or less occurences in the 2019 data set.
cx = crashes_primary.groupby('PRIM_CONTRIBUTORY_CAUSE')
cx = cx.filter(lambda x: len(x) > 150)
# crashes_primary.PRIM_CONTRIBUTORY_CAUSE.unique()
cp = cx.PRIM_CONTRIBUTORY_CAUSE.unique()

# %%
# Counting occurences across the day for each cause
causes_norm = pd.DataFrame({'CRASH_HOUR': np.arange(1, 25)})
for cause in cp:
    cause_hist = crashes_primary[crashes_primary['PRIM_CONTRIBUTORY_CAUSE'] == cause].groupby(
        'CRASH_HOUR').size()
    # cause_hist_norm = (cause_hist / cause_hist.sum()) # distribution for a given cause seen only in context of the cause
    causes_norm[cause] = cause_hist
causes_norm.fillna(0)

# %%
source = causes_norm
# %%
# TOOLTIPS = [
#    ("Crashes", "@i"),
# ]
p = figure(x_range=FactorRange(factors=causes_norm.CRASH_HOUR.astype(str)),
           y_axis_type="log",
           title="Crash primary causes throughout the day",
           tools='',
           # tooltips=TOOLTIPS,
           x_axis_label='Hour of the day',
           y_axis_label='Number of crashes',
           plot_width=1700,
           plot_height=725,
           toolbar_location=None,
           sizing_mode='stretch_width')

# %%
bar = {}
colors = np.append(Category20[20], Category20b[20])
items = []

for indx, i in enumerate(cp):
    bar[i] = p.vbar(x=dodge('CRASH_HOUR', -.5, range=p.x_range), top=i, source=source, muted_alpha=0.01, muted=True,
                    width=.5, fill_color=colors[indx], bottom=0.01, alpha=0.6)
    items.append((i, [bar[i]]))
# %%
legend = Legend(items=items)
p.add_layout(legend, 'right')
p.legend.label_text_font_size = '8pt'
p.legend.click_policy = "mute"
p.y_range.start = 0
# %%
show(p)
# %%
# ##############################################################################################################
# %%
crashes = pd.read_csv("../data/crashes_2019_regions.csv")
chi_bounding = {
    "lon": -87.6298,
    "lat": 41.8281
}
map_location = [chi_bounding['lat'], chi_bounding['lon']]
map_zoom = 10.5
# %%
# Static heat map crashes
# TODO: Write text
CHI_map = folium.Map(map_location, tiles="Stamen Toner", zoom_start=map_zoom)
points = crashes.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
lat = points['LATITUDE'].values
lon = points['LONGITUDE'].values
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=20, radius=12).add_to(CHI_map)
CHI_map.save("../web/folium/heat_crashes.html")
CHI_map
# %%
# Heat map over time - Hour
# TODO: Write text
CHI_map_time = folium.Map(
    map_location, tiles="Stamen Toner", zoom_start=map_zoom)
heat_df = crashes.loc[:, ['LATITUDE', 'LONGITUDE', 'CRASH_DATE']].dropna()

# Create weight column, using date
heat_df['Weight'] = pd.to_datetime(heat_df['CRASH_DATE']).dt.hour
heat_df['Weight'] = heat_df['Weight'].astype(float).dropna()

# List comprehension to make out list of lists
heat_data = [[[row['LATITUDE'], row['LONGITUDE']] for _, row in heat_df[heat_df['Weight'] == i].iterrows()] for i in
             range(0, 24)]

# Plot it on the map
hm = plugins.HeatMapWithTime(heat_data,
                             auto_play=False,
                             radius=4,
                             position="topright"
                             )
hm.add_to(CHI_map_time)
CHI_map_time.save("../web/folium/heat_crashes_over_time.html")
CHI_map_time

# %%
# TODO: Insert text
# Static heat map fatal
CHI_map = folium.Map(map_location, tiles="Stamen Toner", zoom_start=map_zoom)
incapacitating_injuries = crashes["INJURIES_INCAPACITATING"] > 0
fatal_injuries = crashes["INJURIES_FATAL"] > 0
data = crashes[fatal_injuries]
points = data.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=15, radius=25).add_to(CHI_map)
CHI_map.save("../web/folium/heat_fatal.html")
CHI_map

# %%
# TODO: Insert text
# Static heat map incapacitating
CHI_map = folium.Map(map_location, tiles="Stamen Toner", zoom_start=map_zoom)
data = crashes[incapacitating_injuries]
points = data.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=15, radius=13).add_to(CHI_map)
CHI_map.save("../web/folium/heat_incapacitating.html")
CHI_map

# %%
# TODO: Insert text
# Static heat map fatal and incapacitating
CHI_map = folium.Map(map_location, tiles="Stamen Toner", zoom_start=map_zoom)
incapacitating_injuries = crashes["INJURIES_INCAPACITATING"] > 0
data = crashes[incapacitating_injuries | fatal_injuries]
points = data.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=14, radius=12).add_to(CHI_map)
CHI_map.save("../web/folium/heat_fatal_and_incapacitating.html")
CHI_map

# %%
# Calculating the ratio for fatal and incapacitating crashes
# TODO: Insert text
crashes = pd.read_csv("../data/crashes_2019_regions.csv")
crashes = crashes[crashes['REGION_ID'] != -1]
region_crashes = crashes.groupby(
    'REGION_ID')['CRASH_DATE'].count().sort_values()
crashes_fatal_incapacitating = crashes[(crashes['INJURIES_FATAL'] > 0) | (
    crashes['INJURIES_INCAPACITATING'] > 0)]
region_crashes_fatal_incapacitating = crashes_fatal_incapacitating.groupby(
    'REGION_ID')['CRASH_RECORD_ID'].count().sort_values()
df = pd.concat([region_crashes, region_crashes_fatal_incapacitating], axis=1)
df = df.rename(columns={'CRASH_DATE': 'total_crashes',
                        'CRASH_RECORD_ID': 'total_fatal_incap'})
df['fraction'] = df['total_fatal_incap']/df['total_crashes']
# %%
df = pd.read_csv("../data/fatal_incap_frac.csv", index_col="REGION_ID")
# %%
# Calculating color for the different bins


def calc_color(data):
    color_sq = colors = np.flip(np.array(Reds[6]))

    colors = 'Reds'
    new_data, bins = pd.qcut(data, 6, retbins=True,
                             labels=list(range(6)))
    color_ton = []
    for val in new_data:
        color_ton.append(color_sq[val])
    colors = np.flip(np.array(Reds[6]))
    # sns.palplot(colors, 0.6)
    for i in range(6):
        print("\n"+str(i+1)+': '+str((bins[i])) +
              " => "+str((bins[i+1])), end=" ")
    print("\n\n   1   2   3   4   5   6")
    return color_ton, bins, colors


# %%
regions = pd.read_csv("../data/congestion_2019.csv")
# %%
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
# %%
color_ton, bins, colors = calc_color(data=df.fraction.to_numpy()*100)
sns.palplot(colors, 0.6)
cols = ['LATITUDE', 'LONGITUDE', 'REGION_ID']
locations = crashes.loc[:, cols]
CHI_map = folium.Map([chi_bounding["lat"], chi_bounding["lon"]],
                     tiles="Stamen Toner", zoom_start=11)

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
                        color=color_ton[int(row.REGION_ID)-1]).add_to(CHI_map)


for region in centers:
    folium.Marker(location=(region["center_y"], region["center_x"]),
                  icon=folium.DivIcon(
        html=f"""<div style="background-color:rgba(255,255,255,.7); border-radius:50%; width:20px">
                                    <div style="color:black; font-size:14px; width:fit-content; margin:auto; font-weight: 600">{region["id"]}</div>
                                </div>""")
    ).add_to(CHI_map)
CHI_map.save("../web/folium/chi_regions_fatal_incap.html")
# %%
Image("../web/folium/pngs/regions_fatal_incap.png")
# CHI_map

# %%

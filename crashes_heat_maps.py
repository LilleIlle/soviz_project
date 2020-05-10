import pandas as pd
import folium
from folium.plugins import HeatMap, HeatMapWithTime
from folium import plugins

# %%
# Setting up constants common for all maps

crashes = pd.read_csv("./data/crashes_2019_regions.csv")
chi_bounding = {
    "lon": -87.6298,
    "lat": 41.8781
}
map_location = [chi_bounding['lat'], chi_bounding['lon']]
map_zoom = 11

# %%
# Static heat map crashes
CHI_map = folium.Map(map_location, tiles="Stamen Toner", zoom_start=map_zoom)
points = crashes.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
lat = points['LATITUDE'].values
lon = points['LONGITUDE'].values
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=20, radius=12).add_to(CHI_map)
CHI_map.save("./web/folium/heat_crashes.html")

# %%
# Heat map over time - crashes
CHI_map_time = folium.Map(map_location, tiles="Stamen Toner", zoom_start=map_zoom)
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
                             radius=5,
                             position="topright"
                             )
hm.add_to(CHI_map_time)
CHI_map_time.save("./web/folium/heat_crashes_over_time.html")

# %%
# Static heat map fatal
CHI_map = folium.Map(map_location, tiles="Stamen Toner", zoom_start=map_zoom)
incapacitating_injuries = crashes["INJURIES_INCAPACITATING"] > 0
fatal_injuries = crashes["INJURIES_FATAL"] > 0
data = crashes[fatal_injuries]
points = data.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=15, radius=25).add_to(CHI_map)
CHI_map.save("./web/folium/heat_fatal.html")

# %%
# Static heat map incapacitating
CHI_map = folium.Map(map_location, tiles="Stamen Toner", zoom_start=map_zoom)
data = crashes[incapacitating_injuries]
points = data.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=15, radius=13).add_to(CHI_map)
CHI_map.save("./web/folium/heat_incapacitating.html")

# %%
# Static heat map fatal and incapacitating
CHI_map = folium.Map(map_location, tiles="Stamen Toner", zoom_start=map_zoom)
incapacitating_injuries = crashes["INJURIES_INCAPACITATING"] > 0
data = crashes[incapacitating_injuries | fatal_injuries]
points = data.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=14, radius=12).add_to(CHI_map)
CHI_map.save("./web/folium/heat_fatal_and_incapacitating.html")

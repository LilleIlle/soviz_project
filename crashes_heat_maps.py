# import webbrowser
import pandas as pd
import folium
from folium.plugins import HeatMap, HeatMapWithTime
from folium import plugins

# %%
crashes = pd.read_csv("./data/crashes_2019_regions.csv")
chi_bounding = {
    "lon": -87.6298,
    "lat": 41.8781
}

# %%
# Static heat map crashes
CHI_map = folium.Map([chi_bounding['lat'], chi_bounding['lon']], tiles="Stamen Toner", zoom_start=10.5)
points = crashes.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
lat = points['LATITUDE'].values
lon = points['LONGITUDE'].values
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=20, radius=12).add_to(CHI_map)
CHI_map.save("./maps/heat_crashes.html")
# webbrowser.open("file:///Users/mi/soviz_project/maps/chi_heat.html", new=2)

# %%
# Heat map over time - crashes
CHI_map_time = folium.Map([chi_bounding['lat'], chi_bounding['lon']], tiles="Stamen Toner", zoom_start=10.5)
heat_df = crashes.loc[:, ['LATITUDE', 'LONGITUDE', 'CRASH_DATE']].dropna()

# Create weight column, using date
heat_df['Weight'] = pd.to_datetime(heat_df['CRASH_DATE']).dt.hour
heat_df['Weight'] = heat_df['Weight'].astype(float).dropna()
# heat_df = heat_df.dropna(axis=0, subset=['Y','X', 'Weight'])


# List comprehension to make out list of lists
heat_data = [[[row['LATITUDE'], row['LONGITUDE']] for _, row in heat_df[heat_df['Weight'] == i].iterrows()] for i in
             range(0, 24)]

# Plot it on the map
hm = plugins.HeatMapWithTime(heat_data,
                             auto_play=True, max_opacity=0.7,
                             radius=5,
                             )
hm.add_to(CHI_map_time)
CHI_map_time.save("./maps/heat_crashes_over_time.html")


# %%
# Static heat map fatal
CHI_map = folium.Map([chi_bounding['lat'], chi_bounding['lon']], tiles="Stamen Toner", zoom_start=10.5)
incapacitating_injuries = crashes["INJURIES_INCAPACITATING"] > 0
fatal_injuries = crashes["INJURIES_FATAL"] > 0
# data = crashes[incapacitating_injuries_mask]
data = crashes[fatal_injuries]
points = data.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=15, radius=25).add_to(CHI_map)
CHI_map.save("./maps/heat_fatal.html")
# webbrowser.open("file:///Users/mi/soviz_project/maps/chi_heat.html", new=2)

# %%
# Static heat map incapacitating
CHI_map = folium.Map([chi_bounding['lat'], chi_bounding['lon']], tiles="Stamen Toner", zoom_start=10.5)
data = crashes[incapacitating_injuries]
points = data.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=15, radius=13).add_to(CHI_map)
CHI_map.save("./maps/heat_incapacitating.html")
# webbrowser.open("file:///Users/mi/soviz_project/maps/chi_heat.html", new=2)

# %%
# Static heat map fatal and incapacitating
CHI_map = folium.Map([chi_bounding['lat'], chi_bounding['lon']], tiles="Stamen Toner", zoom_start=10.5)
incapacitating_injuries = crashes["INJURIES_INCAPACITATING"] > 0
data = crashes[incapacitating_injuries | fatal_injuries]
points = data.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for _, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=14, radius=12).add_to(CHI_map)
CHI_map.save("./maps/heat_fatal_and_incapacitating.html")
# webbrowser.open("file:///Users/mi/soviz_project/maps/chi_heat.html", new=2)

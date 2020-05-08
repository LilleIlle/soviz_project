# import webbrowser
import pandas as pd
import folium
from folium.plugins import HeatMap
# %%
crashes = pd.read_csv("./data/crashes_2019_regions.csv")
# %%
lon = -87.6298
lat = 41.8781
CHI_map = folium.Map([lat, lon], tiles="Stamen Toner", zoom_start=10.5)

points = crashes.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
lat = points['LATITUDE'].values
lon = points['LONGITUDE'].values
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for index, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=20, radius=12).add_to(CHI_map)
CHI_map.save("./maps/chi_heat.html")
# webbrowser.open("file:///Users/mi/soviz_project/maps/chi_heat.html", new=2)

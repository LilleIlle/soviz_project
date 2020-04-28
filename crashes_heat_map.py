# %%
import webbrowser
from folium import plugins
from folium.plugins import HeatMap
# %%
lon = -87.6298
lat = 41.8781
CHI_map = folium.Map([lat, lon], tiles="Stamen Toner", zoom_start=10.5)
points = crashes.loc[:, ['LATITUDE', 'LONGITUDE']].dropna()
lat = points['LATITUDE'].values
lon = points['LONGITUDE'].values
heat_data = [[row['LATITUDE'], row['LONGITUDE']]
             for index, row in points.iterrows()]

HeatMap(data=heat_data, max_zoom=20, radius=9).add_to(CHI_map)
CHI_map.save("./maps/chi_heat.html")
CHI_map

# webbrowser.open("file:///Users/mi/soviz_project/maps/chi_heat.html", new=2)


# %%

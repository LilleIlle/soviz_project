import pandas as pd
import numpy as np
import folium
from bokeh.palettes import Category20, Category20b, Turbo256

# %%
crashes = pd.read_csv("./data/crashes_2019_regions.csv")
# %%
cols = ['LATITUDE', 'LONGITUDE', 'REGION_ID']
locations = crashes.loc[:, cols]
# %%
# idx = np.arange(0, 255, int(256 / 29))
# colors = np.array(Turbo256)[idx]
colors = np.append(Category20[20], Category20b[10])
lon = -87.6298
lat = 41.8781
CHI_map = folium.Map([lat, lon], tiles="Stamen Toner", zoom_start=10.5)

for i, row in locations.iterrows():
    region = row.REGION_ID
    if region == -1:
        continue
    if i > 50000:
        break

    loc = (row['LATITUDE'], row['LONGITUDE'])
    folium.CircleMarker((loc[0], loc[1]),
                        radius=1,
                        fill=True,
                        fill_opacity=1,
                        color=colors[int(row.REGION_ID)]).add_to(CHI_map)

CHI_map.save("./maps/chi_regions.html")
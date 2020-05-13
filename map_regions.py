# %%
import pandas as pd
import numpy as np
import folium
from bokeh.palettes import Category20, Category20b, Turbo256, Reds
import seaborn as sns

# %%
crashes = pd.read_csv("./data/crashes_2019_regions.csv")
regions = pd.read_csv("./data/congestion_2019.csv")

# %%
cols = ['LATITUDE', 'LONGITUDE', 'REGION_ID']
locations = crashes.loc[:, cols]

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
    # if i > 5000:
        # break

    loc = (row['LATITUDE'], row['LONGITUDE'])
    folium.CircleMarker((loc[0], loc[1]),
                        radius=.05,
                        fill=True,
                        opacity=.1,
                        color=colors[int(row.REGION_ID)]).add_to(CHI_map)

for region in centers:
    folium.Marker(location=(region["center_y"], region["center_x"]),
                  icon=folium.DivIcon(
        html=f"""<div style="background-color:rgba(255,255,255,.7); border-radius:50%; width:20px">
                                    <div style="color:black; font-size:14px; width:fit-content; margin:auto; font-weight: 600">{region["id"]}</div>
                                </div>""")
    ).add_to(CHI_map)
CHI_map.save("./web/folium/chi_regions.html")

# %%
df = pd.read_csv("./data/fatal_incap_frac.csv", index_col="REGION_ID")
# %%


def calc_color(data):
    color_sq = colors = np.flip(np.array(Reds[6]))

    colors = 'Reds'
    new_data, bins = pd.qcut(data, 6, retbins=True,
                             labels=list(range(6)))
    color_ton = []
    for val in new_data:
        color_ton.append(color_sq[val])
    if color != 9:
        # colors = sns.color_palette(colors, n_colors=6)
        colors = np.flip(np.array(Reds[6]))
        sns.palplot(colors, 0.6)
        for i in range(6):
            print("\n"+str(i+1)+': '+str((bins[i])) +
                  " => "+str((bins[i+1])), end=" ")
        print("\n\n   1   2   3   4   5   6")
    return color_ton, bins


# %%
# Color code for reds = 4
color = 4
color_ton, bins = calc_color(data=df.fraction.to_numpy()*100)

# %%
CHI_map = folium.Map([lat, lon], tiles="Stamen Toner", zoom_start=11)

for i, row in locations.iterrows():
    region = row.REGION_ID
    if region == -1:
        continue
    if i > 30000:
        break

    loc = (row['LATITUDE'], row['LONGITUDE'])
    # print(row.REGION_ID)
    folium.CircleMarker((loc[0], loc[1]),
                        radius=.05,
                        fill=True,
                        opacity=.8,
                        color=color_ton[int(row.REGION_ID)-1]).add_to(CHI_map)

CHI_map.save("./web/folium/chi_regions_fatal_incap.html")

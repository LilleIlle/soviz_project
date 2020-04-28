import pandas as pd
import numpy as np
import folium

# %%
regions = pd.read_csv("./data/regions.csv")

# %%
regions.loc[:, ["REGION", "REGION_ID", "WEST", "EAST", "SOUTH", "NORTH"]]

# %%
regions_coords = regions[regions.columns[:6]]
regions_coords.to_csv("./output/regions.csv", index=False)


# %%
newdf = regions_coords[regions_coords.columns[:2]]
newdf["UPPERLEFT_X"] = regions_coords[' WEST']
newdf["UPPERLEFT_Y"] = regions_coords[" NORTH"]
newdf["UPPERRIGHT_X"] = regions_coords[' EAST']
newdf["UPPERRIGHT_Y"] = regions_coords[" NORTH"]
newdf["LOWERLEFT_X"] = regions_coords[' WEST']
newdf["LOWERLEFT_Y"] = regions_coords[" SOUTH"]
newdf["LOWERRIGHT_X"] = regions_coords[' EAST']
newdf["LOWERRIGHT_Y"] = regions_coords[" SOUTH"]

# %%
newdf.to_csv("./output/regions_corners.csv", index=False)

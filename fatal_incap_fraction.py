# %%
import pandas as pd
import numpy as np
import matplotlib as plt
import folium
from bokeh.palettes import Category20, Category20b, Turbo256
from bokeh.io import output_file, show, output_notebook
from bokeh.models import ColumnDataSource, FactorRange, Legend
from bokeh.plotting import figure
from bokeh.transform import dodge
import math
import bokeh
# %%
crashes = pd.read_csv("./data/crashes_2019_regions.csv")
# %%
region_crashes = crashes.groupby('REGION_ID')['CRASH_DATE'].count().sort_values()
crashes_fatal_incapacitating = crashes[(crashes['INJURIES_FATAL']>0) | (crashes['INJURIES_INCAPACITATING']>0)]
region_crashes_fatal_incapacitating = crashes_fatal_incapacitating.groupby('REGION_ID')['CRASH_RECORD_ID'].count().sort_values()
df = pd.concat([region_crashes,region_crashes_fatal_incapacitating], axis=1)
df = df.rename(columns={'CRASH_DATE': 'total_crashes', 'CRASH_RECORD_ID': 'total_fatal_incap'})
df['fraction'] = df['total_fatal_incap']/df['total_crashes']
# %%
df

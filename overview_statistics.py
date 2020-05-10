import pandas as pd
import numpy as np
import matplotlib as plt
import folium
from bokeh.palettes import Category20, Category20b, Turbo256
from bokeh.io import output_file, show, output_notebook
from bokeh.models import ColumnDataSource, FactorRange, Legend
from bokeh.plotting import figure
from bokeh.transform import dodge
import bokeh

# %%
crashes = pd.read_csv("./data/crashes_2019_regions.csv")
# %%
output_file("./html/days_barchart.html")

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
counts = crashes['CRASH_DAY_OF_WEEK'].value_counts().sort_index()

p = figure(x_range=weekdays, plot_height=450, title="Day of Week Crash Distribution",
           toolbar_location=None, tools="", y_axis_label='Number of Crashes', x_axis_label='Day of the Week')

p.vbar(x=weekdays, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000')

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)
# %%
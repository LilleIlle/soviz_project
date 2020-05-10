# %%
import pandas as pd
import numpy as np
import matplotlib as plt
import folium
from bokeh.palettes import Category20, Category20b, Turbo256
from bokeh.io import output_file, save, output_notebook
from bokeh.models import ColumnDataSource, FactorRange, Legend
from bokeh.plotting import figure
from bokeh.transform import dodge
import bokeh
# %%
crashes = pd.read_csv("./data/crashes_2019_regions.csv")
# %%
# DAYS PLOT
output_file("./web/bokeh/days_barchart.html")

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
counts = crashes['CRASH_DAY_OF_WEEK'].value_counts().sort_index()

p = figure(x_range=weekdays, plot_height=450,
           toolbar_location=None, tools="", y_axis_label='Number of Crashes', x_axis_label='Day of the Week')

p.vbar(x=weekdays, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000')

p.xgrid.grid_line_color = None
p.y_range.start = 0

save(p)
# %%
# MONTH PLOT
output_file("./web/bokeh/months_barchart.html")

x = ['January','February','March','April','May','June','July','August','September','October','November','December']
counts = crashes['CRASH_MONTH'].value_counts().sort_index()

p = figure(x_range=x, plot_height=450, plot_width=800, title="Monthly Crash Distribution",
           toolbar_location=None, tools="", y_axis_label='Number of Crashes', x_axis_label='Month')

p.vbar(x=x, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000')

p.xgrid.grid_line_color = None
p.y_range.start = 0

save(p)
# %%
# HOUR PLOT
output_file("./web/bokeh/hours_barchart.html")

x = np.sort(crashes['CRASH_HOUR'].unique()).tolist()
counts = crashes['CRASH_HOUR'].value_counts().sort_index()

p = figure(x_range=(0,23), plot_height=450, plot_width=800, title="Hourly Crash Distribution", toolbar_location=None, tools="", y_axis_label='Number of Crashes', x_axis_label='Hour')

p.vbar(x=x, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000')

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.ticker = list(range(0, 23))

save(p)
# %%
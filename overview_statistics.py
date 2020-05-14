# %%
import pandas as pd
import numpy as np
import matplotlib as plt
import folium
from bokeh.palettes import Category20, Category20b, Turbo256
from bokeh.io import output_file, show, save, output_notebook
from bokeh.models import ColumnDataSource, FactorRange, Legend
from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d
from bokeh.transform import dodge
import bokeh
# %%
crashes = pd.read_csv("./data/crashes_2019_regions.csv")
# %%
# DAYS PLOT
output_file("./web/bokeh/days_barchart.html")

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
counts = crashes['CRASH_DAY_OF_WEEK'].value_counts().sort_index()

TOOLTIPS = [
    #("Hour", "$index"),
    #("Day", "@x"),
    ("Number of crashes", "@top")
]

p = figure(x_range=weekdays,
           plot_height=450,
           toolbar_location=None,
           tools='',
           tooltips=TOOLTIPS,
           y_axis_label='Number of Crashes',
           x_axis_label='Day of the Week')

p.vbar(x=weekdays, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000')

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)
# %%
# MONTH PLOT
output_file("./web/bokeh/months_barchart.html")

x = ['January','February','March','April','May','June','July','August','September','October','November','December']
counts = crashes['CRASH_MONTH'].value_counts().sort_index()

TOOLTIPS = [
    #("Hour", "$index"),
    #("Day", "@x"),
    ("Number of crashes", "@top")
]

p = figure(x_range=x,
           plot_height=450,
           plot_width=800,
           title="Monthly Crash Distribution",
           toolbar_location=None,
           tools='',
           tooltips=TOOLTIPS,
           y_axis_label='Number of Crashes',
           x_axis_label='Month')

p.vbar(x=x, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000')

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)
# %%
# HOUR PLOT
output_file("./web/bokeh/hours_barchart.html")

hours = pd.DataFrame({'CRASH_HOUR': np.arange(0, 24)})

x = np.sort(crashes['CRASH_HOUR'].unique()).tolist()
counts = crashes['CRASH_HOUR'].value_counts().sort_index()

TOOLTIPS = [
    #("Hour", "$index"),
    #("Day", "@x"),
    ("Number of crashes", "@top")
]

p = figure(x_range=(-0.5,23.5),
           plot_height=450,
           plot_width=800,
           title="Hourly Crash Distribution",
           toolbar_location=None,
           tools='',
           tooltips=TOOLTIPS,
           y_axis_label='Number of Crashes',
           x_axis_label='Hour')

p.vbar(x=x, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000') #

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.ticker = list(range(0, 24))

show(p)

# %% HOUR PLOT
output_file("./web/bokeh/hours_barchart.html")

hours = pd.DataFrame({'CRASH_HOUR': np.arange(0, 24)})

x = np.sort(crashes['CRASH_HOUR'].unique()).tolist()
xx = x.copy()
xx.append(24)
counts = crashes['CRASH_HOUR'].value_counts().sort_index()

TOOLTIPS = [
    ("Crashes", "@top"),
]

p = figure(plot_height=450,
           plot_width=800,
           title="Hourly Crash Distribution",
           toolbar_location=None,
           tools='',
           tooltips=TOOLTIPS,
           y_axis_label='Number of Crashes',
           x_axis_label='Hour')

p.quad(top=counts, left=xx[:-1], right=xx[1:], width=0.5,
           fill_color='#000000', line_color='#000000', fill_alpha=0.25)

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.ticker = list(range(0, 24))

show(p)

# %% HOUR AND AVERAGE SPEED PLOT
congestion = pd.read_csv("./data/congestion_2019.csv")
output_file("./web/bokeh/hours_congestion_barchart.html")

congestion = congestion[congestion['SPEED']>0.0]
regions_congestion = congestion.groupby(['REGION_ID','HOUR'])['SPEED'].mean()
hour_congestion = congestion.groupby('HOUR')['SPEED'].mean()


hours = pd.DataFrame({'CRASH_HOUR': np.arange(0, 24)})

x = np.sort(crashes['CRASH_HOUR'].unique()).tolist()
xx = x.copy()
xx.append(24)
counts = crashes['CRASH_HOUR'].value_counts().sort_index()

#TOOLTIPS = [
#    ("Crashes", "@top"),
#]


p = figure(#x_range=(-0.5,23.5),
           plot_height=450,
           plot_width=800,
           title="Hourly Crash Distribution",
           toolbar_location=None,
           tools='',
           #tooltips=TOOLTIPS,
           y_axis_label='Number of Crashes',
           x_axis_label='Hour')

#p.yaxis.axis_line_color = "navy"
#p.vbar(x=x, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000')
p.quad(top=counts, left=xx[:-1], right=xx[1:], width=0.5,
           fill_color='#000000', line_color='#000000', fill_alpha=0.25)

p.extra_y_ranges = {'SPEED': Range1d(start=(hour_congestion.min()-0.25), end=(hour_congestion.max())+0.25)}
p.add_layout(LinearAxis(y_range_name='SPEED', axis_label="Average mph", axis_line_color='red'), 'right')

extra_value_y = pd.Series([hour_congestion[0]], index=[24])
hour_congestion = hour_congestion.append(extra_value_y)
p.line(xx, hour_congestion.array, line_width=1,y_range_name='SPEED',line_color="red")


p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.ticker = list(range(0, 24))

show(p)



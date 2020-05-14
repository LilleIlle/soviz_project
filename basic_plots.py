import pandas as pd
import numpy as np
from bokeh.palettes import Category20, Category20b, Turbo256
from bokeh.io import output_file, show, output_notebook
from bokeh.models import ColumnDataSource, FactorRange, Legend
from bokeh.plotting import figure
from bokeh.transform import dodge
import math
# %%
crashes = pd.read_csv("./data/crashes_2019_regions.csv")
# %%
# BASIC PRIMARY CAUSE PLOT
output_file("./web/bokeh/primary_cause_bar_chart.html")

crashes_primary = crashes[(crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'UNABLE TO DETERMINE')
                          & (crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'NOT APPLICABLE')]
cp = crashes[(crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'UNABLE TO DETERMINE')
                          & (crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'NOT APPLICABLE')].PRIM_CONTRIBUTORY_CAUSE.unique()
counts = None
counts = crashes_primary['PRIM_CONTRIBUTORY_CAUSE'].value_counts().sort_values()

TOOLTIPS = [
    ("Number of crashes", "@top")
]

p = figure(x_range=cp,
           plot_height=1050,
           plot_width=1050,
           toolbar_location=None,
           tools='',
           tooltips=TOOLTIPS,
           y_axis_label='Number of crashes')
           #y_axis_type="log")

p.vbar(x=cp, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000', bottom=0.01)
p.xgrid.grid_line_color = None
p.xaxis.major_label_orientation = 0.4 * math.pi/2
p.y_range.start = 0
show(p)
# %%
# BASIC PRIMARY CAUSE PLOT (LOG Y-AXIS)
output_file("./web/bokeh/primary_cause_bar_chart_log.html")

crashes_primary = crashes[(crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'UNABLE TO DETERMINE')
                          & (crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'NOT APPLICABLE')]
cp = crashes[(crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'UNABLE TO DETERMINE')
                          & (crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'NOT APPLICABLE')].PRIM_CONTRIBUTORY_CAUSE.unique()
counts = None
counts = crashes_primary['PRIM_CONTRIBUTORY_CAUSE'].value_counts().sort_values()

TOOLTIPS = [
    ("Number of crashes", "@top")
]

p = figure(x_range=cp,
           plot_height=1450,
           toolbar_location=None,
           tools='',
           tooltips=TOOLTIPS,
           y_axis_label='Number of crashes',
           y_axis_type="log")

p.vbar(x=cp, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000', bottom=0.01)
p.xgrid.grid_line_color = None
p.xaxis.major_label_orientation = math.pi/2
p.y_range.start = 10**(-2)
show(p)
# %%
# BASIC REGION CRASH BAR CHART
output_file("./web/bokeh/region_bar_chart.html")
crashes = crashes[crashes['REGION_ID']!=-1]
counts = None
counts = crashes.groupby('REGION_ID').size()

TOOLTIPS = [
    ("Number of crashes", "@top")
]

p = figure(x_range=counts.index.array,
           plot_height=500,
           toolbar_location=None,
           tools='',
           tooltips=TOOLTIPS,
           y_axis_label='Number of crashes',
           x_axis_label='Region ID')

p.vbar(x=counts.index.array, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000'), #bottom=0.01)
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.ticker = list(range(1, 30))
show(p)

# %%
# BASIC REGION AVG SPEED BAR CHART
output_file("./web/bokeh/region_avg_speed_bar_chart.html")

congestion = pd.read_csv("./data/congestion_2019.csv")
avg_speed = congestion.groupby('REGION_ID')['SPEED'].mean().sort_values()
#crashes = crashes[crashes['REGION_ID']!=-1]
counts = None
counts = avg_speed

TOOLTIPS = [
    ("Average mph", "@top")
]

p = figure(x_range=counts.index.array,
           plot_height=500,
           toolbar_location=None,
           tools='',
           tooltips=TOOLTIPS,
           y_axis_label='Average mph',
           x_axis_label='Region ID')

p.vbar(x=counts.index.array, top=counts, width=0.5, fill_alpha=0.25, fill_color='#000000', line_color='#000000'), #bottom=0.01)
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.ticker = list(range(1, 30))
show(p)
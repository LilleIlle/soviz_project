import pandas as pd
import numpy as np
from bokeh.palettes import Category20, Category20b, Turbo256
from bokeh.io import output_file, show, output_notebook
from bokeh.models import ColumnDataSource, FactorRange, Legend
from bokeh.plotting import figure
from bokeh.transform import dodge
# %%
crashes = pd.read_csv("./data/crashes_2019_regions.csv")
# %%
output_file("./web/bokeh/primary_cause.html")
# %%
# Filtering the primary causes 'UNABLE TO DETERMINE' and 'NOT APPLICABLE' as we deem this irrelevant for the purpose of the plot
crashes_primary = crashes[(crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'UNABLE TO DETERMINE')
                          & (crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'NOT APPLICABLE')]
# %%
# Filtering all primary causes that have 150 or less occurences in the 2019 data set.
cx = crashes_primary.groupby('PRIM_CONTRIBUTORY_CAUSE')
cx = cx.filter(lambda x: len(x) > 150)
cp = cx.PRIM_CONTRIBUTORY_CAUSE.unique() # crashes_primary.PRIM_CONTRIBUTORY_CAUSE.unique()

# %%
# Counting occurences across the day for each cause
causes_norm = pd.DataFrame({'CRASH_HOUR': np.arange(1, 25)})
for cause in cp:
    cause_hist = crashes_primary[crashes_primary['PRIM_CONTRIBUTORY_CAUSE'] == cause].groupby('CRASH_HOUR').size()
    # cause_hist_norm = (cause_hist / cause_hist.sum()) # distribution for a given cause seen only in context of the cause
    causes_norm[cause] = cause_hist
causes_norm.fillna(0)

# %%
source = causes_norm
# %%
p = figure(x_range=FactorRange(factors=causes_norm.CRASH_HOUR.astype(str)),
           y_axis_type="log",
           title="Crash primary causes throughout the day",
           x_axis_label='Hour of the day',
           y_axis_label='Number of crashes',
           plot_width=1700,
           plot_height=725,
           toolbar_location=None,
           sizing_mode='stretch_width')

# %%
bar = {}
colors = np.append(Category20[20], Category20b[20])
items = []

for indx, i in enumerate(cp):
    bar[i] = p.vbar(x=dodge('CRASH_HOUR', -.5, range=p.x_range), top=i, source=source, muted_alpha=0.01, muted=True,
                    width=.5, fill_color=colors[indx], bottom=0.01, alpha=0.6)
    items.append((i, [bar[i]]))

# %%
legend = Legend(items=items)
p.add_layout(legend, 'right')
p.legend.label_text_font_size = '8pt'
p.legend.click_policy = "mute"
p.y_range.start = 0
# %%
output_file("./html/primary_cause.html")

show(p)
# %%


# %%
#cx = crashes_primary.groupby('PRIM_CONTRIBUTORY_CAUSE')
#cx = cx.filter(lambda x: len(x) > 100)
#ss = cx.PRIM_CONTRIBUTORY_CAUSE.unique()

# xx = crashes_primary.groupby('PRIM_CONTRIBUTORY_CAUSE')['PRIM_CONTRIBUTORY_CAUSE'].filter(lambda x: len(x) >= 20)


#ux = cx.PRIM_CONTRIBUTORY_CAUSE.unique()

# w = crashes_primary.groupby('PRIM_CONTRIBUTORY_CAUSE').size().sort_values()

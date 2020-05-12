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
crashes_primary = crashes[crashes['PRIM_CONTRIBUTORY_CAUSE'] != 'UNABLE TO DETERMINE']
crashes_primary = crashes_primary[crashes_primary['PRIM_CONTRIBUTORY_CAUSE'] != 'NOT APPLICABLE']
cp = crashes_primary['PRIM_CONTRIBUTORY_CAUSE'].unique()

# %%

causes_norm = pd.DataFrame({'CRASH_HOUR': np.arange(1, 25)})
for cause in cp:
    cause_hist = crashes_primary[crashes_primary['PRIM_CONTRIBUTORY_CAUSE'] == cause].groupby('CRASH_HOUR').size()
    cause_hist_norm = cause_hist / cause_hist.sum()
    causes_norm[cause] = cause_hist_norm
causes_norm.fillna(0)

# %%
source = causes_norm
# %%
p = figure(x_range=FactorRange(factors=causes_norm.CRASH_HOUR.astype(str)),
           title="Crash primary causes throughout the day",
           x_axis_label='Hour of the day',
           y_axis_label='Relative frequency',
           plot_width=1700,
           plot_height=1000,
           toolbar_location=None,
           sizing_mode='stretch_width')
# %%
bar = {}
colors = np.append(Category20[20], Category20b[20])
items = []

for indx, i in enumerate(cp):
    bar[i] = p.vbar(x=dodge('CRASH_HOUR', -.5, range=p.x_range), top=i, source=source, muted_alpha=0.01, muted=True,
                    width=.5, fill_color=colors[indx])
    items.append((i, [bar[i]]))

# %%

legend = Legend(items=items)

p.add_layout(legend, 'right')
p.legend.label_text_font_size = '8pt'
p.legend.click_policy = "mute"
# %%
# output_file("./html/primary_cause.html")

show(p)

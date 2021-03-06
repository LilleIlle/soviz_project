# %%
import datetime
import math

import folium
import numpy as np
import pandas as pd
from IPython.display import Image, display, HTML
from bokeh.io import output_file, show
from bokeh.palettes import Category20, Category20b
from bokeh.plotting import figure

import folium
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import Image
from bokeh.io import output_file, show, output_notebook
from bokeh.models import FactorRange, Legend, LinearAxis, Range1d
from bokeh.palettes import Category20, Category20b, Reds
from bokeh.plotting import figure
from bokeh.transform import dodge
from folium import plugins
from folium.plugins import HeatMap
output_notebook()
# %% [markdown]
# # 1. Motivation
# In this project, we investigate the traffic of the City of Chicago as a case study of a busy urban environment.
# With its population of approximately 2.7 million it is the third-most-populous city in the United States.
# Daily life in Chicago thus entails millions of people participating in the city's traffic.
# We will have a main focus on temporal patterns of traffic in the project.
#
# Two data sets are used for this project:
# * [Traffic Crashes - Crashes](https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if)
# * [Chicago Traffic Tracker - Historical Congestion Estimates by Region - 2018-Current](https://data.cityofchicago.org/dataset/Chicago-Traffic-Tracker-Historical-Congestion-Esti/kf7e-cur8)
#
#
# In the following, these are referred to as the *Crashes* and *Congestion* data sets, respectively.
# Both sets are freely available via [Chicago Data Portal](https://data.cityofchicago.org).
#
# The Crashes data set contains location as well as a multitude of meta data on each police registered traffic crash within the City of Chicago limits and under the jurisdiction of Chicago Police Department.
#
# The Congestion data set contains information about the congestion of the streets.
# Congestion is estimated by probing GPS traces from the public transportation buses, yielding regional average speeds of
# buses with 10 minutes intervals. The congestion data set features a division of Chicago into 29 regions that covers the city (except O’Hare airport area).
# With comparable traffic patterns, a region is comprised of two or three community areas.
#
# The combination of theses two data sets allows for relating each crash to one of the 29 defined regions of the City of
# Chicago, as well as the estimated level of congestion at the time of the crash.
#
# Through careful analysis of the data, the goal is to elicit interesting findings about the traffic patterns of the City of Chicago and convey them in an intuitive manner
# to educate, non-scientific readers.

# %%
dev = False
if dev:
    lon = -87.6298
    lat = 41.8281
    CHI_map = folium.Map([lat, lon], tiles="Stamen Toner", zoom_start=10.5)
    CHI_map.save("../web/folium/chi_map.html")

display(HTML("<iframe src='https://chicago-traffic.netlify.app/folium/chi_map.html' height='750' width='1000'></iframe>"))


# %%

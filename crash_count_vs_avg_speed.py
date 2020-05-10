import numpy as np
from bokeh.plotting import figure, output_file, save


# TODO: Don't use hardcoded dicts
region_crashes_tally = {3: 5199, 15: 4024, 18: 7739, 19: 4021, 2: 4114, 8: 6159, 26: 3923, 6: 4895, 7: 4922, 20: 3413,
                        13: 5461, 22: 2267, 10: 6406, 5: 6591, 11: 6782, 4: 2940, 14: 4409, 16: 2847, 28: 1049, 9: 2873,
                        23: 4908, 12: 4140, 21: 3190, 24: 3625, 1: 2592, 17: 1288, 27: 1477, 25: 1832, 29: 2407,
                        -1: 801}

region_speed_means = {1: 20.577022889511255, 2: 26.68329213080924, 6: 22.633488102758474, 21: 23.674691823369628,
                      7: 21.460690040008423, 18: 25.10555749752574, 29: 19.161841900229525, 22: 27.68232664406494,
                      10: 23.731599250384285, 14: 24.040862286797218, 3: 23.235282065320387, 23: 24.224279517361918,
                      28: 20.995748278548717, 13: 18.773307222573173, 8: 20.809373144385255, 4: 20.18918570616353,
                      19: 26.006200593821728, 17: 24.532245198787063, 12: 19.132034112444728, 27: 28.521725241634904,
                      24: 24.968908799932617, 9: 22.66006338042998, 20: 25.892239044831435, 5: 22.866837583440375,
                      16: 24.206990186994606, 11: 22.74667487892188, 25: 25.541196908757822, 26: 28.672279475246896,
                      15: 25.74476016003369}

x = np.zeros(29)
for key, val in region_crashes_tally.items():
    if key == -1:
        break
    x[key - 1] = val

y = np.zeros(29)
for key, val in region_speed_means.items():
    y[key - 1] = val

TOOLTIPS = [
    ("Region ID", "$index"),
    ("Number of crashes", "@x"),
    ("Avg. speed (mph)", "@y{(0.0)}"),
]

# create a new plot with a title and axis labels
p = figure(
    title="Number of Crashes vs Avg. Speed for All 29 Regions",
    x_axis_label='Number of Crashes',
    y_axis_label='Avg. Speed',
    toolbar_location=None,
    tools='',
    tooltips=TOOLTIPS,
    sizing_mode='stretch_both',
)

p.circle(x, y, size=18, fill_color="black", fill_alpha=0.25, line_color="black")

# Output to static HTML file
output_file("./web/bokeh/crash_count_vs_avg_speed.html")
save(p)

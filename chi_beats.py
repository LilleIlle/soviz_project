# %%
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns

# %%
import urllib.request
import geojson
import gdal
import subprocess

# %%
sns.set(style="whitegrid", palette="pastel", color_codes=True)
sns.mpl.rc("figure", figsize=(10, 6))
%matplotlib inline


# %%
shp_path = "./data/shapefiles/chi_beats.shp"
chi_sf = shp.Reader(shp_path)

regions_shp_path = "./data/shapefiles/regions.shp"
regions_sf = shp.Reader(regions_shp_path)


# %%


def read_shapefile(sf):
    """
    Read a shapefile into a Pandas dataframe with a 'coords'
    column holding the geometry information. This uses the pyshp
    package
    """
    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df
# %%


def plot_shape(id, s=None):
    """ PLOTS A SINGLE SHAPE """
    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal')
    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points), 1))
    y_lat = np.zeros((len(shape_ex.points), 1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.plot(x_lon, y_lat)
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)
    # use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0], shape_ex.bbox[2])
    return x0, y0


# %%
def plot_map(sf, x_lim=None, y_lim=None, figsize=(11, 9)):
    '''
    Plot map with lim coordinates
    '''
    plt.figure(figsize=figsize)
    id = 0
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')

        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0, y0, id, fontsize=10)
        id = id+1

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)


# %%
def plot_map2(id, sf, x_lim=None, y_lim=None, figsize=(11, 9)):
    '''
    Plot map with lim coordinates
    '''

    plt.figure(figsize=figsize)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')

    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points), 1))
    y_lat = np.zeros((len(shape_ex.points), 1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.plot(x_lon, y_lat, 'r', linewidth=3)

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)

# %%


def plot_map_fill(id, sf, x_lim=None,
                  y_lim=None,
                  figsize=(11, 9),
                  color='r'):
    '''
    Plot map with lim coordinates
    '''

    plt.figure(figsize=figsize)
    fig, ax = plt.subplots(figsize=figsize)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')

    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points), 1))
    y_lat = np.zeros((len(shape_ex.points), 1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    ax.fill(x_lon, y_lat, color)

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)

# %%


def plot_map_fill_multiples_ids(title, beats, sf,
                                x_lim=None,
                                y_lim=None,
                                figsize=(11, 9),
                                color='r'):
    '''
    Plot map with lim coordinates
    '''

    plt.figure(figsize=figsize)
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(title, fontsize=16)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')

    for id in beats:
        shape_ex = sf.shape(id)
        x_lon = np.zeros((len(shape_ex.points), 1))
        y_lat = np.zeros((len(shape_ex.points), 1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        ax.fill(x_lon, y_lat, color)

        x0 = np.mean(x_lon)
        y0 = np.mean(y_lat)
        plt.text(x0, y0, id, fontsize=10)

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)

# %%
# plot_map_fill(0, chi_sf, x_lim=None, y_lim=None, color='g')


# # %%
# ids = [0, 1, 2, 3, 4, 5, 6]
# plot_map_fill_multiples_ids("Multiple Shapes",
#                             ids, chi_sf, color='r')

# %%


def plot_map_fill_multiples_ids_tone(sf, title, beats,
                                     print_id, color_ton,
                                     bins,
                                     x_lim=None,
                                     y_lim=None,
                                     figsize=(11, 9)):
    '''
    Plot map with lim coordinates
    '''

    plt.figure(figsize=figsize)
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(title, fontsize=16)

    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')

        for id in beats:
            shape_ex = sf.shape(id)
            x_lon = np.zeros((len(shape_ex.points), 1))
            y_lat = np.zeros((len(shape_ex.points), 1))
            for ip in range(len(shape_ex.points)):
                x_lon[ip] = shape_ex.points[ip][0]
                y_lat[ip] = shape_ex.points[ip][1]
            ax.fill(x_lon, y_lat, color_ton[beats._(id)])
            if print_id != False:
                x0 = np.mean(x_lon)
                y0 = np.mean(y_lat)
                plt.text(x0, y0, id, fontsize=10)
        if (x_lim != None) & (y_lim != None):
            plt.xlim(x_lim)
        plt.ylim(y_lim)
# %%


def calc_color(data, color=None):
    if color == 1:
        color_sq = ['#dadaebFF', '#bcbddcF0', '#9e9ac8F0',
                    '#807dbaF0', '#6a51a3F0', '#54278fF0']
        colors = 'Purples'
    elif color == 2:
        color_sq = ['#c7e9b4', '#7fcdbb', '#41b6c4',
                    '#1d91c0', '#225ea8', '#253494']
        colors = 'YlGnBu'
    elif color == 3:
        color_sq = ['#f7f7f7', '#d9d9d9', '#bdbdbd',
                    '#969696', '#636363', '#252525']
        colors = 'Greys'
    elif color == 9:
        color_sq = ['#ff0000', '#ff0000', '#ff0000',
                    '#ff0000', '#ff0000', '#ff0000']
    else:
        color_sq = ['#ffffd4', '#fee391', '#fec44f',
                    '#fe9929', '#d95f0e', '#993404']
        colors = 'YlOrBr'
    new_data, bins = pd.qcut(data, 6, retbins=True,
                             labels=list(range(6)))
    color_ton = []
    for val in new_data:
        color_ton.append(color_sq[val])
    if color != 9:
        colors = sns.color_palette(colors, n_colors=6)
        sns.palplot(colors, 0.6)
        for i in range(6):
            print("\n"+str(i+1)+': '+str(int(bins[i])) +
                  " => "+str(int(bins[i+1])-1), end=" ")
        print("\n\n   1   2   3   4   5   6")
    return color_ton, bins

# %%


def plot_comunas_data(sf, title, comunas, data=None,
                      color=None, print_id=False):
    '''
    Plot map with selected comunes, using specific color
    '''

    y_lim = (41.6, 42.05)  # latitude
    x_lim = (-87.95, -87.5)  # longitude

    color_ton, bins = calc_color(data, color)
    df = read_shapefile(sf)
    comuna_id = []
    for i in comunas:
        comuna_id.append(df.beat_num.astype(
            int)[df.beat_num.astype(int) == i]._[0])

    plot_map_fill_multiples_ids_tone(sf, title, comuna_id,
                                     print_id,
                                     color_ton,
                                     bins,
                                     x_lim=x_lim,
                                     y_lim=y_lim,
                                     figsize=(11, 9))


# %%
beats = crashes.groupby("BEAT_OF_OCCURRENCE").size().keys().to_numpy(dtype=int)
data = crashes.groupby("BEAT_OF_OCCURRENCE").size().values

print_id = True
color_palette = 1
plot_comunas_data(chi_sf, "Crashes",
                  beats[:15], data[:15], color_palette, print_id)

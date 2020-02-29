#!/usr/bin/env python3

import json, os, csv
from numpy import arange
from math import log
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

#TODO:
# --> Interpolation
#   Current implementation is unsatisfactory, based upon:
# https://stackoverflow.com/questions/5283649/plot-smooth-line-with-pyplot
#   Challenge: logarithmic scale. To check:
# https://stackoverflow.com/questions/3242382/interpolation-over-an-irregular-grid


def compress_median(sub_list):
    y_list = []
    for point in sub_list:
        y_list.append(point[1])
    y_list.sort()
    for point in sub_list:
        if point[1] == y_list[int((len(y_list)-1)/2)]:
            return point

def compress_max(sub_list):
    y_list = []
    for point in sub_list:
        y_list.append(point[1])
    y_list.sort()
    for point in sub_list:
        if point[1] == y_list[len(y_list)-1]:
            return point



config = {}
with open("config.json", "r") as f:
    config = json.load(f)

#print (config)

keys = []
for dtype in config["data"]:
    keys.append(dtype)

g_data = {} # global data array

for dtype in range(len(keys)): # for each data type
    g_data[keys[dtype]] = []

    for f in os.listdir(os.getcwd()): # for each file
        if keys[dtype] in f and ".csv" in f:
            with open(f, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for line in csv_reader:
                    if 0 < line_count:
                        row = [] # never use loop variable for anything else inside the same loop
                        row.append(float(line[0]))
                        row.append(float(line[1]))
                        g_data[keys[dtype]].append(row)
                    #print (line, row); exit()
                    line_count += 1


for key in keys: # sort data type list by the x values
    g_data[key].sort()

# print(g_data[keys[1]]) # debug only

if g_data[keys[0]] == []:
    print("No calibrational files found, please make sure they are in the same directory")
    quit()

for key in range(1, len(keys)): # calibrate
    for line in range(len(g_data[keys[key]])):
        g_data[keys[key]][line][1] = g_data[keys[key]][line][1] - g_data[keys[0]][line][1]

# print(keys)

if config["compressed"]:


    def bins_sort(dataset, sort_type, dtype): # try not to reuse global names within functions to avoid possible confusions
        bins = [] # new cycle, creating bins
        if config["x_limits_data"]:
            graph_range = int(log(config["x_max_data"], 10) - log(config["x_min_data"], 10)) # getting graph range
        else:
            graph_range = 8 # x-axis (logarithmic) - from 0 to 10^8
        if dtype == "tr_floor_": # adjusting graph range to match # bins according to data type
            cpd = config["count_per_decade_floor"]
            compress_floor_bool = True
        else:
            if sort_type == "normal":
                cpd = config["count_per_decade_median"]
            elif sort_type == "max":
                cpd = config["count_per_decade_max"]
            compress_floor_bool = False
        graph_range = graph_range*cpd
        
        for i in range(graph_range): # creating a bin per unit in range
            bins.append([])
        
        for point in dataset: # filling the bins up
            try:
                if point is None: # let's avoid execptions if possible! But how did that None happened in the first place?
                    continue      # exeptions is the last resort when you DON'T KNOW what's wrong
                                  # or the code that throws it is not yours to fix
                if config["x_limits_data"]:
                    index = int(cpd*(log(point[0], 10) - log(config["x_min_data"], 10)))
                else:
                    index = int(cpd*log(point[0], 10))
                if 0 <= index and len(bins) > index: # let's avoid execptions if possible!
                    bins[index].append(point)
            except (TypeError, IndexError):
                print("!!!", dtype, point); exit()
                pass # here we throw some data out without knowing what or why was that

        result = []
        for binn in bins:
            if compress_floor_bool:
                result.append(compress_max(binn))
            else:
                if sort_type == "normal":
                    result.append(compress_median(binn))
                elif sort_type == "max":
                    result.append(compress_max(binn))
        return result


    for dtype in range(1, len(keys)): # cycle through data types
        if keys[dtype] == "tr_floor_":
            result = bins_sort(g_data[keys[dtype]], "normal", keys[dtype])
        else:
            medium = bins_sort(g_data[keys[dtype]], "normal", keys[dtype])
            result = bins_sort(medium, "max", keys[dtype])
        
        g_data[keys[dtype]] = result

if config["inverted"]:
    for dtype in range(1, len(keys)):
        for line in range(len(g_data[keys[dtype]])):
            try:
                g_data[keys[dtype]][line][1] = -g_data[keys[dtype]][line][1]
            except TypeError:
                pass

fig = plt.figure(figsize=config["size"])
plot = fig.add_subplot()

for dtype in range(1, len(keys)):
    if config["data"][keys[dtype]]["show"]:
        x = []
        y = []
        for line in g_data[keys[dtype]]:
            try:
                x.append(line[0])
                y.append(line[1])
            except:
                pass
        if config["interpolation"]:
            xn = np.array(x)
            yn = np.array(y)
            xnew = np.linspace(xn.min(), xn.max(), 300) # 300 represents number of points to make between T.min and T.max
            spl = make_interp_spline(xn, yn, k=3)  # type: BSpline
            ynew = spl(xnew)
            plot.plot(xnew, ynew, config["data"][keys[dtype]]["color"], label=config["data"][keys[dtype]]["name"])
        else:
            plot.plot(x, y, config["data"][keys[dtype]]["color"], label=config["data"][keys[dtype]]["name"])

plot.set_xlabel(config["x_name"])
plot.set_ylabel(config["y_name"])
plt.title(config["title"])
if config["x_limits_graph"]:
    plt.xlim([config["x_min_graph"], config["x_max_graph"]])
if config["y_limits"]:
    plt.ylim([config["y_min"], config["y_max"]])
plt.xscale('log')
plt.minorticks_on()
plt.grid(True, which="major", color="grey")
plt.grid(True, which="minor", axis='both', color="gainsboro")
plt.legend(loc="lower right")
name = config["title"].replace(" ", "_")
plt.savefig(f'{name}.png')
plt.show()

#print(g_data[keys[1]])

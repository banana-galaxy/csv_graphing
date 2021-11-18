#!/usr/bin/env python3

import sys, os, json, csv
from math import log
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

# CREDITS
# Interpolation based upon: https://stackoverflow.com/questions/5283649/plot-smooth-line-with-pyplot
# Logarithmic scale: https://stackoverflow.com/questions/3242382/interpolation-over-an-irregular-grid


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

def bins_sort(dataset, dtype, config_file): # try not to reuse global names within functions to avoid possible confusions
    config = {}
    with open(config_file, "r") as f:
        config = json.load(f)

    bins = [] # new cycle, creating bins
    if config["x_limits_data"]:
        graph_range = int(log(config["x_max_data"], 10) - log(config["x_min_data"], 10)) # getting graph range
    else:
        graph_range = 8 # x-axis (logarithmic) - from 0 to 10^8
    if dtype == config['data']['floor']['file_name']: # adjusting graph range to match # bins according to data type
        cpd = config["count_per_decade_floor"]
        compress_floor_bool = True
    else:
        cpd = config["count_per_decade"]
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
            #result.append(compress_max(binn))
            result.append(compress_median(binn))
        else:
            result.append(compress_median(binn))
    return result


def main_plotter(config_file): # all data processing and plotting for one configuration file

    main_path = os.path.realpath(__file__)

    config = {}
    with open(config_file, "r") as f:
        config = json.load(f)

    keys = []
    for dtype in config["data"]:
        keys.append(dtype)

    g_data = {} # global data array

    cal_dir = os.path.join(os.path.split(main_path)[0], config['cal_dir'])
    g_data['cal'] = []
    for file in os.listdir(cal_dir):
        with open(os.path.join(cal_dir, file)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for line in csv_reader:
                if 0 < line_count:
                    g_data['cal'].append([float(line[0]), float(line[1])])
                line_count+=1
    
    all_dir = os.path.join(os.path.split(main_path)[0],  config['main_dir'])


    for dtype in keys:
        g_data[dtype] = []
        file_base_name = config['data'][dtype]['file_name']

        files = []
        for file in os.listdir(all_dir):
            if file_base_name in file: # FAILING
                files.append(file)

        for file in files:
            with open(os.path.join(all_dir, file)) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for line in csv_reader:
                    if 0 < line_count:
                        g_data[dtype].append([float(line[0]), float(line[1])])
                    line_count+=1


    for key in keys: # sort data type list by the x values
        g_data[key].sort()

    # print(g_data[keys[1]]) # debug only

    if g_data['cal'] == []:
        print("No calibrational files found, please make sure they are in the same directory")
        quit()

    for key in range(len(keys)): # calibrate
        for line in range(len(g_data[keys[key]])):
            g_data[keys[key]][line][1] = g_data[keys[key]][line][1] - g_data['cal'][line][1]

    # print(keys)


    if config["compressed"]:
        for dtype in range(len(keys)): # cycle through data types
            result = bins_sort(g_data[keys[dtype]], config['data'][keys[dtype]]['file_name'], config_file)
            g_data[keys[dtype]] = result

    if config["inverted"]:
        for dtype in range(len(keys)):
            for line in range(len(g_data[keys[dtype]])):
                try:
                    g_data[keys[dtype]][line][1] = -g_data[keys[dtype]][line][1]
                except TypeError:
                    pass

    fig = plt.figure(figsize=config["size"])
    plot = fig.add_subplot()

    for dtype in range(len(keys)):
        npi = int(config["size"][0] * 100 / 4) # number of points for interpolation ~~ less than 4 pixels per point
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
                logxn = np.log10(xn)
                logxnew = np.linspace(logxn.min(), logxn.max(), npi)
                xnew = np.power(10.0, logxnew)
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
    if config["interactive"]:
        plt.show()

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        main_plotter("config.json")
    else:
        for i in range(1, len(args)):
            main_plotter(args[i])
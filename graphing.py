#!/usr/bin/env python3
import json, os
from numpy import arange
from math import log
import matplotlib.pyplot as plt



def compress(sub_list):
    y_list = []
    for point in sub_list:
        y_list.append(point[1])
    y_list.sort()
    for point in sub_list:
        if point[1] == y_list[int((len(y_list)-1)/2)]:
            return point


def compress_floor(sub_list):
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

keys = []
for dtype in config["data"]:
    keys.append(dtype)

data = {}
for dtype in range(len(keys)): # for each data type
    data[keys[dtype]] = []

    for f in os.listdir(os.getcwd()): # for each file
        if keys[dtype] in f:
            with open(f, "r") as csv:
                csv = csv.read().split("\n")
                for line in range(1, len(csv)-1):
                    splitted = csv[line].split(",")
                    splitted.pop(2)
                    for num in range(len(splitted)):
                        splitted[num] = float(splitted[num])
                    data[keys[dtype]].append(splitted)

for key in keys: # sort data type list by the x values
    data[key].sort()

if data[keys[0]] == []:
    print("No calibrational files found, please make sure they are in the same directory")
    quit()

for key in range(1, len(keys)): # calibrate
    for line in range(len(data[keys[key]])):
        data[keys[key]][line][1] = data[keys[key]][line][1] - data[keys[0]][line][1]

for key in keys:
    print(key)

if config["compressed"]:

    for dtype in range(1, len(keys)): # cycle through data types
        bins = [] # new cycle, creating bins
        graph_range = log(config["x_max"], 10) - log(config["x_min"], 10) # getting graph range
        if keys[dtype] == "tr_floor_": # adjusting graph range to match # bins according to data type
            graph_range = graph_range*config["count_per_decade_floor"]
        else:
            graph_range = graph_range*config["count_per_decade"]
        
        for i in range(graph_range): # creating a bin per unit in range
            bins.append([])

        bins.append([]) # creating additional bin to compensate for #0
        
        for point in range(data[keys[dtype]]):
            #pass
            pass

if config["inverted"]:
    for dtype in range(1, len(keys)):
        for line in range(len(data[keys[dtype]])):
            data[keys[dtype]][line][1] = -data[keys[dtype]][line][1]

fig = plt.figure(figsize=(8,6))
plot = fig.add_subplot()

for dtype in range(1, len(keys)):
    x = []
    y = []
    for line in data[keys[dtype]]:
        x.append(line[0])
        y.append(line[1])
    plot.plot(x, y, config["data"][keys[dtype]]["color"], label=config["data"][keys[dtype]]["name"])

plot.set_xlabel(config["x_name"])
plot.set_ylabel(config["y_name"])
plt.title(config["title"])
if config["y_limits_status"]:
    plt.ylim([config["y_min"], config["y_max"]])
plt.xscale('log')
plt.grid(True, which="major", color="grey")
plt.grid(True, which="minor", color="gainsboro")
plt.legend(loc="lower right")
plt.show()

#print(data[keys[2]])
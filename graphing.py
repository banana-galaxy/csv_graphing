#!/usr/bin/env python3
import json, os, csv
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
            with open(f, 'r') as csv_file:
                #csv = csv.read().split("\n")
                #for line in range(1, len(csv)-1):
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for line in csv_reader:
                    #if line.endswith("\n\r"):
                    #    line.replace("\n\r", "")
                    #elif line.endswith("\n"):
                    #    line.replace("\n", "")
                    #splitted = csv[line].split(",")
                    #splitted = line.split(",")
                    #if len(splitted) == 3:
                    #    splitted.pop(2)
                    #try:
                    #    for num in range(len(splitted)):
                    #        splitted[num] = float(splitted[num])
                    #    data[keys[dtype]].append(splitted)
                    #except:
                    #    pass
                    if line_count == 0:
                        line_count += 1
                        continue
                    if len(line) == 3:
                        line.pop(2)
                    for num in range(len(line)):
                        line[num] = float(line[num])
                    data[keys[dtype]].append(line)
                    line_count += 1


for key in keys: # sort data type list by the x values
    data[key].sort()

if data[keys[0]] == []:
    print("No calibrational files found, please make sure they are in the same directory")
    quit()

for key in range(1, len(keys)): # calibrate
    for line in range(len(data[keys[key]])):
        data[keys[key]][line][1] = data[keys[key]][line][1] - data[keys[0]][line][1]

#for key in keys:
#    print(key)

if config["compressed"]:

    for dtype in range(1, len(keys)): # cycle through data types
        bins = [] # new cycle, creating bins
        graph_range = int(log(config["x_max"], 10) - log(config["x_min"], 10)) # getting graph range
        if keys[dtype] == "tr_floor_": # adjusting graph range to match # bins according to data type
            graph_range = graph_range*config["count_per_decade_floor"]
            cpd = config["count_per_decade_floor"]
            compress_floor_bool = True
        else:
            graph_range = graph_range*config["count_per_decade"]
            cpd = config["count_per_decade"]
            compress_floor_bool = False
        
        for i in range(graph_range): # creating a bin per unit in range
            bins.append([])

        bins.append([]) # creating additional bin to compensate for #0
        
        for point in data[keys[dtype]]: # filling the bins up
            index = int(cpd*(log(point[0], 10) - log(config["x_min"], 10)))
            if index <= 0:
                pass
            else:
                bins[index].append(point)

        result = [] 
        for binn in bins:
            if compress_floor_bool:
                result.append(compress_floor(binn))
            else:
                result.append(compress(binn))
        data[keys[dtype]] = result

if config["inverted"]:
    for dtype in range(1, len(keys)):
        for line in range(len(data[keys[dtype]])):
            try:
                data[keys[dtype]][line][1] = -data[keys[dtype]][line][1]
            except TypeError:
                pass

fig = plt.figure(figsize=(8,6))
plot = fig.add_subplot()

for dtype in range(1, len(keys)):
    if config["data"][keys[dtype]]["show"]:
        x = []
        y = []
        for line in data[keys[dtype]]:
            try:
                x.append(line[0])
                y.append(line[1])
            except:
                pass
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
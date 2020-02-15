import matplotlib.pyplot as plt
import sys

if len(sys.argv) == 1:
    print("Please enter a file to plot as an argument")
    quit()

color = []
title = input("Enter the graph title (leave blank for no title): ")
xmin = input("Enter x axis minimum (leave blank for no limits): ")
if xmin != "":
    xmax = input("Enter x axis maximum: ")
for csv in range(len(sys.argv)-1):
    color.append(input(f"Enter color for {sys.argv[csv+1]} (leave blank for default sky blue): "))
head_x = ""
head_y = ""
x = []
y = []
for csv in range(len(sys.argv)-1):
    with open(sys.argv[csv+1], "r") as f:
        x.append([])
        y.append([])
        for line in f:
            if line != ['']:
                line = line.split(",")
                if '"' in line[0]:
                    head_x = line[0].replace('"', '')
                    head_y = line[1].replace('"', '')
                else:
                    x[csv].append(float(line[0]))
                    y[csv].append(float(line[1]))

fig = plt.figure(figsize=(8,6))
plot = fig.add_subplot()

for count in range(len(sys.argv)-1):
    if color[count] != '':
        plot.plot(x[count], y[count], color[count])
    else:
        plot.plot(x[count], y[count])

plot.set_xlabel(head_x)
plot.set_ylabel(head_y)
plt.title(title)
if xmin != '':
    plt.xlim([int(xmin), int(xmax)])
plt.xscale('log')
plt.grid(True)
plt.show()
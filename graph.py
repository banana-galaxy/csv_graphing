from matplotlib import pyplot
import sys

if len(sys.argv) == 1:
    print("Please enter a file to plot as an argument")
    quit()

title = input("Enter the graph title (leave blank for no title): ")
xmin = input("Enter x axis minimum (leave blank for no limits): ")
if xmin != "":
    xmax = input("Enter x axis maximum: ")
head_x = ""
head_y = ""
x = []
y = []
with open(sys.argv[1], "r") as f:
    for line in f:
        if line != ['']:
            line = line.split(",")
            if '"' in line[0]:
                head_x = line[0].replace('"', '')
                head_y = line[1].replace('"', '')
            else:
                x.append(float(line[0]))
                y.append(float(line[1]))

fig = pyplot.figure(figsize=(8,6), dpi=100)
fig.suptitle(title)
plot = fig.add_subplot()
plot.plot(x,y)
plot.set_xlabel(head_x)
plot.set_ylabel(head_y)
#plot.title(title)
plot.grid()
pyplot.xscale('log')
'''pyplot.plot(x,y)
pyplot.xlabel(head_x)
pyplot.ylabel(head_y)
pyplot.title(title)
pyplot.grid()
pyplot.xscale('log')'''
if xmin != '':
    plot.set_xlim([int(xmin), int(xmax)])
pyplot.show()
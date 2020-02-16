try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Please install matplotlib\npip3 install matplotlib")
    quit()
import sys

if len(sys.argv) == 1:
    print("Please enter a file to plot as an argument")
    quit()


# --- defining variables ---
colors = {"floor":"silver", "symm":"dodgerblue", "diff":"darkorange", "asym":"forestgreen"}
title = "Power Filter 1A"
xmin, xmax = 1000, 100000000


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

for f in range(len(sys.argv)-1):
    for sort in colors:
        if sort in sys.argv[f+1]:
            plot.plot(x[f], y[f], colors[sort])

plot.set_xlabel(head_x)
plot.set_ylabel(head_y)
plt.title(title)
plt.xlim([xmin, xmax])
plt.xscale('log')
plt.grid(True)
plt.show()
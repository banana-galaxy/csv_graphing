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
colors = ["silver", "dodgerblue", "darkorange", "forestgreen"]
labels = ["floor", "symmetrical", "differential", "asymmetrical"]
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

for count in range(len(sys.argv)-1):
    plot.plot(x[count], y[count], colors[count], label=labels[count])

plot.set_xlabel(head_x)
plot.set_ylabel(head_y)
plt.title(title)
plt.xlim([xmin, xmax])
plt.xscale('log')
plt.grid(True, which="major", color="grey")
plt.grid(True, which="minor", color="gainsboro")
plt.legend(loc="lower right")
plt.show()
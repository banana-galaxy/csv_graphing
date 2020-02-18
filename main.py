import sys, os
from matplotlib import pyplot as pyplot
from assemble import assemble
from callibrate import callibrate
from graph import graph

files = []
for f in os.listdir(os.getcwd()):
    files.append(f)

comm = []
diff = []
unsym = []
cal = []
floor = []
assembled = []
calibrated = []
files = {"cal":cal, "floor":floor, "comm":comm, "diff":diff, "unsym":unsym, "assembled":assembled, "calibrated":calibrated}
names = ["cal", "floor", "comm", "diff", "unsym"]
show = ["floor", "comm", "diff", "unsym"]

for f in os.listdir(os.getcwd()):
    for csv in files:
        if csv in f and f.endswith(".csv"):
            if not "assemble" in f:
                files[csv].append(f)

for f in names:
    args = ["program"]
    for csv in files[f]:
        args.append(csv)
    assemble(args)
    if os.path.exists(f"{f}_assembled.csv"):
        os.remove(f"{f}_assembled.csv")
    os.rename("output.csv", f"{f}_assembled.csv")
    files["assembled"].append(f"{f}_assembled.csv")

for f in range(1, len(files["assembled"])):
    parts = files["assembled"][f].split(".")
    csv = parts[0] + "_calibrated." + parts[1]
    if os.path.exists(csv):
        os.remove(csv)
    callibrate(["program", files["assembled"][0], files["assembled"][f]])
    parts = files["assembled"][f].split(".")
    csv = parts[0] + "_calibrated." + parts[1]
    files["calibrated"].append(csv)

output = ["program"]
for f in calibrated:
    output.append(f)
graph(output)
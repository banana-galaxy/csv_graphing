import sys, os
from matplotlib import pyplot as pyplot
from assemble import assemble
import assemble_compress
from callibrate import callibrate
from graph import graph

compress = True
if len(sys.argv) > 1:
    if sys.argv[1] == "full":
        compress = False

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
files = {"tr_cal_":cal, "tr_floor_":floor, "comm_":comm, "diff_":diff, "unsym_":unsym, "assembled":assembled, "calibrated":calibrated}
names = ["tr_cal_", "tr_floor_", "comm_", "diff_", "unsym_"]
show = ["floor", "comm", "diff", "unsym"]
file_additions = ["_assembled", "_calibrated", "_ready"]

for addition in file_additions:
    for f in os.listdir(os.getcwd()):
        if addition in f:
            os.remove(f)

for f in os.listdir(os.getcwd()):
    for csv in range(len(names)):
        if names[csv] in f and f.endswith(".csv"):
            files[names[csv]].append(f)

if not compress:
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
else:
    for f in files["tr_cal_"]:
        f = f.split("_")
        for name in range(1, len(names)):
            for csv in files[names[name]]:
                if f[len(f)-1] in csv:
                    callibrate(["program", "_".join(f), csv])
                    parts = csv.split(".")
                    csv = f"{parts[0]}_calibrated.{parts[1]}"
                    files["calibrated"].append(csv)
    
    assemble = []
    for name in range(len(names)-1):
        assemble.append([])

    for f in range(len(files["calibrated"])):
        for name in range(len(names)-1):
            if names[name+1] in files["calibrated"][f]:
                assemble[name].append(files["calibrated"][f])
        
    for sorting in range(len(assemble)):
        test_parts = assemble[sorting][0].split("_")
        floor = 0
        for part in test_parts:
            if "floor" == part:
                floor = 1
        assemble_compress.compress(floor, assemble[sorting])
        for name in show:
            for part in test_parts:
                if name == part:
                    if os.path.exists(f"{name}_ready.csv"):
                        os.remove(f"{name}_ready.csv")
                    os.rename("output.csv", f"{name}_ready.csv")
    
    output = ["program"]
    for name in show:
        output.append(f"{name}_ready.csv")
    graph(output)
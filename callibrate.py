import sys, os

def callibrate(args):
    # accounting for human factor
    if len(args) == 1:
        print("Please provide paths to the files as arguments")
        quit()

    files = []
    for f in range(2, len(args)):
        if not os.path.exists(args[f]):
            if "*" in args[f]:
                template = args[f].replace("*", "")
                found = False
                for csv in os.listdir(os.getcwd()):
                    if template in csv:
                        files.append(csv)
                        found = True
                if not found:
                    print(f"Could not find files based on {template}\nplease make sure the script and the files are in the same directory")
                    quit()
            else:
                print(f"Could not find {args[f]}")
                quit()
        else:
            files.append(args[f])

    calibre = []
    with open(args[1], "r") as f:
        content = f.read().split("\n")
        for line in content:
            calibre.append(line.split(","))

    calibrated = [calibre[0]]
    for f in files:
        with open(f, "r") as csv:
            content = csv.read().split("\n")
            for line in range(1, len(content)):
                try:
                    if content[line] != '' and calibre[line] != ['']:
                        content[line] = content[line].split(",")
                        content[line][1] = float(content[line][1]) - float(calibre[line][1])
                        calibrated.append(content[line])
                except IndexError:
                    pass

            f = f.split(".")
            with open(f"{f[0]}_calibrated.{f[1]}", "a") as output:
                for line in calibrated:
                    output.write(f"{line[0]},{line[1]}\n")

if __name__ == "__main__":
    callibrate(sys.argv)
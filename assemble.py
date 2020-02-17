import sys, os

# accounting for human factor
if len(sys.argv) == 1:
    print("Please provide paths to the files as arguments")
    quit()

files = []
for f in range(1, len(sys.argv)):
    if not os.path.exists(sys.argv[f]):
        if "*" in sys.argv[f]:
            template = sys.argv[f].replace("*", "")
            found = False
            for csv in os.listdir(os.getcwd()):
                if template in csv:
                    files.append(csv)
                    found = True
            if not found:
                print(f"Could not find files based on {template}\nplease make sure the script and the files are in the same directory")
                quit()
        else:
            print(f"Could not find {sys.argv[f]}")
            quit()
    else:
        files.append(sys.argv[f])

data = []

for f in files: # assembling all the data into one multi-dimensional list
    with open(f, "r") as csv:
        content = csv.read().split("\n")
        for line in range(len(content)):
            content[line] = content[line].split(",")
            if not '"' in content[line][0]:
                for instance in range(len(content[line])):
                    if content[line] != ['']:
                        content[line][instance] = float(content[line][instance])
            
        data.append(content)

head = data[0][0]
for f in data:
    if not f[0] == head:
        print("The files do not have the same headers")
        quit()

#deciding on the name of the output file
output = ""
if os.path.exists("output.csv"):
    count = 1
    while True:
        if os.path.exists(f"output{count}.csv"):
            count += 1
        else:
            output = f"output{count}.csv"
            break
else:
    output = "output.csv"

#writing the data to the output file
output_data = []
with open(output, "a") as f:
    f.write(f"{head[0]},{head[1]}\n")
    
    for csv in data:
        for line in csv:
            if line != ['']:
                if line != head:
                    output_data.append(line)
    
    output_data.sort()
    for line in output_data:
        f.write(f"{line[0]},{line[1]}\n")

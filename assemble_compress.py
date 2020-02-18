import sys, os
from numpy import arange

# defining variable

floor = 0



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
        content[0] = content[0].split(",")

        for line in range(1, len(content)):
            content[line] = content[line].split(",")
            for instance in range(len(content[line])):
                if content[line] != ['']:
                    content[line][instance] = float(content[line][instance])
            
        data.append(content)

head = data[0][0]
for f in data:
    if not f[0] == head:
        print("The files do not have the same headers")
        quit()


# sorting file data
sorting_data = []
for csv in data:
    for line in range(1, len(csv)):
        if csv[line] != ['']:
            sorting_data.append(csv[line])
sorting_data.sort()

output_data = []
if floor: # sorting floor
    for exponent in arange(3.1, 8.1, 0.1):

        # accumulating data into sub_list based on current exponent
        sub_list = []
        for line in sorting_data:
            if line[0] > 10**(exponent-0.1) and line[0] < 10**exponent:
                sub_list.append(line)

        # appending highest Y value to sub_list
        if len(sub_list) > 1:
            big = sub_list[0]
            for line in sub_list:
                if line[1] > big[1]:
                    big = line
            index = sub_list.index(big)
            output_data.append(sub_list[index])
else: # sorting non floor
    for exponent in arange(3.01, 8.01, 0.01):

        # accumulating data into sub_list based on current exponent
        sub_list = []
        for line in sorting_data:
            if line[0] > 10**(exponent-0.01) and line[0] < 10**exponent:
                sub_list.append(line)

        # appending median Y value to sub_list
        y_list = []
        for line in sub_list:
            y_list.append(line[1])
        y_list.sort()

        if len(y_list) > 1:
            if len(y_list)%2 > 0:
                y_index = int((len(y_list)+1)/2)
            else:
                y_index = int((len(y_list))/2)
            if len(y_list) > 0:
                for line in range(len(sub_list)):
                    if sub_list[line][1] == y_list[y_index]:
                        output_data.append(sub_list[line])



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
with open(output, "a") as f:
    f.write(f"{head[0]},{head[1]}\n")

    for line in output_data:
        f.write(f"{line[0]},{line[1]}\n")

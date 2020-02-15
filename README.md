# csv_graphing

you will need to install **matplotlib** for **graph.py** to work
> pip3 install matplotlib

## running

**main.py** assembles graph data from multiple files into one, you will need to provide the files as arguments, example:
> python3 main.py graph.csv another_graph.csv
the output file will be **output.csv**, if that already exists it will start numbering the new output files

**graph.py** makes a graph with lines plotted from given files, example:
> python3 graph.py output.csv output1.csv
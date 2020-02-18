# csv_graphing

you will need to install **matplotlib** for **graph.py** to work
> pip3 install matplotlib

## running

**main.py** does everything described below in the right order and displays a graph, just make sure *all* the files as well as *all* the scripts are *all* in the same directory

**assemble.py** assembles graph data from multiple files into one, you will need to provide the files as arguments, example:
> python3 assemble.py graph.csv another_graph.csv

the output file will be **output.csv**, if that already exists it will start numbering the new output files
**assemble_compress.py** does the same as **assemble.py** with the addition of compressing the graph data files and as a result, smoothing out the line on the graph

You can tell either of these scripts to look for files based on a template, for example if you want to concatenate all files that start with "Grf" the command will look like this:
> python3 assemble.py Grf*

note the star at the end of the template, that's to indicate we've entered a template and not a filename

**graph.py** makes a graph with lines plotted from given files, example:
> python3 graph.py output.csv output1.csv
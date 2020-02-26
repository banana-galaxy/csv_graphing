# csv_graphing

you will need to install **matplotlib** for **graph.py** to work
> pip3 install matplotlib

## running

**graphing.py** and **config.json** are now available to do all the work. You only need these two files along with all the data files in one directory, then change the config to your liking and run graphing.py :)

***

**main.py** does everything described below in the right order and displays a graph, just make sure *all* the files as well as *all* the scripts are *all* in the same directory. Then simply do:
> python3 main.py

note this will create a compressed/smoothed out graph, if you want to see the full data add in "full" as an argument:
> python3 main.py full

***

**assemble.py** assembles graph data from multiple files into one, you will need to provide the files as arguments, example:
> python3 assemble.py graph.csv another_graph.csv

the output file will be **output.csv**, if that already exists it will start numbering the new output files
**assemble_compress.py** does the same as **assemble.py** with the addition of compressing the graph data files and as a result, smoothing out the line on the graph

You can tell either of these scripts to look for files based on a template, for example if you want to concatenate all files that start with "Grf" the command will look like this:
> python3 assemble.py Grf*

note the star at the end of the template, that's to indicate we've entered a template and not a filename

**graph.py** makes a graph with lines plotted from given files, example:
> python3 graph.py output.csv output1.csv

## updates

02/18/2020: main.py now automatically compresses/smoothes out the graph, you can add "full" as an argument to show an uncompressed graph

02/26/2020: After quite some time of debugging graphing.py and config.json are now available and do all the work
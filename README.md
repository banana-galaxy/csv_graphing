# csv_graphing

The **graphing.py** Python script:
* Assembles multiple **CSV** files named `prefix_*.csv` with the same `prefix_`
* Applies calibration (read from `tr_cal_*.csv`, configurable) to all other datasets
* Reduces input data noise using median to produce a configurable number of points
* Beautifies resulting graphs by BSpline interpolation
* Produces Bode (logarithmic) plots where size, names, colors, and limits are all configurable

The code has been written for processing of Power EMI Filter Insertion Loss measurements as per CISPR 17. Results can be seen at [775mv.com](https://775mv.com/product-category/emi-filters/)

## Installation

### clone repository
`git clone git@github.com:banana-galaxy/csv_graphing.git`
### enter folder
`cd csv_graphing`
### create a virtual environment (venv)
`python3 -m venv ./`
### activate venv
linux: `source ./bin/activate`\
windows: `source ./venv/Scripts/activate` or `source ./venv/bin/activate`
### install libraries (matplotlib and scipy)
`pip3 install -r requirements.txt`

## Usage

### activate your venv if you haven't already
linux: `source ./bin/activate`\
windows: `source ./venv/Scripts/activate` or `source ./venv/bin/activate`\
Please note you need to be in the "csv_graphing" directory to activate the venv.

### assemble different frequency files into a single one for each type of measurement
example: `python3 assemble.py floor_low_freq.csv floor_medium_freq.csv floor_high_freq.csv`

The assemble.py file will produce an `output.csv` file, make sure to rename it. If there already is an `output.csv` file it will create an `output1.csv`, then `output2.csv` and so on.\
There can be as much files of different frequencies as you want.

### creating the graph
Once you have all the files of the different types of measurements you want you can create a graph.\
We create a graph with `graphing.py`.\
`graphing.py` creates graphs based on a configuration file. The configuration file contains the following information:\
- The name of the graph
- The size of the graph
- x and y axis labels
- Limitation on what range of data to read if needed
- What x and y limits to use if any
- Different settings for computing and displaying the data
- The file prefixes to look for, for each measurement type. Along with how to display them on the graph.
- Whether or not you want the graph to be "interactive"

`config.json` is a sample configuration file you can use as a template. By default `graphing.py` uses `config.json` as its configuration file, if you want to use something else, specify the name of the file as a command line parameter. For example:\
`python3 graphing.py my_config.json`

Several configuration files can be given as command line parameters and will be processed one by one resulting in different graphs based on the information in them. Example:
`./graphing.py my_config.json config_fan_filter.json config_30a_filter.json`\
This will produce three (3) graphs, each based on the info from one of the config files. `graphing.py` reads the config files and makes graphs for them in the order they are given as command line parameters.

All input files need to reside in the directory of the python file being run.

Once you are done you can type `deactivate` to deactivate the venv.
***

## Updates

2020-02-29: First Release
2021-11-14: Update README
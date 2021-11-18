# csv_graphing

The **graphing.py** Python script:
* Gathers data from as many files as are provided
* Applies calibration data to all datasets
* Reduces input data noise using median to produce a configurable number of points
* Beautifies resulting graphs by BSpline interpolation
* Produces Bode (logarithmic) plots where size, names, colors, and limits are all configurable

The code has been written for processing of Power EMI Filter Insertion Loss measurements as per CISPR 17. Results can be seen at [775mv.com](https://775mv.com/product-category/emi-filters/)

## Installation

### clone repository
`git clone git@github.com:banana-galaxy/csv_graphing.git`
### enter folder
`cd csv_graphing`
### create a virtual environment (venv) - you can skip this along with the next step if you don't know about venvs
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

### creating the graph
`graphing.py` creates graphs based on a configuration file. The configuration file contains the following information:\
- The name of the graph
- The size of the graph
- x and y axis labels
- Limitation on what range of data to read if needed
- What x and y limits to use if any
- Different settings for computing and displaying the data
- The directories to look for that contain the calibration files, and the rest
- The file prefixes to look for, for each measurement type. Along with how to display them on the graph.
- Whether or not you want to have a graph window to tinker with.

`graphing.py` looks for a folder with files containing calibration data and a separate folder containing all the other data to create its graph, the names it looks for are defined in the configuration file.

`config.json` is a sample configuration file you can use as a template. By default `graphing.py` uses `config.json` as its configuration file, if you want to use something else, specify the name of the file as a command line parameter. For example:\
`python3 graphing.py my_config.json`

Several configuration files can be given as command line parameters and will be processed one by one resulting in different graphs based on the information in them. Example:
`./graphing.py my_config.json config_fan_filter.json config_30a_filter.json`\
This will produce three (3) graphs, each based on the info from one of the config files. `graphing.py` reads the config files and makes graphs for them in the order they are given as command line parameters.

All input files need to reside in the directory of the python file being run.

Once you are done you can type `deactivate` to deactivate the venv.
***

## Updates

2020-02-29: First Release\
2021-11-14: Update README\
2021-11-17: Combined the two "graphing" and "assemble" scripts, changed the config for easier usage, updated README
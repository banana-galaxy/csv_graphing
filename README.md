# csv_graphing

The **graphing.py** Python script:
* Assembles multiple **CSV** files named `prefix_*.csv` with the same `prefix_`
* Applies calibration (read from `tr_cal_*.csv`, configurable) to all other datasets
* Reduces input data noise using median to produce a configurable number of points
* Beautifies resulting graphs by BSpline interpolation
* Produces Bode (logarithmic) plots where size, names, colors, and limits are all configurable

The code has been written for processing of Power EMI Filter Insertion Loss measurements as per CISPR 17. Results can be seen at [775mv.com](https://775mv.com/product-category/emi-filters/)

## Prerequisites

**Python 3**
>`python3 --version`
* last tested with Python version 3.6.9

**matplotlib**
>`pip3 install matplotlib`

## Usage

**graphing.py** called without command line parameters will use **config.json**.

A number of configuration files can be given as command line parameters and will be processed one by one. Example:
>`./graphing.py config.json s21.json s21-raw.json`
 
 All input files need to reside in the local directory.

## Updates

2020-02-29: First Release

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 11:46:58 2018

@author: deborahkhider

Opening GRIB files with Python and setting the variable long names
"""

import pygrib

file = "/Volumes/Data HD/Documents/MINT/Climate/netCDFTutorial/test.grib"

# Open the file
grbs = pygrib.open(file)
grb = grbs.select(name='Total precipitation')[0]
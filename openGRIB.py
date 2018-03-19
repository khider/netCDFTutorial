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

#User input
keys = ['Total precipitation'] #lat/lon/time are given with each parameter. No need to loop over them

#Iterate over and store values
def getGribVar(grib_file, keys):
    ''' Extract variables from a GRIB file.
    
    This function gets the variable contained in a GRIB file 
    and return them into Python nested dictionaries. The first
    dictionary's key contains the longname, while the
    second dictionary contains values, the standard CF name,
    units and the missing data flag.
    
    Args:
        grib_file (str): A name (path) of a GRIB file
        keys (list): A list of keys to fetch the variables according
            to the CF standard
    
    Returns:
        dict_out (dict): A dictionary containing the standard names as keys and
            the associated data as values.
    '''
    import pygrib    
    
    grbs = pygrib.open(grib_file)
    
    dict_out={}
    for key in keys:
        vars_values = []
        vars_time = []
        for grb in grbs:
            # Grab the various metadata
            if grb.parameterName == key:
                vars_time.append(grb.validDate)
                vars_values.append((grb.values*grb.scaleValuesBy)+grb.offsetValuesBy)
        # Pack into the dictionary
        if 'latitude' not in dict_out.keys():
            lats,longs = grb.latlons()
            lats = lats[:,0]
            longs = longs[0,:]
            dict_out['latitude']={'values':lats}
            dict_out['longitude']={'values':longs}
            dict_out['time']={'values':vars_time}
        dict_out[key] = {'values':vars_values, 'units':grb.parameterUnits,'missing_values':grb.missingValue, 'standard_name':grb.cfName}    
        
        return dict_out

#Exanple

dict_out =  getGribVar(file,keys)           
            
            
        
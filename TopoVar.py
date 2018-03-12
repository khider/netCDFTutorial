#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 16:01:09 2018

@author: deborahkhider

Open and manipulate a netCDF file that contains all the needed variables for
initializing TOPOFLOW

"""

from netCDF4 import Dataset 
import numpy as np

file = "/Volumes/Data HD/Documents/MINT/Climate/netCDFTutorial/Example.nc"

nc_fid = Dataset(file)
nc_vars = [var for var in nc_fid.variables]

# Get the needed keys
keys=[]
for vars in nc_vars:
    keys.append(nc_fid.variables[vars].getncattr('long_name'))
    
#Get a dictionary that contains all the extraacted variables
def getNcVar(nc_file, keys):
    ''' Extract variables from a netCDF file.
    
    This function gets the variable contained in a netCDF file 
    and return them into Python nested dictionaries. The first
    dictionary's key contains the CF longname, while the
    second dictionary contains values, units and the missing data flag.
    
    Args:
        nc_file (str): A name (path) of a netCDF file
        keys (list): A list of keys to fetch the variables according
            to the CF standard
    
    Returns:
        dict_out (dict): A dictionary containing the standard names as keys and
            the associated data as values.
    '''
    from netCDF4 import Dataset
    #Open the netCDF file
    nc_fid = Dataset(nc_file)
    # Get the variable names
    nc_vars = [var for var in nc_fid.variables]
    # Get the longnames for each variables
    nc_vars_longname = []
    nc_vars_units =[]
    #Add corrections if needed
    nc_vars_scale_factor=[]
    nc_vars_add_offset=[]
    # Check the missing value tags
    nc_vars_missing_value=[]
    
    for vars in nc_vars:
        if 'long_name' in nc_fid.variables[vars].ncattrs():
            nc_vars_longname.append(nc_fid.variables[vars].getncattr('long_name'))
        else:
            nc_vars_longname.append(vars)
        if 'units' in nc_fid.variables[vars].ncattrs():
            nc_vars_units.append(nc_fid.variables[vars].getncattr('units'))
        else:
            nc_vars_units.append('NA')
        if 'scale_factor' in nc_fid.variables[vars].ncattrs():
            nc_vars_scale_factor.append(nc_fid.variables[vars].getncattr('scale_factor'))
        else:
            nc_vars_scale_factor.append(1)
        if 'add_offset' in nc_fid.variables[vars].ncattrs():
            nc_vars_add_offset.append(nc_fid.variables[vars].getncattr('add_offset'))
        else:
            nc_vars_add_offset.append(0) 
        if 'missing_value' in nc_fid.variables[vars].ncattrs(): 
            nc_vars_missing_value.append(nc_fid.variables[vars].getncattr('missing_value'))
        else:
            nc_vars_missing_value.append('NA')
    # Check for the list against the desired variables and output.
    dict_out ={}
    for name in nc_vars_longname:
        if name in keys:
            f = {'values':[],'units':[],'missing_value':[]}
            idx = nc_vars_longname.index(name)
            f['values']=(nc_fid.variables[nc_vars[idx]][:]*nc_vars_scale_factor[idx])\
                +nc_vars_add_offset[idx]
            f['units']=nc_vars_units[idx]
            f['missing_value'] = nc_vars_missing_value[idx]
            dict_out[name] = f
               
    return dict_out

dict_out =  getNcVar(file,keys)   

# Data manipulation
# 1. Relative humidity calculation
TD = np.array(dict_out['2 metre dewpoint temperature']['values'])
T = np.array(dict_out['2 metre temperature']['values'])
RH = 100*(np.exp((17.625*TD)/(243.04+TD))/np.exp((17.625*T)/(243.04+T)))

# put in dict_out
dict_out['relative humidity']={'values':RH,'units':'NA'} 

#2. wind speed
U = np.array(dict_out['10 metre U wind component']['values'])
V = np.array(dict_out['10 metre V wind component']['values'])

W = np.sqrt(U**2+V**2)

dict_out['wind speed']={'values':W,'units':dict_out['10 metre V wind component']['units']} 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 11:50:29 2018

@author: deborahkhider

Opening a dataset contained in multiple netCDF files
"""

from netCDF4 import MFDataset
# Just get a list of netCDF files. 
root = "/Volumes/Data HD/Documents/MINT/Climate/netCDFTutorial"
files = ["Oct2010.nc","Nov2010.nc","Dec2010.nc"]

file_names =[]
for name in files:
    file_names.append(root+"/"+name)
    
#Open the file and get the keys for this example
nc_fid = MFDataset(file_names)
# Get the variables
nc_vars = [var for var in nc_fid.variables]
# Get the keys
keys = []    
for vars in nc_vars:
    keys.append(nc_fid.variables[vars].getncattr('long_name'))
 
# Import the package
from netCDF4 import MFDataset
# Open the netCDF files
nc_fid = MFDataset(file_names)
# Get the variable names
nc_vars = [var for var in nc_fid.variables]

#Make empty lists to collect the info
#longname (should be using the CF conventions)
nc_vars_longname=[]
#Units
nc_vars_units=[]
#Corrections
nc_vars_scale_factor=[]
nc_vars_add_offset=[]
#Missing values
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

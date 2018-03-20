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
keys=[]
nc_vars = [var for var in nc_fid.variables]
for vars in nc_vars:
    keys.append(getattr(nc_fid.variables[vars],'long_name'))

# First let's print out the file
def MFncdump(nc_fid):
    """
    MFncdump prints dimensions, variables and their attribute info
    
    Args:
        nc_fid: a netCDF file    
    """
        
    # Global attributes
    print("NetCDF Global Attributes: ")
    for name in nc_fid.ncattrs():
        print('\t'+name+": "+getattr(nc_fid,name))

    #Dimension shape information
    print("NetCDF dimension information: ")
    nc_dims = [dim for dim in nc_fid.dimensions]
    for dim in nc_dims:
        print('\t'+dim+': ')
        for attrname in nc_fid.variables[dim].ncattrs():
            print('\t\t'+attrname+": "+getattr(nc_fid.variables[dim], attrname))
    #Variables information
    print("NetCDF variables information: ")
    for name, variable in nc_fid.variables.items():
        print('\t'+name+': ')
        for attrname in variable.ncattrs():
            print('\t\t'+attrname+': '+str(getattr(variable,attrname)))
 
def getMFNcVar(nc_files, keys):
    ''' Extract variables from a dataset across multiple netCDF files.
    
    This function gets the variable contained in a netCDF file 
    and return them into Python nested dictionaries. The first
    dictionary's key contains the longname, while the
    second dictionary contains values, standard name (CF),
    units and the missing data flag.
    
    Args:
        nc_file (str): A name (path) of a netCDF file
        keys (list): A list of keys to fetch the variables according
            to the CF standard
    
    Returns:
        dict_out (dict): A dictionary containing the standard names as keys and
            the associated data as values.
    '''
    # Import the package
    from netCDF4 import MFDataset
    # Open the netCDF files
    nc_fid = MFDataset(nc_files)
    # Get the variable names
    nc_vars = [var for var in nc_fid.variables]
    
    #Make empty lists to collect the info
    #longname (should be using the CF conventions)
    nc_vars_longname=[]
    #Units
    nc_vars_units=[]
    # Get the standard name
    nc_vars_standardname=[]
    #Corrections
    nc_vars_scale_factor=[]
    nc_vars_add_offset=[]
    #Missing values
    nc_vars_missing_value=[]
    
    for vars in nc_vars:
        if 'long_name' in nc_fid.variables[vars].ncattrs():
            nc_vars_longname.append(getattr(nc_fid.variables[vars],'long_name'))
        else:
            nc_vars_longname.append(vars)
        if 'units' in nc_fid.variables[vars].ncattrs():
            nc_vars_units.append(getattr(nc_fid.variables[vars],'units'))
        else:
            nc_vars_units.append('NA')
        if 'standard_name' in nc_fid.variables[vars].ncattrs():
            nc_vars_standardname.append(getattr(nc_fid.variables[vars],'standard_name'))
        else:
            nc_vars_standardname.append("NA")    
        if 'scale_factor' in nc_fid.variables[vars].ncattrs():
            nc_vars_scale_factor.append(getattr(nc_fid.variables[vars],'scale_factor'))
        else:
            nc_vars_scale_factor.append(1)
        if 'add_offset' in nc_fid.variables[vars].ncattrs():
            nc_vars_add_offset.append(getattr(nc_fid.variables[vars],'add_offset'))
        else:
            nc_vars_add_offset.append(0) 
        if 'missing_value' in nc_fid.variables[vars].ncattrs(): 
            nc_vars_missing_value.append(getattr(nc_fid.variables[vars],'missing_value'))
        else:
            nc_vars_missing_value.append('NA')
    # Check for the list against the desired variables and output.
    dict_out ={}
    for name in nc_vars_longname:
        if name in keys:
            f = {'values':[],'units':[],'missing_value':[], 'standard_name':{}}
            idx = nc_vars_longname.index(name)
            f['values']=(nc_fid.variables[nc_vars[idx]][:]*nc_vars_scale_factor[idx])\
                +nc_vars_add_offset[idx]
            f['units']=nc_vars_units[idx]
            f['missing_value'] = nc_vars_missing_value[idx]
            f['standard_name'] = nc_vars_standardname[idx]
            dict_out[name] = f
    
    return dict_out            

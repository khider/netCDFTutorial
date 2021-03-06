#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 13:58:13 2018

@author: deborahkhider
"""

from netCDF4 import Dataset  

# Open the example netCDF file
dataset = Dataset("/Volumes/Data HD/Documents/MINT/Climate/netCDFTutorial/test.nc")

# Get the dataset format (not necessary)
print(dataset.file_format)

# Get the name of the dimensions, attributes and variables
def ncdump(nc_fid, verb=True):
    '''
    ncdump outputs dimensions, variables and their attribute information.
    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    verb : Boolean
        whether or not nc_attrs, nc_dims, and nc_vars are printed

    Returns
    -------
    nc_attrs : list
        A Python list of the NetCDF file global attributes
    nc_dims : list
        A Python list of the NetCDF file dimensions
    nc_vars : list
        A Python list of the NetCDF file variables
    '''
    def print_ncattr(key):
        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print("\t\ttype:", repr(nc_fid.variables[key].dtype))
            for ncattr in nc_fid.variables[key].ncattrs():
                print('\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr)))
        except KeyError:
            print("\t\tWARNING: %s does not contain variable attributes" % key)

    # NetCDF global attributes
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print("NetCDF Global Attributes:")
        for nc_attr in nc_attrs:
            print('\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr)))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
    # Dimension shape information.
    if verb:
        print("NetCDF dimension information:")
        for dim in nc_dims:
            print("\tName:", dim) 
            print("\t\tsize:", len(nc_fid.dimensions[dim]))
            print_ncattr(dim)
    # Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print("NetCDF variable information:")
        for var in nc_vars:
            if var not in nc_dims:
                print('\tName:', var)
                print("\t\tdimensions:", nc_fid.variables[var].dimensions)
                print("\t\tsize:", nc_fid.variables[var].size)
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars

dataset_attrs, dataset_dims, dataset_vars = ncdump(dataset, verb=True)

# Import the variables
# Write a functions that loads the variable without looking at them

#Fisrt assume that the user (and then the system) will enter (1) the
# file name (.nc) and the variables of interest which would be 
# mapped to GSN and therefore CF standard.
nc_file = "/Volumes/Data HD/Documents/MINT/Climate/netCDFTutorial/test.nc"
keys = ['latitude','longitude','time','Total precipitation'] 

# Get the necessary information about the netCDF file (i.e. assume that
# the function above is not being run on a regular basis.)

def getNcVar(nc_file, keys):
    ''' Extract variables from a netCDF file.
    
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
    from netCDF4 import Dataset
    #Open the netCDF file
    nc_fid = Dataset(nc_file)
    # Get the variable names
    nc_vars = [var for var in nc_fid.variables]
    # Get the longnames for each variables
    nc_vars_longname = []
    #Get the units
    nc_vars_units =[]
    # Get the standard name
    nc_vars_standardname=[]
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
        if 'standard_name' in nc_fid.variables[vars].ncattrs():
            nc_vars_standardname.append(nc_fid.variables[vars].getncattr('standard_name'))
        else:
            nc_vars_standardname.append('NA')    
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
            f = {'values':[],'units':[],'missing_value':[],'standard_name':{}}
            idx = nc_vars_longname.index(name)
            f['values']=(nc_fid.variables[nc_vars[idx]][:]*nc_vars_scale_factor[idx])\
                +nc_vars_add_offset[idx]
            f['units']=nc_vars_units[idx]
            f['missing_value'] = nc_vars_missing_value[idx]
            f['standard_name'] = nc_vars_standardname[idx]
            dict_out[name] = f
               
    return dict_out

#Run the example
dict_out = getNcVar(nc_file, keys) 
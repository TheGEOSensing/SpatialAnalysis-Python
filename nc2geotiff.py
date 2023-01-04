#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 15:11:01 2022

@author: student
"""

import rioxarray as rio
import xarray
import glob
import shutil
import os
    

####---------- read the .nc files in the source directiory ----------------####

source = '/Users/student/Desktop/Datasets/Sea Ice Motion Vectors NSIDC/'
files = glob.glob(source + '*.nc')
files_sorted = sorted(files)

for file in files_sorted:
    ncfile = xarray.open_dataset(file)   ## open all the files in a loop
    u = ncfile['u']                      ## reading the target data file from a netcdf 
    u = u.rio.set_spatial_dims('x', 'y') ## putting lat long to the spatial dimension
    u.rio.write_crs("epsg:3031")         ## specifying the projection system
    u.rio.to_raster(file[:-2] + '.tif')  ## remove the name .nc and produce .tif
    
####---------- Create a Directory for the destination .tif files ----------------####

destination = "/Users/student/Desktop/Datasets/Sea Ice Motion Vectors NSIDC/geotiffs"
try:
    os.mkdir(destination)
except OSError:
    print ("Creation of the directory %s failed" % destination)
else:
    print ("Successfully created the directory %s " % destination)
    
#### save the .tiff files in the destination folder 
geotiffs = glob.glob(source + '*.tif')
for geotiff in geotiffs:
    shutil.move(geotiff,destination)
    
###### ------------------------------------------------------------ ####  

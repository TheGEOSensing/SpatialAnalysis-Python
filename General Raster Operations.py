from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

#1 Open a dataset and collect the information
ds = gdal.Open("srtm_52_06.tif")
geot = ds.GetGeoTransform()         ## get geotransform
proj = ds.GetProjection()           ## get projection information


nob = ds.RasterCount()              ## number of bands
band1 = ds.GetRaster(1)             ## read the band which is needed - 1/2/3
array = band1.ReadAsArray()         ## read the band as array

plt.figure()
plt.imshow(array)                   ## plotting the image

#2 create a condition for DEM> mean(height) or DEM>4000m 
mask_mean = np.where((array >= np.mean(array)),1,0)  
mask_4000 = np.where((array >= 4000),1,0)           ## if DEM>(height) = 1 otherwise 0
height_4000 = (mask_4000 * array)                   ## height>4000 = mask* DEM_array

plt.figure()
plt.imshow(height_4000)                             ## plotting the image

#3 Set up GDAL output parameters and save the band informations

driver = gdal.GetDriverByName("GTiff")              ## call the driver geotiff
driver.Register()                                   ## register the driver
output = driver.Create("GTiff",                     ## type of the image
                      xsize = height_4000.shape[1], ## size of the x 
                      ysize = height_4000.shape[0], ## size of the y 
                      bands = 1,                    ## number of bands
                      eType = gdal.GDT_Int16)       ## type of data
output.SetGeoTransform(geot)                        ## provide same geotransform information
output.SetProjection(proj)                          ## provide same projection information
outband = output.GetRasterBand(1)                   ## write the dataset bands
outband.WriteArray(height_4000)                     ## write the dataset as array
outband.SetNoDataValue(np.nan)                      ## Set no data value to NaN
outband.FlushCache()



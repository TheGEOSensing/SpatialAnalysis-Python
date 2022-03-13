from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import os

##---------- Open the destination folder ---------##
os.chdir('E:\Remote Sensing of Cryosphere - Gulab Sir\Assignment\Ass1 Landsat NDSI\LC08_L1TP_147036_20190910_20190917_01_T1')

##---------- Open the LANDSAT-8 optical bands ---------##
blue = gdal.Open("LC08_L1TP_147036_20190910_20190917_01_T1_B2.tif")
green = gdal.Open("LC08_L1TP_147036_20190910_20190917_01_T1_B3.tif")
red = gdal.Open("LC08_L1TP_147036_20190910_20190917_01_T1_B4.tif")

##---------- Read the optical bands as array ---------##
blue =  blue.GetRasterBand(1).ReadAsArray()
green = green.GetRasterBand(1).ReadAsArray()
red =   red.GetRasterBand(1).ReadAsArray()

##---------- Plot the band images and histogram ---------##
plt.figure()
plt.imshow(blue)
plt.hist(blue.flatten(), bins = 50)


##---------- Define the stretching and apply them ---------##
def MinMaxStretch(x):
    return((x - np.nanmin(x))/(np.nanmax(x) - np.nanmin(x)))
def Percentile_Stretch(x):
    return((x - np.nanpercentile(x, 2))/(np.nanpercentile(x, 98) - np.nanpercentile(x,2)))
def Std_Stretch(x):
    return((x - (np.nanmean(x)-np.nanstd(x)*2))/((np.nanmean(x)+ np.nanstd(x)*2) - (np.nanmean(x)- np.nanstd(x)*2)))

     
red_minmax = MinMaxStretch(red)
blue_minmax = MinMaxStretch(blue)
green_minmax = MinMaxStretch(green)

red_Percentile = Percentile_Stretch(red)
blue_Percentile = Percentile_Stretch(blue)
green_Percentile = Percentile_Stretch(green)

red_Std_Stretch = Std_Stretch(red)
blue_Std_Stretch = Std_Stretch(blue)
green_Std_Stretch = Std_Stretch(green)

##---------- Plot the strecthed images and histograms ---------##
plt.figure()
plt.hist(green_Percentile.flatten(), bins = 50)
plt.imshow(blue_Percentile)

##---------- Create RGB Stack and copare the images ---------##
rgb_minmax = np.dstack((red_minmax, green_minmax, blue_minmax))
plt.figure()
plt.imshow(rgb_minmax)

rgb_Percentile = np.dstack((red_Percentile, green_Percentile, blue_Percentile))
plt.figure()
plt.imshow(rgb_Percentile)

rgb_Std = np.dstack((red_Std_Stretch, green_Std_Stretch, blue_Std_Stretch))
plt.figure()
plt.imshow(rgb_Std)
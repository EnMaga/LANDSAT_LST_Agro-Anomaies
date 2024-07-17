import gdal
import numpy as np
from osgeo import gdal_array

rasterfile = r"C:\Test\nh_66_5.tif" 

percentiles = [0,25,50,75,100] 

rasterArray = gdal_array.LoadFile(rasterfile) #Read raster as numpy array

for p in percentiles:
    print('{0}th percentile is: {1}'.format(p, np.percentile(rasterArray,p)))

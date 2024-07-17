import gdal
import numpy as np
from osgeo import gdal_array

rasterfile = r"Path where the CSV file is stored\file.tif" 

percentiles = [0,25,50,75,100] 

rasterArray = gdal_array.LoadFile(rasterfile) #Read raster as numpy array

for p in percentiles:
    print('{0}th percentile is: {1}'.format(p, np.percentile(rasterArray,p)))

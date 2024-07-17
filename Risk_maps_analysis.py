import os
import numpy as np
import rasterio
from scipy.ndimage import map_coordinates
from scipy.stats import percentileofscore
import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
from shapely.geometry import Point
import pandas as pd

# Load TIFF files
directory = "/Users/enricomagazzino/Downloads/Spring_LSTs"

file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.tif')]


# Read and stack files
stacked_data = []
for file_path in file_paths:
    with rasterio.open(file_path) as src:
        data = src.read(1)  # Read the first band
        stacked_data.append(data)

# Convert
stacked_data = np.stack(stacked_data, axis=0)

# Calculate the percentile for each pixel
percentile_data = np.zeros_like(stacked_data[0], dtype=np.float32)

for i in range(stacked_data.shape[1]):
    for j in range(stacked_data.shape[2]):
        pixel_values = stacked_data[:, i, j]
        mean_pixel_value = np.mean(pixel_values)
        percentile_data[i, j] = percentileofscore(pixel_values, mean_pixel_value)

percentile_data_signed = (percentile_data - 50) * 2  # Transforming percentile into signed values

# Define new output
meta = src.meta.copy()
meta.update({
    'dtype': 'float32',
    'count': 1
})

output_path = "/Users/enricomagazzino/Downloads/Spring_LSTs/Spring_risk_map2.tif"
with rasterio.open(output_path, 'w', **meta) as dst:
    dst.write(percentile_data_signed.astype(np.float32), 1)

#VALUES EXTRACTION FROM BUFFER AROUND WINE FARMS AND VISUALISATION IN MATRIX (Area vs Season)

# Load files
gdf = gpd.read_file('.../POINTGEOPACKAGE.gpkg')

rasters = {
    "Spring": '.../Spring_risk_map.tif',
    "Winter": '.../Winter_risk_map.tif',
    "Summer": '.../Summer_risk_map.tif',
    "Autumn": '.../Autumn_risk_map.tif'
}

# Define a buffer size in meters
buffer_size = 50 

results = pd.DataFrame()

# Extract pixel values within the buffer for each point
for season, raster_path in rasters.items():
    with rasterio.open(raster_path) as src:
        affine = src.transform
        array = src.read(1)

        for idx, row in gdf.iterrows():
            point = row.geometry
            buffer = point.buffer(buffer_size)
            mask = geometry_mask([buffer], transform=affine, invert=True, out_shape=array.shape)
            masked_data = np.ma.masked_array(array, mask=~mask)
            mean_value = masked_data.mean()

            results = results.append({
                "Point_ID": idx,
                "Season": season,
                "Mean_Value": mean_value
            }

            # Add the attributes from the GeoPackage
            for col in gdf_attributes.columns:
                result[col] = row[col]

            results = results.append(result, ignore_index=True)

tools.display_dataframe_to_user(name="Raster Values with 50m Buffer and Attributes", dataframe=results)

#results.head()

#PLOT EXTRACTED VALUES IN A MATRIX (Area vs Season excluding area NO due to Landsat 7 sensor error causing bias

# Create a custom colormap
from matplotlib.colors import LinearSegmentedColormap

colors = [(0, "blue"), (0.5, "white"), (1, "red")]
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

# Exclude the 'NO' area 
pivot_table_filtered = pivot_table.drop(index='NO')

# Plotting the filtered pivot table as a heatmap 
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table_filtered, annot=True, cmap=cmap, center=0)
plt.title('Mean Raster Values by Season and Area (Excluding NO Area)')
plt.xlabel('Season')
plt.ylabel('Area')
plt.show()

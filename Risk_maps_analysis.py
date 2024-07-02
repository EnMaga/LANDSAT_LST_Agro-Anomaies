import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#############################
## Plot correlation matrix ##
#############################

wine_data = pd.read_csv(r"Path where the CSV file is stored\Wine_Estates_DF_Month.csv")

# Calculate seasonal temperature standard deviation
wine_data['Season'] = wine_data['Month'].map({
    'December': 'Winter', 'January': 'Winter', 'February': 'Winter',
    'March': 'Spring', 'April': 'Spring', 'May': 'Spring',
    'June': 'Summer', 'July': 'Summer', 'August': 'Summer',
    'September': 'Autumn', 'October': 'Autumn', 'November': 'Autumn'
})

# Calculate the standard deviation for each season and area
seasonal_std = wine_data.groupby(['Area', 'Season'])['Temperature'].std().reset_index()

# Calculate the percentiles of the standard deviation
seasonal_std['Std_Percentile'] = seasonal_std['Temperature'].rank(pct=True) * 100

# Create a pivot table for the heatmap
pivot_table = seasonal_std.pivot('Area', 'Season', 'Std_Percentile')

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Seasonal Temperature Standard Deviation Percentile by Area')
plt.xlabel('Season')
plt.ylabel('Area')
plt.show()

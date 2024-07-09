import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels as sm
from sklearn.preprocessing import StandardScaler
from scipy.stats import linregress

scaler = StandardScaler()

anomalies_df = pd.read_csv(r"Path where the CSV file is stored\DummyData.csv")
buds_fert_df = pd.read_csv(r"Path where the CSV file is stored\DummyData2.csv")

# Merging the dataframes on common columns (fid, Area, ID, Varieté, Azienda, LatN, LongE)
merged_df = pd.merge(anomalies_df, buds_fert_df[['fid', 'Year', 'Potential_Fert', 'n_Blind_Buds', 'n_Steril_Buds']], 
                     on=['fid', 'Year'], how='left')

# Create a column for previous year temperature
merged_df['Previous_Year'] = merged_df['Year'] - 1
previous_year_temp = merged_df[['fid', 'ID', 'Year', 'Temperature']].rename(columns={'Year': 'Previous_Year', 'Temperature': 'Previous_Temperature'})

# Merge the previous year temperature back to the original dataframe
final_df = pd.merge(merged_df, previous_year_temp, on=['fid', 'ID', 'Previous_Year'], how='left')

# Display the final dataframe
import ace_tools as tools; tools.display_dataframe_to_user(name="Final DataFrame with Added Columns", dataframe=final_df)

# Show the first few rows of the final dataframe
final_df.head()

# Remove rows with Year 2017
final_df = final_df[final_df['Year'] != 2017]

# Filter the data to include only relevant months for the previous year's temperature
months = [5, 6, 7, 8]
filtered_df = final_df[final_df['Month'].isin(months)]

# Group by fid, ID, Varieté, Azienda, Year and calculate the average temperature for the specified months
avg_temp_df = filtered_df.groupby(['fid', 'ID', 'Variet', 'Azienda', 'Year'])['Previous_Temperature'].mean().reset_index()

# Merge this average temperature back with the final_df
merged_avg_temp_df = pd.merge(final_df, avg_temp_df, on=['fid', 'ID', 'Variet', 'Azienda', 'Year'], suffixes=('', '_avg_05060708'))

# Remove rows with NaN values in the relevant columns
cleaned_df = merged_avg_temp_df.dropna(subset=['Potential_Fert', 'Previous_Temperature_avg_05060708'])

# Plotting the correlation
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))

# Loop through each variety to create separate plots with trendlines
for variety in cleaned_df['Variet'].unique():
    subset = cleaned_df[cleaned_df['Variet'] == variety]
    sns.regplot(x='Previous_Temperature_avg_05060708', y='Potential_Fert', data=subset, label=variety)

plt.title('Correlation of Potential Fertility with Previous Year\'s Average Temperature (May-Aug) by Variety')
plt.xlabel('Previous Year\'s Average Temperature (May-Aug)')
plt.ylabel('Potential Fertility')
plt.legend(title='Variety')
plt.show()

# Prepare a table to store the results
results = []

# Loop through each variety and calculate the correlation coefficient and significance
for variety in cleaned_df['Variet'].unique():
    subset = cleaned_df[cleaned_df['Variet'] == variety]
    slope, intercept, r_value, p_value, std_err = linregress(subset['Previous_Temperature_avg_05060708'], subset['Potential_Fert'])
    results.append({
        'Variety': variety,
        'Correlation Coefficient (r)': r_value,
        'P-value': p_value
    })

# Create a DataFrame for the results
results_df = pd.DataFrame(results)
import ace_tools as tools; tools.display_dataframe_to_user(name="Correlation and Significance Results", dataframe=results_df)

# Display the results table
results_df

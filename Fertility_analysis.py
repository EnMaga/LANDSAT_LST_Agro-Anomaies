import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels as sm
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

data = pd.read_csv(r"Path where the CSV file is stored\Sub_Fert_table.csv")

# Filter data for May and June
data_may_june = data[(data['Month'] == 5) | (data['Month'] == 6)]

# We need to convert 'Aspect_face' and 'Area' to numerical values using one-hot encoding
data_may_june_encoded = pd.get_dummies(data_may_june, columns=['Aspect_face', 'Area'])

# Group by 'Variety' and 'Month' to get the mean values
monthly_means_encoded = data_may_june_encoded.groupby(['Variety', 'Month']).mean().reset_index()

# Normalize the relevant columns
columns_to_normalize = ['Temperature', 'Altitude', 'Potential_Fert']
monthly_means_encoded[columns_to_normalize] = scaler.fit_transform(monthly_means_encoded[columns_to_normalize])

# Prepare the data for regression with selected variables
X_vars = ['Temperature', 'Altitude'] + [col for col in monthly_means_encoded.columns if col.startswith('Aspect_face_') or col.startswith('Area_')]
X_selected = monthly_means_encoded[X_vars]
y_selected = monthly_means_encoded['Potential_Fert']

# Add a constant to the model (intercept)
X_selected = sm.add_constant(X_selected)

# Fit the multiple linear regression model
model_selected = sm.OLS(y_selected, X_selected).fit()

# Display the summary of the multiple linear regression model
model_selected_summary = model_selected.summary()
model_selected_summary


#################################################
## Example plot for Temperature and Blind Buds ##
#################################################


# Prepare the data
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%y')
areas = data['Area'].unique()
varieties = data['Variety'].unique()

# Create a line plot with two y-axes: temperature and number of blind buds by area, with solid vertical lines connected to the temperature axis
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10), sharex=True, sharey=False)

for i, area in enumerate(areas):
    ax1 = axes.flat[i]
    ax2 = ax1.twinx()  # Create a second y-axis
    
    # Plot overall temperature trend for each area
    subset_temp = data[data['Area'] == area]
    sns.lineplot(data=subset_temp, x='Date', y='Temperature', ax=ax1, color='blue', alpha=0.7)
    
    # Plot number of blind buds trend for each variety within the area
    for variety in varieties:
        subset_buds = data[(data['Area'] == area) & (data['Variety'] == variety)]
        if not subset_buds.empty:
            sns.lineplot(data=subset_buds, x='Date', y='n_Blind_Buds', ax=ax2, linestyle='dashed', alpha=0.7)
    
    # Add solid vertical lines for May and June for each year, connected to the temperature axis
    years = subset_temp['Date'].dt.year.unique()
    for year in years:
        ax1.axvline(pd.to_datetime(f'{year}-05-01'), color='grey', linestyle='-', linewidth=1)
        ax1.axvline(pd.to_datetime(f'{year}-06-01'), color='grey', linestyle='-', linewidth=1)
    
    ax1.set_ylabel('Temperature', color='blue')
    ax2.set_ylabel('Number of Blind Buds', color='green')
    ax1.set_title(f'Area: {area}')
    ax1.tick_params(axis='x', rotation=45)

fig.tight_layout()
fig.suptitle('Temperature and Number of Blind Buds Trends by Area', y=1.02)
plt.show()

###############################################################################
## Example plot for Temperature and Blind Buds correlation matrix and trends ##
###############################################################################

#The DF "data_may_june" needs do be created filtering only for those months

# Encode 'Aspect_face' and 'Area' as numerical values for correlation calculation
data_may_june['Aspect_Encoded'] = data_may_june['Aspect_face'].astype('category').cat.codes
data_may_june['Area_Encoded'] = data_may_june['Area'].astype('category').cat.codes

# Select relevant columns for correlation analysis
correlation_columns = ['Potential_Fert', 'Temperature', 'Area_Encoded', 'Aspect_Encoded', 'Altitude']

# Calculate the correlation matrix
correlation_matrix = data_may_june[correlation_columns].corr()

# Display the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Potential Fertility, Temperature, Area, Aspect, Altitude')
plt.show()

# Display the correlation matrix as a dataframe for detailed inspection
correlation_matrix


# Remove '_Encoded' terms and rename the columns for better readability
correlation_matrix.columns = ['Potential Fertility', 'Temperature', 'Area', 'Aspect', 'Altitude']
correlation_matrix.index = ['Potential Fertility', 'Temperature', 'Area', 'Aspect', 'Altitude']

# Display the updated correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Potential Fertility, Temperature, Area, Aspect, Altitude')
plt.show()

# Display the correlation matrix as a dataframe for detailed inspection
correlation_matrix


# Scatter plot of Temperature vs Potential Fertility with regression lines for each Variety
plt.figure(figsize=(12, 8))
sns.lmplot(x='Temperature', y='Potential_Fert', hue='Variety', data=data_may_june, aspect=1.5, markers=["o", "s", "D", "^", "v"], legend_out=False)
plt.title('Temperature vs Potential Fertility per Variety')
plt.xlabel('Temperature')
plt.ylabel('Potential Fertility')
plt.legend(title='Variety')
plt.show()

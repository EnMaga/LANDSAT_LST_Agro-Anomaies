import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data = pd.read_csv(r"Path where the CSV file is stored\DummyData.csv")

#######################
## Explorative plots ##
#######################

# Reorder the months for plotting
ordered_months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']

# Set up the matplotlib figure
plt.figure(figsize=(15, 10))

# Temperature vs Area
plt.subplot(2, 2, 1)
sns.boxplot(x='Area', y='Temperature', data=data)
plt.title('Temperature vs Area')

# Temperature vs Aspect (Exposure)
plt.subplot(2, 2, 2)
sns.boxplot(x='Aspect', y='Temperature', data=data)
plt.title('Temperature vs Aspect')

# Temperature vs Month with ordered months
plt.subplot(2, 2, 3)
sns.boxplot(x='Month', y='Temperature', data=data, order=ordered_months)
plt.title('Temperature vs Month (Ordered)')
plt.xticks(rotation=45)

# Temperature vs Altitude
plt.subplot(2, 2, 4)
sns.scatterplot(x='Altitude', y='Temperature', data=data)
plt.title('Temperature vs Altitude')

plt.tight_layout()
plt.show()


###########################################################
## Boxplot of temperature versus aspect, grouped by area ##
###########################################################

# Set up the matplotlib figure for visualization
plt.figure(figsize=(10, 6))

# Boxplot for Temperature vs Aspect grouped by Area
sns.boxplot(data=data, x='Aspect', y='Temperature', hue='Area')
plt.title('Temperature vs Aspect Grouped by Area')
plt.xlabel('Aspect')
plt.ylabel('Temperature (°C)')
plt.legend(title='Area')
plt.tight_layout()
plt.show()

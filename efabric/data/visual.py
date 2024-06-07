import pandas as pd
import matplotlib.pyplot as plt

# Load data from the CSV file
fashion_data = pd.read_csv('fashion_data.csv')

# Convert the 'date_sale' column to datetime type if it's not already
fashion_data['date_sale'] = pd.to_datetime(fashion_data['date_sale'])

# Create a new column for the year of sale
fashion_data['year'] = fashion_data['date_sale'].dt.year

# Group the data by season, year, and category
grouped_data = fashion_data.groupby(['year', 'season', 'category']).size().unstack().fillna(0)

# Sort the seasons based on the custom order
custom_order = ['Winter', 'Spring', 'Summer', 'Autumn']
grouped_data = grouped_data.reindex(custom_order, level=1)

# Plotting
plt.figure(figsize=(12, 8))
grouped_data.plot(kind='bar', stacked=True, ax=plt.gca())
plt.title('Sales by Category over Seasons with Years')
plt.xlabel('Year and Season')
plt.ylabel('Number of Sales')
plt.grid(True)
plt.legend(grouped_data.columns)
plt.tight_layout()
plt.show()

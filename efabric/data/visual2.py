import pandas as pd
import matplotlib.pyplot as plt

# Loading data from a CSV file
fashion_data = pd.read_csv('../../../Desktop/data_analytics/fashion_data_filled.csv')

# Convert the date_sale column to datetime if it is not already converted
fashion_data['date_sale'] = pd.to_datetime(fashion_data['date_sale'], format='%Y-%m-%d')

# Order for seasons
season_order = ['Winter', 'Spring', 'Summer', 'Autumn']

# Determining the order of seasons
grouped_data = fashion_data.groupby(['season', 'category']).agg({'sales_count': 'sum'}).unstack().fillna(0)

# Reindex data to sort by season order
grouped_data = grouped_data.reindex(season_order)

# Graphing
plt.figure(figsize=(10, 6))
grouped_data.plot(ax=plt.gca())
plt.title('Sales by category and season')
plt.xlabel('Season')
plt.ylabel('Number of sales')
plt.grid(True)
plt.legend(grouped_data.columns.get_level_values(1))
plt.tight_layout()
plt.show()

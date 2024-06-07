import pandas as pd

# Load data from CSV file
fashion_data = pd.read_csv('fashion_data.csv')

# Convert 'date_sale' column to datetime
fashion_data['date_sale'] = pd.to_datetime(fashion_data['date_sale'])

# Create DataFrame with full range of months and categories
full_date_range = pd.date_range(start=fashion_data['date_sale'].min(), end=fashion_data['date_sale'].max(), freq='MS')
all_categories = fashion_data['category'].unique()
full_index = pd.MultiIndex.from_product([full_date_range, all_categories], names=['date_sale', 'category'])
full_dataframe = pd.DataFrame(index=full_index).reset_index()

# Merge data with full DataFrame
merged_data = pd.merge(full_dataframe, fashion_data, on=['date_sale', 'category'], how='left')

# Fill missing values in 'sales_count' with the average between neighboring months for each category
merged_data['sales_count'] = merged_data.groupby('category')['sales_count'].transform(lambda x: x.interpolate())

# Replace non-finite values with zeros
merged_data['sales_count'] = merged_data['sales_count'].fillna(0)

# Round sales_count to integers
merged_data['sales_count'] = merged_data['sales_count'].round().astype(int)

# Map months to seasons
month_to_season = {month: season for season, months in {'Winter': [12, 1, 2], 'Spring': [3, 4, 5], 'Summer': [6, 7, 8],
                                                        'Autumn': [9, 10, 11]}.items() for month in months}
# Add 'season' column
merged_data['season'] = merged_data['date_sale'].dt.month.map(month_to_season)

# Save data to new CSV file
merged_data.to_csv('fashion_data_filled.csv', index=False)

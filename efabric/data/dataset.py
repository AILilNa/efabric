import pandas as pd
from datetime import datetime

# Loading data from xls file
fashion_data = pd.read_excel('fashion_data.xls')

# Removing unnecessary columns
columns_to_drop = ['product_id', 'product_name', 'gender', 'pattern', 'color', 'age_group', 'price', 'material',
                   'season', 'reviews_count', 'average_rating', 'out_of_stock_times', 'brand', 'discount',
                   'last_stock_date', 'wish_list_count']
fashion_data.drop(columns_to_drop, axis=1, inplace=True)

# Create a new column 'date_sale'
fashion_data['date_sale'] = fashion_data.apply(lambda row: datetime(row['year_of_sale'], row['month_of_sale'], 1)
                                               .replace(day=1).strftime('%Y-%m-%d'), axis=1)

# Grouping by 'date_sale' and 'category', summing 'sales_count'
fashion_data = fashion_data.groupby(['date_sale', 'category']).agg({'sales_count': 'sum'}).reset_index()

# Convert 'date_sale' column to datetime format for sorting
fashion_data['date_sale'] = pd.to_datetime(fashion_data['date_sale'])

# Add a 'season' column
fashion_data['season'] = fashion_data['date_sale'].dt.month.map({12: 'Winter', 1: 'Winter', 2: 'Winter',
                                                                 3: 'Spring', 4: 'Spring', 5: 'Spring',
                                                                 6: 'Summer', 7: 'Summer', 8: 'Summer',
                                                                 9: 'Autumn', 10: 'Autumn', 11: 'Autumn'})

# Sort by date
fashion_data.sort_values(by='date_sale', inplace=True)

# Save data to a new CSV file with the specified date format
fashion_data.to_csv('fashion_data.csv', index=False, columns=['date_sale', 'season', 'category', 'sales_count'],
                    date_format='%Y-%m-%d')

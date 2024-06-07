import base64
import io
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Load data
data = pd.read_csv('data/fashion_data_filled.csv')

# Preprocessing
data['date_sale'] = pd.to_datetime(data['date_sale'])
data = data.groupby(['category', 'date_sale']).agg({'sales_count': 'sum'}).reset_index()

# Set frequency for date index if possible
try:
    data.set_index('date_sale', inplace=True)
    data.index.freq = pd.infer_freq(data.index)
except ValueError:
    pass  # If frequency inference fails, just proceed without setting frequency

# Sort data by date
data.sort_index(inplace=True)


# Function to train SARIMA model for a specific category
def train_sarima_model(category_data):
    try:
        # Splitting the data into training and testing sets
        train = category_data[category_data.index < '2021-01-01']
        test = category_data[category_data.index >= '2021-01-01']

        # Check if enough data is available for training
        if len(train) < 20:  # Adjust this threshold as per your requirement
            print(f"Not enough data to train model for {category_data['category'].iloc[0]}")
            return None, None

        # Model training (using SARIMA)
        model = SARIMAX(train['sales_count'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12),
                        initialization='approximate_diffuse')
        model_fit = model.fit(disp=False)

        return model_fit, test
    except Exception as e:
        print(f"Error training model for {category_data['category'].iloc[0]}: {e}")
        return None, None


# Function to make predictions for a specific category
def predict_sales(model, test_data, category_name, forecast_end_date):
    try:
        # Generate predictions
        predictions = model.get_prediction(start=test_data.index[0], end=forecast_end_date)
        predictions_conf = predictions.conf_int()

        # Plotting actual vs predicted sales
        plt.figure(figsize=(10, 5))
        plt.plot(test_data.index, test_data['sales_count'], label='Actual')
        plt.plot(predictions.predicted_mean.index, predictions.predicted_mean, label='Predicted')
        plt.fill_between(predictions_conf.index, predictions_conf.iloc[:, 0], predictions_conf.iloc[:, 1], color='pink', alpha=0.3)
        plt.axvline(x=forecast_end_date, color='gray', linestyle='--', linewidth=1)  # Add vertical line for forecast end date
        plt.title(f'Forecast vs Actuals for {category_name}')
        plt.legend()

        # Save the plot as a bytes object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_uri = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

        # Forecasting for a specified date
        if forecast_end_date in predictions.predicted_mean.index:
            predicted_sales = predictions.predicted_mean.loc[forecast_end_date]

            # Round predicted sales to the nearest integer
            predicted_sales = int(round(predicted_sales))
            category_stock = {'Shirt': 1000, 'Blouse': 60, 'Shoes': 100, 'Jacket': 50, 'Skirt': 50, 'Jeans': 50,
                              'Dressed': 50, 'Shorts': 50}

            # Calculate reorder quantity: predicted sales - current stock
            if category_name in category_stock:
                reorder_quantity = predicted_sales - category_stock[category_name]
            else:
                reorder_quantity = predicted_sales  # Use predicted sales if category not found

            # Ensure reorder quantity is non-negative
            reorder_quantity = max(reorder_quantity, 0)
            print(f"Predicted sales of {category_name} on {forecast_end_date}: {predicted_sales}")

            # Check if enough stock is available
            if reorder_quantity <= 0:
                print(f"Enough stock available for {category_name} on {forecast_end_date}.")
            else:
                print(f"Reorder quantity for {category_name}: {reorder_quantity}")

            # Calculate Mean Squared Error (MSE)
            actual_values = test_data['sales_count']
            squared_errors = (predicted_sales - actual_values) ** 2
            mse = squared_errors.mean()
            print(f"Mean Squared Error (MSE) for {category_name}: {mse:.2f}")

            # Calculate Mean Absolute Error (MAE)
            mae = abs(predicted_sales - actual_values).mean()
            print(f"Mean Absolute Error (MAE) for {category_name}: {mae:.2f}")

            # Calculate a basic accuracy metric
            accuracy_threshold = 0.1  # Threshold for accuracy (e.g., within 10% of actual value)
            actual_value = test_data.loc[forecast_end_date, 'sales_count']
            is_accurate = abs(predicted_sales - actual_value) <= accuracy_threshold * actual_value
            accuracy_message = "Prediction is accurate" if is_accurate else "Prediction might deviate slightly"
            print(accuracy_message)

            return predicted_sales, plot_uri, None

        else:
            error_message = f"No prediction available for {category_name} on {forecast_end_date}."
            return None, None, error_message
    except Exception as e:
        error_message = f"Error predicting sales for {category_name}: {e}"
        return None, None, error_message

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_mock_data(filename, num_rows=5000):
    """
    Generates a mock CSV file with timestamped temperature and humidity readings.
    Intentionally introduces simulated sensor calibration errors.
    """
    start_time = datetime.now() - timedelta(days=7)
    
    data = []
    for i in range(num_rows):
        timestamp = start_time + timedelta(minutes=i*5)
        
        # Base readings
        temp = 20.0 + np.sin(i / 50.0) * 5.0 + random.uniform(-1, 1)
        humidity = 50.0 + np.cos(i / 50.0) * 10.0 + random.uniform(-2, 2)
        
        # Introduce simulated calibration errors (~2% of the data)
        if random.random() < 0.02:
            error_type = random.choice(['temp_spike', 'hum_impossible', 'both'])
            if error_type in ['temp_spike', 'both']:
                temp += random.uniform(50, 100) # Sudden temperature spike
            if error_type in ['hum_impossible', 'both']:
                humidity = random.choice([-20.0, 150.0]) # Impossible humidity values
                
        data.append([timestamp.strftime('%Y-%m-%d %H:%M:%S'), temp, humidity])
        
    df = pd.DataFrame(data, columns=['Timestamp', 'Temperature_C', 'Humidity_Percent'])
    df.to_csv(filename, index=False)
    print(f"Generated raw dataset: {filename} with {num_rows} rows.")

def clean_sensor_data(df):
    """
    Parses and filters the raw dataset to remove erroneous calibration data.
    """
    initial_count = len(df)
    
    # Convert Timestamp column to datetime objects
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Filter out impossible or highly improbable sensor readings
    # Valid Temperature range assumed: -10C to 50C
    # Valid Humidity range assumed: 0% to 100%
    clean_df = df[
        (df['Temperature_C'] >= -10.0) & 
        (df['Temperature_C'] <= 50.0) & 
        (df['Humidity_Percent'] >= 0.0) & 
        (df['Humidity_Percent'] <= 100.0)
    ]
    
    final_count = len(clean_df)
    removed_count = initial_count - final_count
    
    print(f"Filtering complete. Removed {removed_count} erroneous readings.")
    return clean_df

def visualize_data(raw_df, clean_df):
    """
    Engineers visual plots of the sensor measurements using matplotlib.
    Displays a diagnostic dashboard comparing raw vs. filtered data.
    """
    # Ensure datetime format for plotting
    raw_df['Timestamp'] = pd.to_datetime(raw_df['Timestamp'])
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Plot 1: Raw Data (Showing Calibration Errors)
    ax1.plot(raw_df['Timestamp'], raw_df['Temperature_C'], color='red', alpha=0.6, label='Raw Temp (C)')
    ax1.plot(raw_df['Timestamp'], raw_df['Humidity_Percent'], color='blue', alpha=0.6, label='Raw Humidity (%)')
    ax1.set_title('Raw Sensor Data (Showing Calibration Errors)')
    ax1.set_ylabel('Measurements')
    ax1.legend(loc='upper right')
    ax1.grid(True, linestyle=':', alpha=0.7)
    
    # Plot 2: Filtered Data (Cleaned Dataset)
    ax2.plot(clean_df['Timestamp'], clean_df['Temperature_C'], color='darkred', label='Filtered Temp (C)')
    ax2.plot(clean_df['Timestamp'], clean_df['Humidity_Percent'], color='darkblue', label='Filtered Humidity (%)')
    ax2.set_title('Filtered Sensor Data (Clean Dataset)')
    ax2.set_ylabel('Measurements')
    ax2.set_xlabel('Timestamp')
    ax2.legend(loc='upper right')
    ax2.grid(True, linestyle=':', alpha=0.7)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    csv_filename = "mock_sensor_data.csv"
    
    # Step 1: Generate the mock data
    generate_mock_data(csv_filename)
    
    # Read the generated data
    raw_dataframe = pd.read_csv(csv_filename)
    
    # Step 2: Parse and filter the dataset
    cleaned_dataframe = clean_sensor_data(raw_dataframe)
    
    # Step 3: Visualize the diagnostic results
    visualize_data(raw_dataframe, cleaned_dataframe)
    
    # Clean up the generated file after execution
    if os.path.exists(csv_filename):
        os.remove(csv_filename)
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# List of CSV files to load
local_data_files = ["bls_data_.csv", "bls_labor_force.csv", "Unemployment_rate.csv"]

# Title of the app
st.title('BLS Data Dashboard')

# Initialize an empty DataFrame to combine all data
data = pd.DataFrame(columns=["label", "series_id", "date", "value"])

# Load data from each CSV file and combine them
for file in local_data_files:
    if os.path.exists(file):  # Ensure file exists before loading
        local_data = pd.read_csv(file)
        print(f"Columns in {file}: {local_data.columns}")  # Print columns to debug

        # Check if 'date' or other date-related column exists
        if 'date' in local_data.columns:
            local_data['date'] = pd.to_datetime(local_data['date'], errors='coerce')  # Parse dates
        elif 'period' in local_data.columns:  # Adjust based on your data file structure
            local_data['date'] = pd.to_datetime(local_data['period'], errors='coerce')
        else:
            st.warning(f"File {file} does not contain a 'date' or 'period' column.")

        # If the date was successfully added or found, concatenate the data
        if 'date' in local_data.columns:
            data = pd.concat([data, local_data])

# Check if the data is not empty
if not data.empty:
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot each series' data
    for series_id in data["series_id"].unique():
        series_data = data[data["series_id"] == series_id]
        ax.plot(series_data["date"], series_data["value"], label=series_id)

    ax.set_title('BLS Data')
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.legend()
    ax.grid(True)

    # Display the plot
    st.pyplot(fig)

    # Display raw data
    st.subheader("Raw Data")
    st.write(data)
else:
    st.error("No data available to display.")

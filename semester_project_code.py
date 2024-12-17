pip install streamlit

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your processed data
data = pd.read_csv("bls_data.csv")  # Replace with the path to your data file

# Streamlit app layout
st.title('BLS Data Dashboard')

# Create a plot
fig, ax = plt.subplots(figsize=(12, 6))
for series_id in data["series_id"].unique():
    series_data = data[data["series_id"] == series_id]
    ax.plot(series_data["date"], series_data["value"], label=series_id)

ax.set_title('BLS Data')
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.legend()
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)

# Optionally display the raw data
st.subheader("Raw Data")
st.write(data)

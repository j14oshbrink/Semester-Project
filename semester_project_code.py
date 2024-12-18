import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load the data from CSV files
bls_data = pd.read_csv("bls_data.csv")
bls_labor_force = pd.read_csv("bls_labor_force.csv")
unemployment_rate = pd.read_csv("Unemployment_rate.csv")

# Set the title of the Streamlit app
st.title("BLS Data Dashboard")

# Visualizing Total Nonfarm Employment Data (Line plot)
st.subheader("Total Nonfarm Employment")
if not bls_data.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    for series_id in bls_data["series_id"].unique():
        series_data = bls_data[bls_data["series_id"] == series_id]
        ax.plot(pd.to_datetime(series_data["date"]), series_data["value"], label=series_id)
    ax.set_title('Total Nonfarm Employment over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Employment Value')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("No data available for Total Nonfarm Employment.")

# Visualizing Labor Force Participation Data (Bar chart)
st.subheader("Labor Force Participation")
if not bls_labor_force.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    for series_id in bls_labor_force["series_id"].unique():
        series_data = bls_labor_force[bls_labor_force["series_id"] == series_id]
        ax.bar(pd.to_datetime(series_data["date"]), series_data["value"], label=series_id)
    ax.set_title('Labor Force Participation over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Participation Rate')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("No data available for Labor Force Participation.")

# Visualizing Unemployment Rate Data (Line plot)
st.subheader("Unemployment Rate")
if not unemployment_rate.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    for series_id in unemployment_rate["series_id"].unique():
        series_data = unemployment_rate[unemployment_rate["series_id"] == series_id]
        ax.plot(pd.to_datetime(series_data["date"]), series_data["value"], label=series_id)
    ax.set_title('Unemployment Rate over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Unemployment Rate (%)')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("No data available for Unemployment Rate.")
    
st.subheader("employmnet_population_ratio.csv")
if not employmnet_population_ratio.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    for series_id in employmnet_population_ratio["series_id"].unique():
        series_data = employmnet_population_ratio[employmnet_population_ratio["series_id"] == series_id]
        ax.plot(pd.to_datetime(series_data["date"]), series_data["value"], label=series_id)
    ax.set_title('Employment Population Ratio')
    ax.set_xlabel('Date')
    ax.set_ylabel('Unemployment Rate (%)')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("No data available for Unemployment Rate.")

# Optionally, display raw data for each dataset
st.subheader("Raw Data: Total Nonfarm Employment")
st.write(bls_data)

st.subheader("Raw Data: Labor Force Participation")
st.write(bls_labor_force)

st.subheader("Raw Data: Unemployment Rate")
st.write(unemployment_rate)


st.subheader("Raw Data: Employment Population Ratio")
st.write(Employment population ratio)

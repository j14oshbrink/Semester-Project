import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Here is where I will be getting the csv files from the data. Each set will be its own to have separate graphs.
bls_data = pd.read_csv("bls_data.csv")
bls_labor_force = pd.read_csv("bls_labor_force.csv")
unemployment_rate = pd.read_csv("Unemployment_rate.csv")
employment_population_ratio = pd.read_csv("employment_population_ratio.csv")


st.title("BLS Data Dashboard")

# I am going to put my visual coding for each graph below
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

# Using a bar chart for Labor Force Participation (Bar chart)
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

# Unemployment rate Line plot
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
    
# Employment population ratio line plot
st.subheader("Employment Population Ratio")
if not employment_population_ratio.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    for series_id in employment_population_ratio["series_id"].unique():
        series_data = employment_population_ratio[employment_population_ratio["series_id"] == series_id]
        ax.plot(pd.to_datetime(series_data["date"]), series_data["value"], label=series_id)
    ax.set_title('Employment Population Ratio over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Employment Population Ratio (%)')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("No data available for Employment Population Ratio.")

#This will display the raw data sets as well
st.subheader("Raw Data: Total Nonfarm Employment")
st.write(bls_data)

st.subheader("Raw Data: Labor Force Participation")
st.write(bls_labor_force)

st.subheader("Raw Data: Unemployment Rate")
st.write(unemployment_rate)

st.subheader("Raw Data: Employment Population Ratio")
st.write(employment_population_ratio)

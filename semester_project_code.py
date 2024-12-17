import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("bls_data.csv") 
data = pd.read_csv("bls_labor_force.csv")
data = pd.read_csv("Unemployment_rate.csv")

st.title('BLS Data Dashboard')

fig, ax = plt.subplots(figsize=(12, 6))
for series_id in data["series_id"].unique():
    series_data = data[data["series_id"] == series_id]
    ax.plot(series_data["date"], series_data["value"], label=series_id)

ax.set_title('BLS Data')
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.subheader("Raw Data")
st.write(data)

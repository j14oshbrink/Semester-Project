import os
import requests
import pandas as pd
from datetime import datetime

# API key and BLS endpoint URL
api_key = "86b67e98f5134a7386ce62902a756492"  # Make sure to replace with your actual API key
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# Define the series IDs for multiple data sources (e.g., non-farm workers, unemployment rate, labor force)
series_ids = [
    "SMS31000000000000001", # Total Nonfarm NE
    "LASST370000000000008", # Labor Force Participation NC
    "LASST310000000000003", # Unemployment Rate Neb
    "BDS0000001000000000110004LQ5" # Gross Job Losses AL
]

# Local file paths for each data source
local_data_files = [
    "bls_data.csv",  # Total Nonfarm NE
    "bls_labor_force.csv",  # Labor Force Participation NC
    "Unemployment_rate.csv"  # Unemployment Rate Neb
]

# Fetch data from the BLS API
def fetch_bls_data(start_year, end_year):
    payload = {
        "seriesid": series_ids,
        "startyear": start_year,
        "endyear": end_year,
        "registrationkey": api_key
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "REQUEST_SUCCEEDED":
            return data
        else:
            print("Error:", data.get("message"))
    else:
        print("HTTP Error:", response.status_code)

    return None


# Process the fetched data and return as a DataFrame
def process_bls_data(data):
    all_data = []
    for series in data["Results"]["series"]:
        series_id = series["seriesID"]
        for item in series["data"]:
            # Assuming the response contains a 'year' and 'periodName'
            date_str = f"{item['year']} {item['periodName']}"
            date = datetime.strptime(date_str, "%Y %B")  # Convert to datetime object
            all_data.append({
                "series_id": series_id,
                "date": date,
                "value": float(item["value"])
            })
    return pd.DataFrame(all_data)


# Load existing local data if available
def load_local_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, parse_dates=["date"])
    else:
        return pd.DataFrame(columns=["series_id", "date", "value"])


# Save the data to a CSV file
def save_local_data(data, file_path):
    data.to_csv(file_path, index=False)


# Main function to update data and save it locally
def update_data():
    combined_data = pd.DataFrame(columns=["series_id", "date", "value"])

    # Load data from all local CSV files
    for file in local_data_files:
        local_data = load_local_data(file)
        combined_data = pd.concat([combined_data, local_data], ignore_index=True)

    # If there's existing data, get the latest year; otherwise, fetch from the current year
    if not combined_data.empty:
        latest_date = combined_data["date"].max()
        start_year = latest_date.year
    else:
        start_year = datetime.now().year

    # Set the end year to the current year
    end_year = datetime.now().year

    # Fetch new data from the API
    new_data = fetch_bls_data(start_year, end_year)

    if new

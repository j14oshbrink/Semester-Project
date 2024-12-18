import os
import requests
import pandas as pd
from datetime import datetime

#This is the API key and URL from the Labor
api_key = "86b67e98f5134a7386ce62902a756492"  
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# I am changing the names of the ids to what the actual data is to make it easier to read the graphics, and know what the series code is measuring
series_ids = [
    "SMS31000000000000001",  # Total nonfarm NE
    "LASST370000000000008",  # Labor force participation NC
    "LASST310000000000003",  # Unemployment rate Neb.
    "LAUST310000000000007" #Employment-Population Ratio: Nebraska (U
]

# The csv files I am using
data_files = {
    "bls_data": "bls_data.csv",
    "bls_labor_force": "bls_labor_force.csv",
    "unemployment_rate": "Unemployment_rate.csv",
    "employment_population_ratio": "employment_population_ratio.csv"
}

# fetching the data
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

def process_bls_data(data):
    all_data = []

    # data being processed for each of the data sets
    for series in data["Results"]["series"]:
        series_id = series["seriesID"]
        for item in series["data"]:
            # Extract relevant fields: date, value
            all_data.append({
                "series_id": series_id,
                "value": float(item["value"]),
                "date": item.get("year", "") + " " + item.get("periodName", "")  # Year and period
            })

    return pd.DataFrame(all_data)

# Saving the datasets
def save_data_to_csv(data, file_path):
    data.to_csv(file_path, index=False)


def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["series_id", "date", "value"])


def update_data():
    # Set the start and end years for fetching data
    start_year = 2022  # You can change this if needed
    end_year = datetime.now().year


    new_data = fetch_bls_data(start_year, end_year)
    
    if new_data:
        # Process the fetched data
        processed_data = process_bls_data(new_data)
        

        # Saving Total Nonfarm data
        total_nonfarm_data = processed_data[processed_data["series_id"] == "SMS31000000000000001"]
        save_data_to_csv(total_nonfarm_data, data_files["bls_data"])

        # Saving Labor Force Participation data
        labor_force_data = processed_data[processed_data["series_id"] == "LASST370000000000008"]
        save_data_to_csv(labor_force_data, data_files["bls_labor_force"])

        # Saving Unemployment Rate data
        unemployment_rate_data = processed_data[processed_data["series_id"] == "LASST310000000000003"]
        save_data_to_csv(unemployment_rate_data, data_files["unemployment_rate"])

        #Saving employment population ratio
        employment_population_ratio_data = processed_data[processed_data["series_id"] == "LAUST310000000000007"]
        save_data_to_csv(employment_population_ratio_data, data_files["employment_population_ratio"])

        print("Data updated and saved successfully.")
    else:
        print("No new data fetched.")

import os
import requests
import pandas as pd
from datetime import datetime

# API key and BLS endpoint URL
api_key = "86b67e98f5134a7386ce62902a756492"  # Make sure to replace with your actual API key
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# Define the series IDs (e.g., non-farm workers and unemployment rate)
series_ids = [
    "SMS31000000000000001",  # Total nonfarm NE
    "LASST370000000000008",  # Labor force participation NC
    "LASST310000000000003", # Unemployment rate Neb.
    "BDS0000001000000000110004LQ5"  # Gross Job Losses AL
]

# Mapping for `series_id` to their human-readable labels
series_id_labels = {
    "SMS31000000000000001": "Total Nonfarm, NE",
    "LASST370000000000008": "Labor Force Participation, NC",
    "LASST310000000000003": "Unemployment Rate, NE",
    "BDS0000001000000000110004LQ5": "Gross Job Losses, AL"
}

# Local file path to save the data (e.g., CSV file)
local_data_file = "bls_data_.csv"
local_data_file1 = "bls_labor_force.csv"
local_data_file2 = "Unemployment_rate.csv"

# Map for converting quarter strings to month names
quarter_to_month = {
    "1st Quarter": "March",
    "2nd Quarter": "June",
    "3rd Quarter": "September",
    "4th Quarter": "December"
}

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

    # Extract relevant data from the response
    for series in data["Results"]["series"]:
        series_id = series["seriesID"]
        label = series_id_labels.get(series_id, "Unknown Label")  # Get the label for the series_id, default to "Unknown Label"

        for item in series["data"]:
            # Check if the period is a quarter or a month
            if item['periodName'] in quarter_to_month:
                # Convert the quarter to a month name (e.g., "1st Quarter" -> "March")
                month_name = quarter_to_month[item['periodName']]
                date_str = f"{item['year']} {month_name}"
            else:
                # If it's a month name, use it directly
                date_str = f"{item['year']} {item['periodName']}"

            # Convert the date string to a datetime object
            date = datetime.strptime(date_str, "%Y %B")
            all_data.append({
                "series_id": series_id,
                "label": label,  # Add the label to each record
                "date": date,
                "value": float(item["value"])
            })

    return pd.DataFrame(all_data)


# Load existing local data if available
def load_local_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, parse_dates=["date"])
    else:
        return pd.DataFrame(columns=["label", "series_id", "date", "value"])


# Save the data to a CSV file
def save_local_data(data, file_path):
    data.to_csv(file_path, index=False)


# Main function to update data and save it locally
def update_data():
    local_data = load_local_data(local_data_file)

    # Set start year to 2022
    start_year = 2022

    # Set the end year to the current year
    end_year = datetime.now().year

    # Fetch new data from the API
    new_data = fetch_bls_data(start_year, end_year)

    if new_data:
        new_data_df = process_bls_data(new_data)

        # Combine existing data with new data (and remove duplicates)
        combined_data = pd.concat([local_data, new_data_df]).drop_duplicates()

        # Save the updated data back to the CSV file
        save_local_data(combined_data, local_data_file)
        print("Data updated successfully.")
    else:
        print("No new data fetched.")

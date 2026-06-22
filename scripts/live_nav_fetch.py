import requests
import pandas as pd

# Dictionary: scheme_code -> file_name
funds = {
    119551: "SBI_Bluechip",
    120503: "ICICI_Bluechip",
    118632: "Nippon_Large_Cap",
    119092: "Axis_Bluechip",
    120841: "Kotak_Bluechip",
    125497: "HDFC_Top_100_Direct_NAV" 
}

# Loop through each fund
for code, fund_name in funds.items():
    print(f"\nFetching NAV for {fund_name}...")

    # API URL
    url = f"https://api.mfapi.in/mf/{code}"

    # Get response from API
    response = requests.get(url)

    # Convert JSON response to dictionary
    data = response.json()

    # Extract NAV history
    nav_data = data["data"]

    # Convert to DataFrame
    df = pd.DataFrame(nav_data)

    # Save as CSV in data/raw folder
    file_path = f"data/raw/{fund_name}.csv"
    df.to_csv(file_path, index=False)

    print(f"{fund_name} saved successfully at {file_path}")

print("\nAll 5 fund NAV files downloaded successfully!")
import pandas as pd
import requests

scheme_codes = [
    125497,  # HDFC Top 100 Direct
    119551,  # SBI Bluechip
    120503,  # ICICI Bluechip
    118632,  # Nippon Large Cap
    119092,  # Axis Bluechip
    120841   # Kotak Bluechip
]

all_records = []

for code in scheme_codes:
    url = f"https://api.mfapi.in/mf/{code}"

    try:
        response = requests.get(url)
        data = response.json()

        scheme_name = data["meta"]["scheme_name"]

        for row in data["data"]:
            all_records.append({
                "scheme_code": code,
                "scheme_name": scheme_name,
                "date": row["date"],
                "nav": row["nav"]
            })

        print(f"Downloaded: {scheme_name}")

    except Exception as e:
        print(f"Error fetching {code}: {e}")

nav_history = pd.DataFrame(all_records)

nav_history.to_csv(
    "data/raw/nav_history.csv",
    index=False
)

print(nav_history.head())
print("Rows:", len(nav_history))
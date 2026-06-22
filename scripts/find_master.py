import requests
import pandas as pd

schemes = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
    "HDFC_Top100": 125497
}

fund_master = []

for name, code in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"
    data = requests.get(url).json()

    meta = data.get("meta", {})

    fund_master.append({
        "scheme_code": code,
        "scheme_name": name,
        "fund_house": meta.get("fund_house"),
        "scheme_category": meta.get("scheme_category"),
        "scheme_type": meta.get("scheme_type")
    })

fund_master_df = pd.DataFrame(fund_master)

fund_master_df.to_csv("data/raw/fund_master.csv", index=False)

print(fund_master_df)


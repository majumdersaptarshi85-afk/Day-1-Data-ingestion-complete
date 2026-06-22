import pandas as pd

fund_master = pd.read_csv("data/raw/fund_master.csv")
nav_history = pd.read_csv("data/raw/nav_history.csv")

print(fund_master.columns)
print(nav_history.columns)

# Unique scheme codes from both datasets
master_codes = set(fund_master['scheme_code'].unique())
nav_codes = set(nav_history['scheme_code'].unique())

# Codes present in fund_master but missing in nav_history
missing_codes = master_codes - nav_codes

print("Total schemes in fund_master:", len(master_codes))
print("Total schemes in nav_history:", len(nav_codes))
print("Missing scheme codes:", len(missing_codes))

if missing_codes:
    missing_df = fund_master[
        fund_master['scheme_code'].isin(missing_codes)
    ][['scheme_code', 'scheme_name']]

    print("\nMissing AMFI Codes:")
    print(missing_df)
else:
    print("\n All AMFI scheme codes in fund_master are present in nav_history.")


matched_codes = len(master_codes.intersection(nav_codes))
validation_pct = (matched_codes / len(master_codes)) * 100

print(f"Validation Rate: {validation_pct:.2f}%")
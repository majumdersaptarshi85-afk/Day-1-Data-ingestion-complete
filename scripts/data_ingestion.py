import pandas as pd
import os
import re

# Folder containing raw CSV files
folder = "data/raw"

print("="*80)
print("STEP 1: LOAD ALL CSV FILES")
print("="*80)

# Load and inspect all CSV files
for file in os.listdir(folder):
    if file.endswith(".csv"):
        path = os.path.join(folder, file)

        print("\n" + "="*60)
        print("FILE:", file)

        try:
            df = pd.read_csv(path)

            print("Shape:", df.shape)
            print("\nData Types:")
            print(df.dtypes)

            print("\nFirst 5 Rows:")
            print(df.head())

            print("\nMissing Values:")
            print(df.isnull().sum())

            print("\nDuplicate Rows:", df.duplicated().sum())

        except Exception as e:
            print("Error reading file:", e)

print("\n" + "="*80)
print("STEP 2: EXPLORE FUND MASTER")
print("="*80)

# Load fund_master.csv
fund_master_path = os.path.join(folder, "fund_master.csv")
fund_df = pd.read_csv(fund_master_path)

print("\nFund Master Columns:")
print(fund_df.columns.tolist())

# Adjust column names if needed based on your dataset
if "fund_house" in fund_df.columns:
    print("\nUnique Fund Houses:")
    print(fund_df["fund_house"].dropna().unique())

if "category" in fund_df.columns:
    print("\nUnique Categories:")
    print(fund_df["category"].dropna().unique())

if "subcategory" in fund_df.columns:
    print("\nUnique Sub-Categories:")
    print(fund_df["subcategory"].dropna().unique())

if "risk_grade" in fund_df.columns:
    print("\nUnique Risk Grades:")
    print(fund_df["risk_grade"].dropna().unique())

if "scheme_code" in fund_df.columns:
    print("\nSample Scheme Codes:")
    print(fund_df["scheme_code"].head(10).tolist())

print("\n" + "="*80)
print("STEP 3: VALIDATE AMFI CODES")
print("="*80)

# Load nav_history.csv if available, otherwise build from raw NAV files
nav_history_path = os.path.join(folder, "nav_history.csv")
if os.path.exists(nav_history_path):
    nav_df = pd.read_csv(nav_history_path)
else:
    print(f"Warning: nav_history.csv not found at {nav_history_path}. Building from raw NAV files.")
    nav_dfs = []

    def normalize_name(name):
        return re.sub(r"[^a-z0-9]", "", str(name).lower())

    fund_name_to_code = {
        normalize_name(row.get("scheme_name", "")): row.get("scheme_code")
        for _, row in fund_df.iterrows()
        if pd.notna(row.get("scheme_name", None))
    }

    for file in os.listdir(folder):
        if not file.endswith(".csv") or file == "fund_master.csv":
            continue

        file_path = os.path.join(folder, file)
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Skipping {file}: unable to read file ({e})")
            continue

        if "date" not in df.columns or "nav" not in df.columns:
            print(f"Skipping {file}: expected columns ['date', 'nav'], found {df.columns.tolist()}")
            continue

        scheme_name = os.path.splitext(file)[0]
        normalized_file_name = normalize_name(scheme_name)
        scheme_code = fund_name_to_code.get(normalized_file_name)

        if scheme_code is None:
            for normalized_fund_name, code in fund_name_to_code.items():
                if normalized_fund_name in normalized_file_name or normalized_file_name in normalized_fund_name:
                    scheme_code = code
                    break

        if scheme_code is None:
            print(f"Skipping {file}: could not map file name to a fund_master scheme_code")
            continue

        df["scheme_code"] = scheme_code
        nav_dfs.append(df[["scheme_code", "date", "nav"]])

    if len(nav_dfs) == 0:
        raise FileNotFoundError("No raw NAV files could be used to build nav_history.csv.")

    nav_df = pd.concat(nav_dfs, ignore_index=True)
    print(f"Built nav history from {len(nav_dfs)} raw NAV files.")

# Try common scheme code column names
fund_code_col = None
nav_code_col = None

for col in fund_df.columns:
    if "scheme" in col.lower() and "code" in col.lower():
        fund_code_col = col
        break

for col in nav_df.columns:
    if "scheme" in col.lower() and "code" in col.lower():
        nav_code_col = col
        break

if fund_code_col and nav_code_col:
    fund_codes = set(fund_df[fund_code_col].dropna().astype(str))
    nav_codes = set(nav_df[nav_code_col].dropna().astype(str))

    missing_codes = fund_codes - nav_codes

    print("Total fund_master scheme codes:", len(fund_codes))
    print("Total nav_history scheme codes:", len(nav_codes))
    print("Missing scheme codes in nav_history:", len(missing_codes))

    if len(missing_codes) > 0:
        print("Sample missing codes:", list(missing_codes)[:10])
    else:
        print("All scheme codes from fund_master exist in nav_history.")

else:
    print("Could not identify scheme code columns automatically.")

print("\n" + "="*80)
print("STEP 4: DATA QUALITY SUMMARY")
print("="*80)

print("""
Data Quality Summary:
1. All CSV files were loaded and inspected.
2. Missing values and duplicate rows were checked.
3. fund_master unique values for fund house, category, sub-category, and risk grade were explored.
4. AMFI scheme codes were validated between fund_master and nav_history.
5. Any missing scheme codes were reported above.
""")
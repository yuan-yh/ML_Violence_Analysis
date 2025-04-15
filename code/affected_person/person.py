import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
hospitals = ['1', '2', 'NLH', 'MHA']
dfs = {hosp: pd.read_csv(f'{hosp}.csv') for hosp in hospitals}

# Check for null/na values in the 'Occupational Category of Person Affected' field
for hosp, df in dfs.items():
    df.replace('<N/S>', pd.NA, inplace=True)  # Treat <N/S> as missing
    column_has_nulls = df['Occupational Category of Person Affected'].isna().any()
    print(f"{hosp} - 'Person Affected' NULL Val:", column_has_nulls)

all_dates = pd.concat([df[['Occupational Category of Person Affected']].dropna() for df in dfs.values()])

all_dates['Occupational Category of Person Affected'].unique()
# Output

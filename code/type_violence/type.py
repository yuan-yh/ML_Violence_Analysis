import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
hospitals = ['1', '2', 'NLH', 'MHA']
dfs = {hosp: pd.read_csv(f'{hosp}.csv') for hosp in hospitals}

# Check for null/na values in the 'Type of Violence' field
for hosp, df in dfs.items():
    df.replace('<N/S>', pd.NA, inplace=True)  # Treat <N/S> as missing
    column_has_nulls = df['Type of Violence'].isna().any()
    print(f"{hosp} - 'Type of Violence' NULL Val:", column_has_nulls)

all_dates = pd.concat([df[['Type of Violence']].dropna() for df in dfs.values()])

all_dates['Type of Violence'].unique()

violence_mapping = {
    # Physical violence
    'Physical': 'Physical',
    'Abuse/Assault (Physical)': 'Physical',
    'Abuse/Assault (Physical Attempted)': 'Physical (Attempted)',
    
    # Verbal violence
    'Verbal': 'Verbal',
    'Abuse/Assault (Verbal)': 'Verbal',
    'abuse/assault (verbal)': 'Verbal',
    'Abuse/Assault (verbal)': 'Verbal',
    
    # Combined physical and verbal
    'Physical, Verbal': 'Physical & Verbal',
    
    # Attempted violence
    'Attempted Violence (near miss)': 'Attempted Violence',
    'Attempted Violence (Near Miss)': 'Attempted Violence',
    'Verbal, Attempted Violence (near miss)': 'Verbal & Attempted Violence',
    'Threat of Violence': 'Attempted Violence',
    
    # Written/digital
    'Written and/or Digital': 'Written/Digital',
    'Written/Digital': 'Written/Digital',
    
    # Sexual violence
    'Sexual Contact': 'Sexual Violence',
    'Sexual Harassment': 'Sexual Violence',
    
    # Other categories
    'Aggression Toward an Inanimate Object': 'Property Damage',
    'Property Damage/Vandalism': 'Property Damage',
    'Stalking': 'Stalking',
    'Disorderly Person': 'Other',
    'Alleged Abuse/Assault': 'Other'
}


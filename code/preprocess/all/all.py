import pandas as pd
import numpy as np

# Load datasets
hospitals = ['1', '2', 'NLH', 'MHA']
dfs = {hosp: pd.read_csv(f'{hosp}.csv') for hosp in hospitals}

# Specify the columns you want to concatenate
columns_to_concat = ['Event Date', 'Facility Type', 'Department/Office Incident Took Place', 'Occupational Category of Person Affected', 'Aggressor', 'Type of Violence', 'Primary Contributing Factors', 'Severity of Assault', 'Primary Assault Description', 'Assault Description', 'Emotional and/ or Psychological Impact', 'Level of Care Needed', 'Response Action Taken']

# Concatenate the specified columns from all DataFrames
all_selected_data = pd.concat([df[columns_to_concat] for df in dfs.values()])

all_selected_data.to_csv('all.csv', index=False)
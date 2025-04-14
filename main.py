import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib.colors import LinearSegmentedColormap

# Load datasets (1&2 for unknown hospital)
hospitals = ['1', '2', 'NLH', 'MHA']
dfs = {hosp: pd.read_csv(f'{hosp}.csv') for hosp in hospitals}

# Check for columns / fields
for hosp, df in dfs.items():
    print(f"{hosp} columns:", df.columns.tolist())

###################### Date ###################### 
# Check for null/na values in the 'Event Date' field
for hosp, df in dfs.items():
    column_has_nulls = df['Event Date'].isna().any()
    print(f"{hosp} - 'Event Date' NULL Val:", column_has_nulls)

# Ensure a consistent date format - 'datetime'
for hosp, df in dfs.items():
    dfs[hosp]['Event Date'] = pd.to_datetime(dfs[hosp]['Event Date'])
    # # Handle missing/incorrect time values
    # dfs[hosp].dropna(subset=['Event Date'], inplace=True)

# Draw date distribution for each hospital as subplots
# Histogram
plt.figure(figsize=(15, 10))
for i, hosp in enumerate(hospitals, 1):
    plt.subplot(2, 2, i)
    sns.histplot(dfs[hosp]['Event Date'], bins=30, kde=True)
    plt.title(f'Hospital {hosp} - Event Date Distribution')
    plt.xlabel('Event Date')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Histogram with gradient
plt.figure(figsize=(15, 10))
gradient = LinearSegmentedColormap.from_list('gr', ["#EBA625", "#8C0000"])

for i, hosp in enumerate(hospitals, 1):
    plt.subplot(2, 2, i)
    n, bins, patches = plt.hist(dfs[hosp]['Event Date'], bins=30)
    
    # Apply gradient color to bars
    for patch, val in zip(patches, n):
        patch.set_facecolor(gradient(val / max(n)))
    
    plt.title(f'Hospital {hosp}', fontsize=14)
plt.tight_layout()
plt.show()

# Line Plot
plt.figure(figsize=(15, 10))
for i, hosp in enumerate(hospitals, 1):
    plt.subplot(2, 2, i)
    
    # Get value counts of dates and sort by date
    date_counts = dfs[hosp]['Event Date'].value_counts().sort_index()
    
    sns.lineplot(x=date_counts.index, y=date_counts.values)
    plt.title(f'Hospital {hosp} - Event Date Distribution')
    plt.xlabel('Event Date')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
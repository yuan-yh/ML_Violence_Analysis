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
###################### Date.Subplot ###################### 
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
    
    if (hosp == '1' or hosp == '2'):
      plt.title(f'Hospital {hosp}', fontsize=14)
    else:
      plt.title(f'{hosp}', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Count')
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

###################### Date.All ###################### 
all_dates = pd.concat([df[['Event Date']] for df in dfs.values()])

plt.figure(figsize=(10, 6))
sns.histplot(all_dates['Event Date'], bins=30, kde=True)
plt.title('Overall WPV Date Distribution')
plt.xlabel('Date')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

###################### Date.All.Weekday ###################### 
# Define the proper ordering for weekdays and months
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

# Heatmap
all_dates['Month'] = all_dates['Event Date'].dt.month_name()

heatmap_data = all_dates.pivot_table(
    index='Weekday',
    columns='Month',
    aggfunc='size',
    fill_value=0
)

plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt="d")
plt.title('Overall WPV Submission by Weekday', fontsize=14)
plt.tight_layout()
plt.show()

# Histogram
plt.figure(figsize=(10, 6))
gradient = LinearSegmentedColormap.from_list('gr', ["#EBA625", "#8C0000"])
    
# Calculate counts for each weekday
counts = all_dates['Weekday'].value_counts().reindex(weekday_order, fill_value=0)

# Normalize counts for color mapping
norm = plt.Normalize(vmin=counts.min(), vmax=counts.max())
colors = [gradient(norm(val)) for val in counts]

# Use barplot instead of countplot
sns.barplot(
    x=counts.index,
    y=counts.values,
    order=weekday_order,
    palette=colors,
)

plt.title('Overall WPV Submission - Weekday Distribution', fontsize=14)
plt.xlabel('Weekday')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Line Plot
# Add weekday and month columns to each hospital's dataframe
for hosp in hospitals:
    df = dfs[hosp]
    df['Weekday'] = df['Event Date'].dt.day_name()
    df['Month'] = df['Event Date'].dt.month_name()

# Combined weekday distribution in one plot (for comparison)
plt.figure(figsize=(12, 6))
for hosp in hospitals:
    weekday_counts = dfs[hosp]['Weekday'].value_counts().reindex(weekday_order)
    plt.plot(weekday_order, weekday_counts, marker='o', label=f'Hospital {hosp}')
    
plt.title('Overall WPV Submission - Weekday Distribution')
plt.xlabel('Weekday')
plt.ylabel('Count')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

###################### Date.Subplot.Month ###################### 
for hosp in hospitals:
    df = dfs[hosp]
    df['Weekday'] = df['Event Date'].dt.day_name()
    df['Month'] = df['Event Date'].dt.month_name()

# Histogram Month
plt.figure(figsize=(10, 6))
gradient = LinearSegmentedColormap.from_list('gr', ["#EBA625", "#8C0000"])
    
# Calculate counts for each weekday
counts = all_dates['Month'].value_counts().reindex(month_order, fill_value=0)

# Normalize counts for color mapping
norm = plt.Normalize(vmin=counts.min(), vmax=counts.max())
colors = [gradient(norm(val)) for val in counts]

# Use barplot instead of countplot
sns.barplot(
    x=counts.index,
    y=counts.values,
    order=month_order,
    palette=colors,
)

plt.title('Overall WPV Submission - Month Distribution', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Line Plot Month
# Combined weekday distribution in one plot (for comparison)
plt.figure(figsize=(12, 6))
for hosp in hospitals:
    month_counts = dfs[hosp]['Month'].value_counts().reindex(month_order)
    plt.plot(month_order, month_counts, marker='o', label=f'Hospital {hosp}')
    
plt.title('Overall WPV Submission - Month Distribution')
plt.xlabel('Month')
plt.ylabel('Count')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

###################### Date.All.Weekday ###################### 
# Extract day and month
all_dates['Day'] = all_dates['Event Date'].dt.day
all_dates['Month'] = all_dates['Event Date'].dt.month_name()

# Define month order
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Pivot table for heatmap
heatmap_data = all_dates.pivot_table(
    index='Day',
    columns='Month',
    aggfunc='size',
    fill_value=0
)

# Plot
plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=0.5, annot=True, fmt="d")
plt.title('Overall WPV - Calendar View', fontsize=14)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Day of Month', fontsize=12)
plt.tight_layout()
plt.show()

###################### Date.Subplot.Weekday ###################### 
# Histogram Weekday
plt.figure(figsize=(15, 10))
gradient = LinearSegmentedColormap.from_list('gr', ["#EBA625", "#8C0000"])

for i, hosp in enumerate(hospitals, 1):
    plt.subplot(2, 2, i)
    df = dfs[hosp]
    
    # Calculate counts for each weekday
    counts = df['Weekday'].value_counts().reindex(weekday_order, fill_value=0)
    
    # Normalize counts for color mapping
    norm = plt.Normalize(vmin=counts.min(), vmax=counts.max())
    colors = [gradient(norm(val)) for val in counts]
    
    # Use barplot instead of countplot
    sns.barplot(
        x=counts.index,
        y=counts.values,
        order=weekday_order,
        palette=colors,
    )

    if (hosp == '1' or hosp == '2'):
        plt.title(f'Hospital {hosp} - Weekday Distribution', fontsize=14)
    else:
        plt.title(f'{hosp} - Weekday Distribution', fontsize=14)
    plt.xlabel('Weekday')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Heatmap by weekday and month for each hospital
plt.figure(figsize=(16, 12))
for i, hosp in enumerate(hospitals, 1):
    plt.subplot(2, 2, i)
    
    # Create pivot table (ensure counts are integers)
    heatmap_data = dfs[hosp].pivot_table(
        index='Weekday',
        columns='Month',
        values='Event Date',  
        aggfunc='count',  # This should return integers
        fill_value=0
    ).astype(int)  # Force conversion to integers
    
    # Reorder rows and columns
    heatmap_data = heatmap_data.reindex(weekday_order)
    existing_months = [m for m in month_order if m in heatmap_data.columns]
    heatmap_data = heatmap_data[existing_months]
    
    # Use fmt="d" since we ensured data is integer
    sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=.5)
    if (hosp == '1' or hosp == '2'):
        plt.title(f'Hospital {hosp} - Weekday vs Month Distribution', fontsize=14)
    else:
        plt.title(f'{hosp} - Weekday vs Month Distribution', fontsize=14)
    plt.xlabel('Month')
    plt.ylabel('Weekday')
    
plt.tight_layout()
plt.show()

###################### Time ###################### 
# One of the given dataset provides specific timeslots when users start to fill the report, which can be used to infer event time
# This comes from only 1-month record, which is less reliable though.
if '2' in dfs:
    # Extract time component
    df_2 = dfs['2'].copy()
    df_2['Event Time'] = df_2['Event Date'].dt.time
    
    # Convert to hours for better visualization
    df_2['Hour'] = df_2['Event Date'].dt.hour + df_2['Event Date'].dt.minute/60 + df_2['Event Date'].dt.second/3600
    
    plt.figure(figsize=(10, 6))
    sns.histplot(df_2['Hour'], bins=24, kde=True)
    plt.title('Hospital 2 - Report Submission Time Distribution', fontsize=12)
    plt.xlabel('Hour of Day', fontsize=10)
    plt.ylabel('Number of Reports', fontsize=10)
    plt.xticks(range(0, 25, 2))
    plt.xlim(0, 24)
    plt.grid(True, alpha=0.3)
    
    # Add disclaimer about limited data
    plt.annotate(
        "Note: Data only covers one month; trends may not be representative.",
        xy=(0.5, -0.15), xycoords="axes fraction",
        ha="center", fontsize=9, color="gray"
    )
    
    plt.tight_layout()
    plt.show()

# Heatmap: Weekday vs. Hour
if '2' in dfs:
    df_2 = dfs['2'].copy()
    
    # Extract time and weekday
    df_2['Report Time'] = df_2['Event Date'].dt.time
    df_2['Hour'] = df_2['Event Date'].dt.hour + df_2['Event Date'].dt.minute/60 + df_2['Event Date'].dt.second/3600
    df_2['Weekday'] = df_2['Event Date'].dt.day_name()  # Monday, Tuesday, etc.
    
    # --- Weekday vs. Hour (Heatmap) ---
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df_2['Weekday'] = pd.Categorical(df_2['Weekday'], categories=weekday_order, ordered=True)
    
    # Pivot table for heatmap
    heatmap_data = df_2.pivot_table(
        index='Weekday',
        columns=pd.cut(df_2['Hour'], bins=range(0, 25, 1)),
        aggfunc='size',
        fill_value=0
    )
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=0.5)
    plt.title('Hospital 2 - Report Submission Time by Weekday', fontsize=12)
    plt.xlabel('Hour of Day', fontsize=10)
    plt.ylabel('Weekday', fontsize=10)
    plt.annotate(
        "Note: Data only covers one month; trends may not be representative.",
        xy=(0.5, -0.25), xycoords="axes fraction",
        ha="center", fontsize=9, color="gray"
    )
    plt.tight_layout()
    plt.show()
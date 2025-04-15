import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
hospitals = ['1', '2', 'NLH', 'MHA']
dfs = {hosp: pd.read_csv(f'{hosp}.csv') for hosp in hospitals}

# Check for null/na values in the 'Aggressor' field
for hosp, df in dfs.items():
    df.replace('<N/S>', pd.NA, inplace=True)  # Treat <N/S> as missing
    column_has_nulls = df['Aggressor'].isna().any()
    print(f"{hosp} - 'Aggressor' NULL Val:", column_has_nulls)

all_dates = pd.concat([df[['Aggressor']].dropna() for df in dfs.values()])

all_dates['Aggressor'].unique()
# Output:
# ['Patient', 'Employee (Lateral)', 'Visitor', 'Other', 'Inpatient', 'Resident (LTC)', 'Outpatient']

# Pie Chart (before removing overlapping)
# Combine all aggressor data (excluding NA values) and count occurrences
aggressor_counts = all_dates['Aggressor'].value_counts()

plt.figure(figsize=(12, 10))

# Custom colors (optional)
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6','#c4e17f']

# Explode the smallest slices for better visibility
explode = [0.05 if (count/sum(aggressor_counts)*100) < 5 else 0 for count in aggressor_counts]

# Plot with improved parameters
wedges, texts, autotexts = plt.pie(
    aggressor_counts,
    explode=explode,
    labels=aggressor_counts.index,
    autopct=lambda p: f'{p:.1f}%' if p >= 5 else '',  # Only show % for slices >5%
    startangle=140,
    colors=colors,
    textprops={'fontsize': 12},
    wedgeprops={'edgecolor': 'white', 'linewidth': 1},
    pctdistance=0.85
)

# Improve label appearance
plt.setp(autotexts, size=12, weight="bold")
plt.setp(texts, size=12)

# Add legend for small slices
plt.legend(
    wedges,
    aggressor_counts.index,
    title="Aggressor Types",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=12
)

# Add title with improved formatting
plt.title('Overall WPV Submission - Aggressor Distribution\n', 
          fontsize=16, fontweight='bold', pad=20)

# Equal aspect ratio
plt.axis('equal')

# Add white circle in center to make it a donut chart (optional)
# centre_circle = plt.Circle((0,0),0.70,fc='white')
# fig = plt.gcf()
# fig.gca().add_artist(centre_circle)

plt.tight_layout()
plt.show()

# Pie Chart (after removing overlapping)

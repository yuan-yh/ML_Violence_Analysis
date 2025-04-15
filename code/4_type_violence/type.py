import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
df = pd.read_csv('3_all_split_role.csv')
df['Type of Violence'].unique()

####################### Split multiple records in one field & Mapping #######################
# Split 'Type of Violence' by comma and explode into separate rows
df['Type of Violence'] = df['Type of Violence'].str.split(', ')
df = df.explode('Type of Violence')
df['Type of Violence'] = df['Type of Violence'].str.strip()

# Fill NaN with 'Unknown' for clarity
df['Type of Violence'] = df['Type of Violence'].fillna('Unknown')

# Define mapping to general categories
violence_mapping = {
    'Physical': 'Physical Violence',
    'Verbal': 'Verbal Abuse',
    'Attempted Violence (near miss)': 'Attempted Violence',
    'Attempted Violence (Near Miss)': 'Attempted Violence',
    'Written and/or Digital': 'Written/Digital',
    'Written/Digital': 'Written/Digital',
    'Abuse/Assault (Physical)': 'Physical Violence',
    'Abuse/Assault (Verbal)': 'Verbal Abuse',
    'abuse/assault (verbal)': 'Verbal Abuse',
    'Sexual Contact': 'Sexual Violence',
    'Aggression Toward an Inanimate Object': 'Disorderly Conduct',
    'Abuse/Assault (Physical Attempted)': 'Attempted Violence',
    'Sexual Harassment': 'Sexual Violence',
    'Threat of Violence': 'Threat',
    'Stalking': 'Stalking',
    'Abuse/Assault (verbal)': 'Verbal Abuse',
    'Disorderly Person': 'Disorderly Conduct',
    'Alleged Abuse/Assault': 'Alleged Abuse',
    'Property Damage/Vandalism': 'Property Damage',
    'Unknown': 'Unknown'
}

# Apply mapping and handle unmapped categories
df['General Violence_Category'] = df['Type of Violence'].map(violence_mapping)
df['General Violence_Category'] = df['General Violence_Category'].fillna('Other')

df['General Violence_Category'].unique()
df.head()

####################### Graph #######################
# Horizontal Bar
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

# Count and sort categories
category_counts = df['General Violence_Category'].value_counts().sort_values(ascending=True)

# palette = sns.color_palette("Reds_r", len(category_counts))

norm = plt.Normalize(category_counts.min(), category_counts.max())
palette = plt.cm.Reds(norm(category_counts))

# Plot
bar_plot = sns.barplot(
    x=category_counts.values,
    y=category_counts.index,
    palette=palette,
    edgecolor="black",
    linewidth=0.5,
    saturation=0.8
)

# Customize
plt.title("WPV - Distribution of Violence Categories", fontsize=14, pad=15)
plt.xlabel("Number of Incidents", fontsize=12)
plt.ylabel("Violence Category", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.3)

# Add value labels
for i, count in enumerate(category_counts):
    bar_plot.text(count + 0.5, i, f"{count}", va="center", fontsize=10)

plt.tight_layout()
plt.show()

# Pie Chart
plt.figure(figsize=(10, 8))
sns.set_style("white")

# Count categories and filter small slices
category_counts = df['General Violence_Category'].value_counts()
min_threshold = 0.02 * category_counts.sum()  # Group tiny categories into "Other"
filtered_counts = category_counts[category_counts > min_threshold]
other_count = category_counts[category_counts <= min_threshold].sum()
if other_count > 0:
    filtered_counts["Other"] = other_count

# Custom colors
colors = sns.color_palette("pastel")[:len(filtered_counts)]

# Plot
plt.pie(
    filtered_counts,
    labels=filtered_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    wedgeprops={"edgecolor": "white", "linewidth": 1},
    textprops={"fontsize": 10}
)

# Add title and legend
plt.title("WPV - Proportion of Violence Categories", fontsize=14, pad=20)
plt.legend(
    filtered_counts.index,
    title="Categories",
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

plt.tight_layout()
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
df = pd.read_csv('0_all.csv')
df['Facility Type'].unique()

####################### Map 'Location' based on 'Facility Type' and 'Department/Office Incident Took Place' #######################
# Step 1: Clean the 'Facility Type' column
df['Facility Type'] = df['Facility Type'].str.strip()
df['Facility Type'] = df['Facility Type'].replace({
    'Acute Care Hospital?': 'Acute Care Hospital',
    'ER ': 'ER',
    'ER room 11': 'ER',
    'ACU ': 'ACU',
    'Cary Medical ': 'Cary Medical'
})

# Step 2: Define a function to map departments under 'Other' Facility Type
def map_department(department):
    if pd.isna(department):
        return 'Other'
    department = str(department).strip().lower()
    if 'emergency' in department or 'ed' in department or 'er' in department:
        return 'ED/ER'
    elif 'psych' in department or 'behavioral' in department:
        return 'Behavioral Health Unit'
    elif 'medical/surgical' in department or 'med/surg' in department or 'medical surgical' in department:
        return 'Med/Surg/Inpatient'
    elif 'outpt' in department or 'outpatient' in department:
        return 'Outpatient'
    elif 'cardiac' in department or 'scu' in department:
        return 'Cardiac Unit'
    elif 'intensive care' in department or 'icu' in department:
        return 'ICU'
    elif 'hallway' in department or 'common area' in department or 'lobby' in department or 'parking' in department or 'grounds' in department:
        return 'Common Areas'
    elif 'lab' in department or 'radiology' in department or 'imaging' in department or 'ct scan' in department:
        return 'Diagnostic Services'
    elif 'therapy' in department or 'pt/ot' in department:
        return 'Therapies'
    elif 'surgery' in department or 'peri-op' in department:
        return 'Surgery & Peri-Op'
    elif 'ob' in department or 'women' in department or 'children' in department:
        return 'OB/Women & Children'
    elif 'care mgmt' in department or 'social work' in department:
        return 'Care Management'
    elif 'patient service' in department or 'registration' in department or 'scheduling' in department:
        return 'Patient Services'
    elif 'admin' in department or 'admitting' in department:
        return 'Administration'
    else:
        return 'Other Department'
    
# Step 3: Create 'General Location' column
df['General Location'] = df.apply(
    lambda row: map_department(row['Department/Office Incident Took Place']) 
    if row['Facility Type'] == 'Other' 
    else row['Facility Type'], axis=1
)

# Step 4: Standardize General Locations
general_location_mapping = {
    'ER': 'ED/ER',
    'ED': 'ED/ER',
    'Outpatient physical therapy': 'Outpatient',
    'Ambulatory Care Unit': 'Outpatient',
    'ACU': 'Ambulatory Care Unit',
    'SCU': 'Special Care Unit',
    'OB': 'OB/Women & Children',
    'Lab': 'Diagnostic Services',
    'Other Department': 'Other'
}
df['General Location'] = df['General Location'].replace(general_location_mapping)

# Further generalize the column
# Define the mapping dictionary
location_group_map = {
    # Clinical Units
    'ED/ER': 'Clinical Unit',
    'Med/Surg/Inpatient': 'Clinical Unit',
    'ICU': 'Clinical Unit',
    'Cardiac Unit': 'Clinical Unit',
    'Special Care Unit': 'Clinical Unit',
    'Behavioral Health Unit': 'Clinical Unit',
    'OB/Women & Children': 'Clinical Unit',
    'Outpatient': 'Clinical Unit',
    'Ambulatory Care Unit': 'Clinical Unit',
    'BC': 'Clinical Unit',

    # Support Services
    'Diagnostic Services': 'Support Service',
    'Care Management': 'Support Service',
    'Patient Services': 'Support Service',

    # Administrative / Shared
    'Administration': 'Administrative/Shared',
    'Common Areas': 'Administrative/Shared',

    # Facility / Location
    'Cary Medical': 'Facility/Location',
    'Acute Care Hospital': 'Facility/Location',

    # To Clarify
    'Other': 'Other'
}

# Map the new column
df['General Advanced Location'] = df['General Location'].map(location_group_map)

########################## Graph ##########################
# General Location - all
# Step 5: Visualization
plt.figure(figsize=(12, 8))
location_counts = df['General Location'].value_counts().sort_values(ascending=False)
bar_plot = sns.barplot(x=location_counts.values, y=location_counts.index, palette="viridis")
plt.title('WPV in Hospital - Distribution of Location', fontsize=16)
plt.xlabel('Count', fontsize=12)
plt.ylabel('Location', fontsize=12)

# Add value labels
for i, count in enumerate(location_counts):
    bar_plot.text(count + 0.5, i, f"{count}", va="center", fontsize=10)
  
plt.tight_layout()
plt.show()


# General Location - top k (15)
# Get value counts and select top N locations
top_n = 15  # Show top 15 locations - adjust as needed
location_counts = df['General Location'].value_counts().sort_values(ascending=True)  # Sort ascending for horizontal bar
top_locations = location_counts.tail(top_n)  # Get largest N values

# Create figure
plt.figure(figsize=(12, 8))
bar_plot = sns.barplot(x=top_locations.values, y=top_locations.index, palette="viridis")

# Customize appearance
plt.title(f'Top {top_n} Locations for Workplace Violence Incidents', 
          fontsize=16, pad=20, fontweight='bold')
plt.xlabel('Number of Incidents', fontsize=12, labelpad=10)
plt.ylabel('')  # Remove y-label since categories are self-explanatory
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# Add value labels with improved formatting
for i, count in enumerate(top_locations.values):
    # Place text inside bar for light colors, outside for dark
    color = bar_plot.patches[i].get_facecolor()
    brightness = sum(color[:3])/3  # Simple brightness calculation
    text_color = 'white' if brightness < 0.6 else 'black'
    x_pos = count if brightness < 0.6 else count + 0.5
    bar_plot.text(x_pos, i, 
                 f"{count:,}",  # Format with thousands separator
                 va='center', 
                 color=text_color,
                 fontsize=10,
                 fontweight='bold' if brightness < 0.6 else None)

# Add grid lines for better readability
plt.grid(axis='x', linestyle='--', alpha=0.3)

# Remove spines for cleaner look
sns.despine(left=True)

plt.tight_layout()
plt.show()

# Advanced General location
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set(style="whitegrid")

# Count the occurrences of each group
group_counts = df['General Advanced Location'].value_counts()

# Plot
plt.figure(figsize=(8, 5))
sns.barplot(x=group_counts.values, y=group_counts.index, palette="viridis")
plt.title("WPV in Hospital - Location Distribution")
plt.xlabel("Count")
plt.ylabel("Location")
plt.tight_layout()
plt.show()

# Pie chart
plt.figure(figsize=(10, 10))  # Increased figure size

# Get value counts and prepare data
location_counts = df['General Advanced Location'].value_counts()
total = location_counts.sum()
threshold = total * 0.02  # 2% threshold - adjust as needed

# Group small categories into "Other"
main_categories = location_counts[location_counts >= threshold]
other_count = location_counts[location_counts < threshold].sum()

if other_count > 0:
    main_categories['Other (<2%)'] = other_count

# Create custom autopct function to show both % and count
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return f'{pct:.1f}%\n({val:,})' if pct > 3 else ''
    return my_autopct

# Plot with improved settings
patches, texts, autotexts = plt.pie(
    main_categories,
    labels=main_categories.index,
    autopct=make_autopct(main_categories),
    startangle=140,
    colors=sns.color_palette("pastel"),
    pctdistance=0.8,
    textprops={'fontsize': 10}
)

# Improve label appearance
plt.setp(autotexts, size=10, weight="bold")
plt.setp(texts, size=10)

# Equal aspect ratio ensures pie is drawn as circle
plt.axis('equal')

# Add legend for small categories
if other_count > 0:
    plt.legend(
        loc='upper left',
        bbox_to_anchor=(1, 1),
        title='Small Categories',
        labels=[f'{k} ({v:,})' for k,v in location_counts[location_counts < threshold].items()]
    )

plt.title('WPV in Hospital - Location Distribution\n', 
          pad=20, fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()

################################ SUMMARY ################################
# Create summary table
summary = df['General Advanced Location'].value_counts().reset_index()
summary.columns = ['General Advanced Location', 'Count']
summary['Percentage'] = (summary['Count'] / summary['Count'].sum() * 100).round(1)

print(summary)
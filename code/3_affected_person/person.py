import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

####################### Check individual data #######################
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

####################### Check all data #######################
# Load datasets
df = pd.read_csv('all.csv')
df['Occupational Category of Person Affected'].unique()

# LC: regex, match substring
# Start from here , we need to categorize them, mapping into more general groups
def split_roles(s):
    if pd.isnull(s):
        return []
    parts = re.split(r',\s*(?![^()]*\))', s)
    return [part.strip() for part in parts if part.strip()]

def get_general_role(role):
    if pd.isnull(role) or not role.strip():
        return ''
    # Remove content within parentheses
    role_clean = re.sub(r'\(.*?\)', '', role).strip()
    # Split on '/' and take first part
    role_clean = role_clean.split('/')[0].strip()
    # Split on '-' and take first part
    role_clean = role_clean.split('-')[0].strip()
    if not role_clean:
        return ''
    role_lower = role_clean.lower()
    # Determine the general role based on keywords
    if 'nurse' in role_lower or 'np' in role_lower:
        return 'Nurse'
    elif 'physician' in role_lower or 'practitioner' in role_lower or 'app' in role_lower:
        return 'Physician/APP'
    elif 'security' in role_lower:
        return 'Security'
    elif 'allied health' in role_lower:
        return 'Allied Health'
    elif 'technologist' in role_lower or 'technician' in role_lower:
        return 'Technologist/Technician'
    elif 'administrat' in role_lower or 'registration' in role_lower or 'receptionist' in role_lower or 'mgr' in role_lower or 'manager' in role_lower or 'supv' in role_lower:
        return 'Admin/Management'
    elif 'patient' in role_lower:
        return 'Patient'
    elif 'family' in role_lower:
        return 'Family'
    elif 'emt' in role_lower or 'paramedic' in role_lower:
        return 'EMT/Paramedic'
    elif 'therapist' in role_lower:
        return 'Therapist'
    elif 'social worker' in role_lower:
        return 'Social Worker'
    elif 'facilities' in role_lower or 'plant operations' in role_lower:
        return 'Facilities'
    elif 'midwife' in role_lower:
        return 'Midwife'
    elif 'police' in role_lower:
        return 'Police'
    elif 'staff' in role_lower:
        return 'Staff'
    elif 'cna' in role_lower or 'nursing' in role_lower:
        return 'Nursing Assistant'
    elif 'psych' in role_lower or 'mental' in role_lower:
        return 'Mental Health'
    elif 'rehabilitation' in role_lower:
        return 'Rehabilitation'
    else:
        print(role_lower)
        return 'Other'

# Assuming 'all_dates' is the DataFrame with the required columns
# Split the occupational categories into individual roles
df['Split Roles'] = df['Occupational Category of Person Affected'].apply(split_roles)

# Explode the list of roles into separate rows
exploded_df = df.explode('Split Roles').reset_index(drop=True)

# Apply the general role categorization
exploded_df['General Role'] = exploded_df['Split Roles'].apply(get_general_role)

exploded_df['General Role'].unique()
# exploded_df.head()

exploded_df['General Role'].unique()

exploded_df.to_csv('all_split_role.csv', index=False)


####################### Graph #######################
# Filter out empty strings before counting
role_counts = exploded_df[exploded_df['General Role'] != '']['General Role'].value_counts().sort_values(ascending=True)

# Create figure
plt.figure(figsize=(10, 6))
sns.barplot(x=role_counts.values, y=role_counts.index, palette='viridis')

# Add annotations
for i, v in enumerate(role_counts.values):
    plt.text(v + 0.2, i, str(v), color='black', va='center')

plt.title('Overall WPV Role Distribution', pad=20)
plt.xlabel('Count')
plt.ylabel('Role')
plt.annotate(
        "Note: Empty entries are excluded.",
        xy=(0.5, -0.15), xycoords="axes fraction",
        ha="center", fontsize=9, color="gray"
    )
plt.tight_layout()
plt.show()
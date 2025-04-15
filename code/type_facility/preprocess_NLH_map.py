import pandas as pd
import numpy as np

df = pd.read_csv('NLH.csv')
df['Occupational Category of Person Affected'].unique()

###################### MAP FACILITY TYPE ######################
# Define mapping rules using keywords
conditions = [
    # Emergency Department (ED)
    df['Occupational Category of Person Affected'].str.contains('ED|EMT', case=False, na=False),
    
    # Psychiatric Units (BC or SCU)
    df['Occupational Category of Person Affected'].str.contains('PSYCH|MH|CLIN|SOCIAL WORKER', case=False, na=False),
    
    # Medical/Surgical/Inpatient (Med/Surg/Inpatient)
    df['Occupational Category of Person Affected'].str.contains('NURSE|CNA|ASSISTANT|PCA|STAFF RN|PHYSICAL THERAPIST|RESPIRATORY', case=False, na=False),
    
    # Other departments (e.g., Radiology, Security)
    df['Occupational Category of Person Affected'].str.contains('RAD|CT|SECURITY|TRANSPORT|ENVIRONMENTAL|TELECOMM', case=False, na=False),
]

# Assign labels based on the order of conditions
choices = ['ED', 'BC/SCU', 'Med/Surg/Inpatient', 'Other']

# Use numpy.select to apply the conditions/choices
df['Facility Type'] = np.select(conditions, choices, default='Other')

# Simplify labels if needed (e.g., merge BC/SCU into a single category)
df['Facility Type'] = df['Facility Type'].replace({'BC/SCU': 'BC'})  # Adjust based on your needs

# Optional: Handle empty strings or whitespace entries
df['Facility Type'] = df['Facility Type'].replace(r'^\s*$', 'Other', regex=True)

# Verify results
df[['Occupational Category of Person Affected', 'Facility Type']].head(10)


###################### MAP Severity of Assault ######################
###################### MAP Level of Care Needed ######################
# Process together as both base on 'Physical Injury Incurred? Level of Care', 'Nature of Injury', and 'Location of Injury on Body'
# Define the function to determine severity
def determine_severity(nature, location):
    severe_nature_terms = [
        'Head Injury', 'Bleeding/Hemorrhage', 'Laceration/Cut/Tear',
        'Bite - Human', 'Exposure - Body Fluids', 'Exposure - Other Hazardous Material',
        'Puncture', 'Hypertension', 'Strain/Sprain', 'Inflammation'
    ]
    severe_location_terms = [
        'head', 'face', 'eye', 'neck', 'chest', 'abdomen', 'groin',
        'genitals', 'testicles', 'throat', 'broken', 'concussion', 'rib',
        'spinal', 'back', 'hip', 'nose', 'skull', 'jaw', 'chin'
    ]
    
    # Check nature of injury
    if isinstance(nature, str):
        for term in severe_nature_terms:
            if term in nature:
                return 'Severe'
    
    # Check location (case-insensitive)
    if isinstance(location, str):
        location_lower = location.lower()
        for term in severe_location_terms:
            if term in location_lower:
                return 'Severe'
    
    return 'Mild'

# Apply the severity mapping
df['Severity of Assault'] = 'None'  # Default to 'None'
mask = df['Physical Injury Incurred? Level of Care'] == 'Yes'
df.loc[mask, 'Severity of Assault'] = df[mask].apply(
    lambda row: determine_severity(row['Nature of Injury'], row['Location of Injury on Body']), axis=1
)

# Handle 'Unknown' and '  ' as 'None'
df.loc[df['Physical Injury Incurred? Level of Care'].isin(['Unknown', '  ']), 'Severity of Assault'] = 'None'

# Base mapping on severity
df['Level of Care Needed'] = np.where(
    df['Severity of Assault'] == 'Severe', 'ED',
    np.where(df['Severity of Assault'] == 'Mild', 'Urgent Care', '<N/S>')
)

# Adjust for specific cases (e.g., exposures or bites)
exposure_mask = df['Nature of Injury'].str.contains('Exposure - Body Fluids|Exposure - Other Hazardous Material', na=False)
bite_mask = df['Nature of Injury'].str.contains('Bite - Human', na=False)
df.loc[exposure_mask | bite_mask, 'Level of Care Needed'] = 'ED'

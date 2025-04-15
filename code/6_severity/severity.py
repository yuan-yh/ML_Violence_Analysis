import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load datasets
df = pd.read_csv('0_all.csv')
df['Severity of Assault'].unique()

# Define the mapping from original values to simplified categories and numerical values
severity_mapping = {
    # Mild
    'Mild - Mild Soreness/Abrasions/Scratches/Small Bruises': 'Mild',
    'Mild': 'Mild',
    # Moderate
    'Moderate - Major Soreness/Cuts/Large Bruises': 'Moderate',
    'Moderate': 'Moderate',
    # Severe
    'Severe - Laceration/Fracture(s)/Head Injury': 'Severe',
    'Severe': 'Severe',
    # None
    'None - No Contact/Unwanted Contact w/No Injury': 'None',
    'None - No Contact or Unwanted Contact w/o Injury': 'None',
    # Other or missing
    'Other': 'Other',
    # Handle NaN or missing values (if any)
    pd.NA: 'Unknown',  # or 'Other' if you prefer
    None: 'Unknown',   # or 'Other'
}

# Numerical mapping (you can adjust the numbers as needed)
numerical_mapping = {
    'None': 0,
    'Mild': 1,
    'Moderate': 2,
    'Severe': 3,
    'Other': 4,
    'Unknown': np.nan
}

# Step 1: Create a cleaned 'Severity_Category' column
df['General Severity Category'] = df['Severity of Assault'].map(severity_mapping).fillna('Unknown')

# Step 2: Map to numerical values
df['General Severity Numerical'] = df['General Severity Category'].map(numerical_mapping)

# Verify the results
print("\nValue counts for Severity_Category:")
print(df['General Severity Category'].value_counts())

print("\nValue counts for Severity_Numerical:")
print(df['General Severity Numerical'].value_counts())

# Visualize the distribution
sns.countplot(data=df, x='General Severity Category', order=['None', 'Mild', 'Moderate', 'Severe', 'Other', 'Unknown'])
plt.title('WPV in Hospital - Distribution of Assault Severity')
plt.xticks(rotation=45)
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load datasets
df = pd.read_csv('6_7_all_map_emo.csv')
# df = pd.read_csv('0_all.csv')

df['Level of Care Needed'].unique()

###################### MAP to clean ######################
# Create mapping dictionary to standardize values
care_mapping = {
    'First Aid': 'First Aid',
    'ED': 'Emergency Department',
    'Urgent Care': 'Urgent Care',
    'Other (please specify)': 'Other',
    'Unknown': np.nan  # Treat unknown as missing
}

# Apply mapping and drop NA
df['Level of Care Needed'] = df['Level of Care Needed'].map(care_mapping).dropna()

###################### Graph ######################

###################### MAP to NUMBER ######################
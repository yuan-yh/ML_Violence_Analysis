import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ephem

################################## MOON ##################################
def get_moon_phase(date):
    date = ephem.Date(date)
    nnm = ephem.next_new_moon(date)
    pnm = ephem.previous_new_moon(date)
    lunation = (date - pnm) / (nnm - pnm)
    return lunation

# Load datasets
hospitals = ['1', '2', 'NLH', 'MHA']
dfs = {hosp: pd.read_csv(f'{hosp}.csv') for hosp in hospitals}
all_dates = pd.concat([df[['Event Date']] for df in dfs.values()])

# Apply to each date
all_dates['Moon Phase'] = all_dates['Event Date'].apply(lambda x: get_moon_phase(x))
# Create full moon indicator (phase between 0.9 and 1.1)
all_dates['Full Moon'] = all_dates['Moon Phase'].between(0.9, 1.1).astype(int)

plt.figure(figsize=(12, 6))

# Create bins - using more bins for better resolution
bins = np.linspace(0, 1, 21)  # 20 bins for better granularity

# Plot histogram
n, bins, patches = plt.hist(all_dates['Moon Phase'], bins=bins, 
                            edgecolor='black', alpha=0.7)

# Customize colors to represent moon phases
for i in range(len(patches)):
    if bins[i] >= 0.9 or bins[i] <= 0.1:  # New Moon (0) and near Full Moon (1)
        patches[i].set_facecolor('gold')
    elif 0.4 <= bins[i] <= 0.6:  # First Quarter
        patches[i].set_facecolor('lightblue')
    elif 0.65 <= bins[i] <= 0.85:  # Full Moon (approximately)
        patches[i].set_facecolor('yellow')

# Add vertical lines for key phases
plt.axvline(0, color='black', linestyle='--', alpha=0.5, label='New Moon')
plt.axvline(0.25, color='gray', linestyle=':', alpha=0.5)
plt.axvline(0.5, color='black', linestyle='--', alpha=0.5, label='First Quarter')
plt.axvline(0.75, color='black', linestyle='--', alpha=0.5, label='Full Moon')
plt.axvline(1, color='black', linestyle='--', alpha=0.5)

# Add labels and title
plt.title('WPV Distribution by Moon Phase', pad=20)
# 0 = New Moon, 0.5 = First Quarter, 0.75 = Full Moon, 1 = Next New Moon
plt.xlabel('Moon Phase')
plt.ylabel('Number of Events')
plt.xticks([0, 0.25, 0.5, 0.75, 1], 
           ['New Monn', 'Waxing\nCrescent', 'First\nQuarter', 'Full Moon', 'Next\nNew Moon'])

# Add legend and grid
# plt.legend()
plt.grid(axis='y', alpha=0.3)

# Show plot
plt.tight_layout()
plt.show()

################################## TEMP ##################################

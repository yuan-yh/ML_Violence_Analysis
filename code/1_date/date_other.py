import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ephem
import requests
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import time
from datetime import datetime
import re

# Load datasets
hospitals = ['1', '2', 'NLH', 'MHA']
dfs = {hosp: pd.read_csv(f'{hosp}.csv') for hosp in hospitals}
all_dates = pd.concat([df[['Event Date']] for df in dfs.values()])

################################## MOON ##################################
def get_moon_phase(date):
    date = ephem.Date(date)
    nnm = ephem.next_new_moon(date)
    pnm = ephem.previous_new_moon(date)
    lunation = (date - pnm) / (nnm - pnm)
    return lunation

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
def clean_date(date_input):
    """Convert various date formats to YYYY-MM-DD"""
    if pd.isna(date_input):
        return None
        
    date_str = str(date_input).strip()
    
    try:
        # Handle already properly formatted dates (YYYY-MM-DD)
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str
            
        # Handle datetime strings like "10/9/2024 8:19"
        if ' ' in date_str:
            date_str = date_str.split()[0]
            
        # Handle US format (MM/DD/YYYY)
        if re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', date_str):
            return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
            
        # Handle ISO format (YYYY-MM-DD) with possible timestamp
        if 'T' in date_str:
            return date_str.split('T')[0]
            
        # Try automatic parsing as last resort
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
        
    except Exception as e:
        print(f"Warning: Could not parse date {date_input} (Error: {str(e)})")
        return None
    
@lru_cache(maxsize=1000)
def get_weather_for_date(date_str):
    """Get weather data with robust date handling"""
    clean_date_str = clean_date(date_str)
    if not clean_date_str:
        return None
    
    lat, lon = 42.36, -71.06  # Boston
    
    try:
        # Determine API endpoint
        today = datetime.now().strftime('%Y-%m-%d')
        base_url = "https://api.open-meteo.com/v1/forecast" if clean_date_str > today else "https://archive-api.open-meteo.com/v1/archive"
        
        params = {
            'latitude': lat,
            'longitude': lon,
            'start_date': clean_date_str,
            'end_date': clean_date_str,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
            'temperature_unit': 'fahrenheit',
            'timezone': 'America/New_York'
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()['daily']
        
        return {
            'date': clean_date_str,
            'max_temp': data['temperature_2m_max'][0],
            'min_temp': data['temperature_2m_min'][0],
            'precip': data['precipitation_sum'][0]
        }
        
    except Exception as e:
        print(f"Error processing {date_str} (as {clean_date_str}): {str(e)}")
        return None

def add_weather_data(df, date_column='Event Date', max_workers=5):
    """Process DataFrame with parallel requests"""
    # Convert all dates to clean format first
    df['_clean_date'] = df[date_column].apply(clean_date)
    
    # Process unique dates in parallel
    unique_dates = [d for d in df['_clean_date'].unique() if d is not None]
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        weather_data = {}
        for date, result in zip(unique_dates, executor.map(get_weather_for_date, unique_dates)):
            weather_data[date] = result
            time.sleep(0.2)  # Rate limiting
    
    # Map results back to original rows
    df['Temperature_MAX'] = df['_clean_date'].map(lambda x: weather_data.get(x, {}).get('max_temp'))
    df['Temperature_MIN'] = df['_clean_date'].map(lambda x: weather_data.get(x, {}).get('min_temp'))
    df['Precipitation'] = df['_clean_date'].map(lambda x: weather_data.get(x, {}).get('precip'))
    
    # Clean up
    df.drop('_clean_date', axis=1, inplace=True)
    return df

all_dates = add_weather_data(all_dates)

# 
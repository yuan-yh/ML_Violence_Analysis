import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
df = pd.read_csv('0_all.csv')
df['Primary Contributing Factors'].unique()
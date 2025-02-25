import pandas as pd
import numpy as np
import random as rd
from time import time

# Start time
start_time = time()

# Import data
df = pd.read_excel(r'C:\Users\ryan\Downloads\2024 - 2025 Audition Results - to share.xlsx',
                     sheet_name='Modified Results', skiprows=[1,180], usecols='C:V')
df = df[df['Total'] != 0]
df = df.drop(['Stage Crew only', 'Total'], axis=1)
df = df.dropna(axis=0, how='all')
df = df.fillna(0)

# Setting to display full data frame no matter its size
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)










# End time
end_time = time()
total_time = end_time - start_time
print(f'Time elapsed: {total_time:.2f}')
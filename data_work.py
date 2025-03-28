import pandas as pd
import numpy as np
import random as rand
from time import time

# Start time
start_time = time()

# Import data
df = pd.read_excel(r'C:\Users\ryan\Downloads\2024 - 2025 Audition Results - to share.xlsx',
                     sheet_name='Modified Results', skiprows=[1,180], usecols='C:V')
df = df[df["Total"] != 0]
df = df.fillna(0)
df = df.drop(columns=['Total', 'Stage Crew only'])

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Create conflict matrix in an efficient way (If you can!)
acro = df[df["Acro"] != 0]
pole = df[df["Aerial Pole"] != 0]
bike = df[df["Bike"] != 0]
clowns = df[df["Clowns"] != 0]
chains = df[df["Aerial Chain"] != 0]
dance = df[df["Dance"] != 0]
wheel = df[df["German Wheel"] != 0]
wire = df[df["Highwire"] != 0]
juggling = df[df["Juggling"] != 0]
perch = df[df["Perch"] != 0]
swing = df[df["Russian Swing"] != 0]
lyra = df[df["Double Lyra"] != 0]
prop = df[df["Stoinev Atayde"] != 0]
teeter = df[df["Teeterboard/Bar"] != 0]
tumbling = df[df["Tumbling"] != 0]
unis = df[df["Unicycles"] != 0]
wall = df[df["Wall Trampoline"] != 0]


hour1 = pd.merge(tumbling, juggling, how='outer').merge(chains, how='outer')
hour1 = hour1.drop(columns=['Perch', 'Acro', 'Aerial Pole', 'Bike', 'Teeterboard/Bar', 'Dance', 'Highwire',
                         'Double Lyra', 'Stoinev Atayde', 'Clowns', 'Russian Swing', 'Unicycles', 'Wall Trampoline', 'German Wheel'])
print(hour1)

pole_conflicts = {
    "pole": sum(perch["Aerial Pole"]),
    "bike": sum(perch["Bike"]),
    "clowns": sum(perch["Clowns"]),
    "chains": sum(perch["Aerial Chain"]),
    "dance": sum(perch["Dance"]),
    "wheel": sum(perch["German Wheel"]),
    "wire": sum(perch["Highwire"]),
    "juggling": sum(perch["Juggling"]),
    # "perch": sum(clowns["Perch"]),
    "acro": sum(perch["Acro"]),
    "swing": sum(perch["Russian Swing"]),
    "lyra": sum(perch["Double Lyra"]),
    "prop": sum(perch["Stoinev Atayde"]),
    "teeter": sum(perch["Teeterboard/Bar"]),
    "tumbling": sum(perch["Tumbling"]),
    "unis": sum(perch["Unicycles"]),
    "wall": sum(perch["Wall Trampoline"]),
}
#print(pole_conflicts)

# List of available spaces to practice and dictionary for what spaces each act can practice in
spaces_list = ['Red Floor', 'Wood Floor', 'Aerial Land', 'Classroom', 'Other']
available_spaces = {
            'Acro': ['Red Floor', 'Wood Floor'],
            'Aerial Pole': ['Aerial Land'],
            'Bike': ['Wood Floor', 'Other'],
            'Clowns': ['Classroom'],
            'Aerial Chain': ['Aerial Land'],
            'Dance': ['Red Floor', 'Wood Floor', 'Other'],
            'German Wheel': ['Wood Floor'],
            'Highwire': ['Wood Floor'],
            'Juggling': ['Red Floor', 'Wood Floor'],
            'Perch': ['Classroom'],
            'Russian Swing': ['Red Floor'],
            'Double Lyra': ['Aerial Land'],
            'Stoinev Atayde': ['Classroom'],
            'Teeterboard/Bar': ['Red Floor'],
            'Tumbling': ['Red Floor', 'Wood Floor'],
            'Unicycles': ['Wood Floor', 'Other'],
            'Wall Trampoline': ['Other'],
            'None': ['Red Floor', 'Wood Floor', 'Aerial Land', 'Classroom', 'Other']
        }
available_spaces_restricted = {
            'Acro': ['Red Floor'],
            'Aerial Pole': ['Aerial Land'],
            'Bike': ['Other'],
            'Clowns': ['Classroom'],
            'Aerial Chain': ['Aerial Land'],
            'Dance': ['Other'],
            'German Wheel': ['Wood Floor'],
            'Highwire': ['Wood Floor'],
            'Juggling': ['Wood Floor'],
            'Perch': ['Classroom'],
            'Russian Swing': ['Red Floor'],
            'Double Lyra': ['Aerial Land'],
            'Stoinev Atayde': ['Classroom'],
            'Teeterboard/Bar': ['Red Floor'],
            'Tumbling': ['Red Floor'],
            'Unicycles': ['Other'],
            'Wall Trampoline': ['Other'],
            'None': ['Wood Floor', 'Aerial Land', 'Classroom']
}

# End time
end_time = time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")

#TODO: Work with classes a bit, define the schedule itself as a class and maybe even the whole algorithm as a class.
#TODO: Figure out how to generate random schedules using the schedule class that you will also make.
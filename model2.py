import numpy as np
import pandas as pd
import random as rd
import matplotlib.pyplot as plt
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

class Schedule:
    def __init__(self, acts, spaces, hours):
        self.acts = acts
        self.spaces = spaces
        self.hours = hours
        self.matrix = pd.DataFrame(index=['H1', 'H2', 'H3', 'H4'], columns=self.spaces)
        self.act_conflicts = 0
        self.hour1 = pd.DataFrame(index=['H1'], columns=self.spaces)
        self.hour2 = pd.DataFrame(index=['H2'], columns=self.spaces)
        self.hour3 = pd.DataFrame(index=['H3'], columns=self.spaces)
        self.hour4 = pd.DataFrame(index=['H4'], columns=self.spaces)


    def get_permutations(self, hour):
        ...
        #Find all permutations of an hour and save them in a list (would be nice if the function just returns a list)
        #Maybe reset the list after every step of the algorithm so I can reuse the permutations list.
        #Need to get both permutations for an hour and also permutations of the schedule as a whole for the step that I'm on in the algorithm.


    def find_best_permutation(self, hour1, hour2, hour3, hour4):
        ...
        #Check each VALID permutation of the schedule and choose the best one.


    def evaluate_schedule(self):
        ...
        #Evaluates the schedule in the same way as previous algorithm.


    def evaluate_hour(self, hour):
        ...
        #Evaluates an hour the same way as previous algorithm.



# List of available spaces to practice and dictionary for what spaces each act can practice in
spaces_list = ['Red Floor', 'Wood Floor', 'Aerial Land', 'Classroom', 'Other']
rf_acts = ['Teeterboard/Bar', 'Russian Swing', 'Acro', 'Tumbling']
wf_acts = ['German Wheel', 'Highwire', 'Juggling', 'None']
al_acts = ['Aerial Chain', 'Double Lyra', 'Aerial Pole', 'None']
cl_acts = ['Clowns', 'Stoinev Atayde', 'Perch', 'None']
oth_acts = ['Bike', 'Unicycles', 'Dance', 'Wall Trampoline']
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
print(f'Elapsed time: {elapsed_time:.4f} seconds')
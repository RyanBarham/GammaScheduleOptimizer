import numpy as np
import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from time import time
import itertools

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

class Hour:
    def __init__(self, chosen_acts, choosing_acts):
        self.chosen_acts = [chosen_acts]
        self.choosing_acts = choosing_acts
        self.permutations = []

    def set_choosing_acts(self, acts):
        self.choosing_acts = acts

    def set_chosen_acts(self, acts):
        self.chosen_acts = acts

    def get_chosen_acts(self):
        return self.chosen_acts

    def get_permutations(self):
        return self.permutations

    # Gets valid permutations between acts that have been chosen for an hour and acts to be chosen next for that hour
    def find_permutations(self):
        perm1 = self.chosen_acts + [self.choosing_acts[0]]
        perm2 = self.chosen_acts + [self.choosing_acts[1]]
        perm3 = self.chosen_acts + [self.choosing_acts[2]]
        perm4 = self.chosen_acts + [self.choosing_acts[3]]
        self.permutations = [perm1, perm2, perm3, perm4]
        return self.permutations


class Schedule:
    def __init__(self, acts, spaces, hour1, hour2, hour3, hour4):
        self.acts = acts
        self.spaces = spaces
        self.hour1 = hour1
        self.hour2 = hour2
        self.hour3 = hour3
        self.hour4 = hour4
        self.matrix = pd.DataFrame(index=['H1', 'H2', 'H3', 'H4'], columns=self.spaces)
        self.act_conflicts = 0
        self.choosing_step = 1
        # This choosing step is telling us what index of permutations we are looking through depending on what
        # step in the building of our schedule we are on.

    # Check each VALID permutation of the schedule and choose the best one.
    # This method is called after permutations of separate hours has already been obtained
    def find_best_permutation(self, hour1, hour2, hour3, hour4):
        valid_permutations = []
        conflict_scores = []
        raw_permutations = itertools.product(hour1.get_permutations(), hour2.get_permutations(), hour3.get_permutations(), hour4.get_permutations())
        for perm in raw_permutations:
            flag = check_act_uniqueness(perm, self.choosing_step)
            if flag:
                valid_permutations.append(perm)
        for permutation in valid_permutations:
            conflict_score = evaluate_schedule(permutation)
            conflict_scores.append(conflict_score)
        lowest_score_index = conflict_scores.index(min(conflict_scores))
        best_permutation = valid_permutations[lowest_score_index]
        return best_permutation

    # Method to move the algorithm on to the next step and get ready to pick acts for the next space
    def move_to_next_step(self, best_permutation):
        self.hour1 = best_permutation[0]
        self.hour2 = best_permutation[1]
        self.hour3 = best_permutation[2]
        self.hour4 = best_permutation[3]

        self.act_conflicts = evaluate_schedule(best_permutation)

        self.choosing_step += 1


# Schedule evaluation taken out of class structure since we are sending all of our permutations through it
# without defining each of them as a schedule object
def evaluate_schedule(schedule):
    hour1 = schedule[0]
    hour2 = schedule[1]
    hour3 = schedule[2]
    hour4 = schedule[3]

    hour1_conflicts = evaluate_hour(hour1)
    hour2_conflicts = evaluate_hour(hour2)
    hour3_conflicts = evaluate_hour(hour3)
    hour4_conflicts = evaluate_hour(hour4)
    total_conflicts = hour1_conflicts + hour2_conflicts + hour3_conflicts + hour4_conflicts
    return total_conflicts

# Evaluating hour with same isolated matrix method as first model
def evaluate_hour(hour):
    isolated_matrix = df.loc[:, hour]
    isolated_matrix = isolated_matrix[~(isolated_matrix == 0).all(axis=1)]
    entries_value = sum(isolated_matrix.sum())
    row_value = len(isolated_matrix.index)
    return entries_value - row_value

# Method to make sure that our valid permutations don't have any repeat acts, like teeter being on the schedule twice for example
def check_act_uniqueness(lists, index):
    seen_acts = set()
    for sub_perm in lists:
        value = sub_perm[index]
        if value in seen_acts:
            return False
        seen_acts.add(value)
    return True

# Creates schedule and hour objects, decides what spaces are choosing first and order of choosing, gets hour permutations,
# gets schedule permutations and finds best one, properly saves all data before moving on to next step until finally outputting
# the finished schedule product. Current version has red floor acts set and wood floor acts picked first
def main():
    hour1 = Hour(rf_acts[0], wf_acts)
    hour2 = Hour(rf_acts[1], wf_acts)
    hour3 = Hour(rf_acts[2], wf_acts)
    hour4 = Hour(rf_acts[3], wf_acts)

    hour1.find_permutations()
    hour2.find_permutations()
    hour3.find_permutations()
    hour4.find_permutations()

    schedule = Schedule(df.columns, spaces_list, hour1, hour2, hour3, hour4)

    schedule.move_to_next_step(schedule.find_best_permutation(hour1, hour2, hour3, hour4))

    print(schedule.act_conflicts)
    print(schedule.hour1)
    print(schedule.hour2)
    print(schedule.hour3)
    print(schedule.hour4)

    hour1.set_chosen_acts(schedule.hour1)
    hour2.set_chosen_acts(schedule.hour2)
    hour3.set_chosen_acts(schedule.hour3)
    hour4.set_chosen_acts(schedule.hour4)

    hour1.set_choosing_acts(al_acts)
    hour2.set_choosing_acts(al_acts)
    hour3.set_choosing_acts(al_acts)
    hour4.set_choosing_acts(al_acts)

    hour1.find_permutations()
    hour2.find_permutations()
    hour3.find_permutations()
    hour4.find_permutations()

    schedule.move_to_next_step(schedule.find_best_permutation(hour1, hour2, hour3, hour4))

    print(schedule.act_conflicts)
    print(schedule.hour1)
    print(schedule.hour2)
    print(schedule.hour3)
    print(schedule.hour4)

    hour1.set_chosen_acts(schedule.hour1)
    hour2.set_chosen_acts(schedule.hour2)
    hour3.set_chosen_acts(schedule.hour3)
    hour4.set_chosen_acts(schedule.hour4)

    hour1.set_choosing_acts(cl_acts)
    hour2.set_choosing_acts(cl_acts)
    hour3.set_choosing_acts(cl_acts)
    hour4.set_choosing_acts(cl_acts)

    hour1.find_permutations()
    hour2.find_permutations()
    hour3.find_permutations()
    hour4.find_permutations()

    schedule.move_to_next_step(schedule.find_best_permutation(hour1, hour2, hour3, hour4))

    print(schedule.act_conflicts)
    print(schedule.hour1)
    print(schedule.hour2)
    print(schedule.hour3)
    print(schedule.hour4)

    hour1.set_chosen_acts(schedule.hour1)
    hour2.set_chosen_acts(schedule.hour2)
    hour3.set_chosen_acts(schedule.hour3)
    hour4.set_chosen_acts(schedule.hour4)

    hour1.set_choosing_acts(oth_acts)
    hour2.set_choosing_acts(oth_acts)
    hour3.set_choosing_acts(oth_acts)
    hour4.set_choosing_acts(oth_acts)

    hour1.find_permutations()
    hour2.find_permutations()
    hour3.find_permutations()
    hour4.find_permutations()

    schedule.move_to_next_step(schedule.find_best_permutation(hour1, hour2, hour3, hour4))

    print(schedule.act_conflicts)
    print(schedule.hour1)
    print(schedule.hour2)
    print(schedule.hour3)
    print(schedule.hour4)



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

if __name__ == '__main__':
    main()

# End time
end_time = time()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.4f} seconds')
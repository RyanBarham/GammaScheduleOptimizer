import numpy as np
import pandas as pd
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

class Schedule:
    def __init__(self, acts, spaces, hours):
        self.acts = acts
        self.spaces = spaces
        self.hours = hours
        self.size = len(self.spaces) * self.hours
        self.matrix = pd.DataFrame(index=['H1', 'H2', 'H3', 'H4'], columns=self.spaces)
        self.act_conflicts = 0
        self.space_conflicts = 0
        self.acts_in_wrong_space = []

#TODO: Fix your class getter and setter stuff

    @property
    def acts(self):
        return self._acts

    @acts.setter
    def acts(self, acts):
        self._acts = acts

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, hours):
        if hours == 4:
            self._hours = int(hours)
        else:
            raise ValueError('Must be 4 hours')

    @property
    def spaces(self):
        return self._spaces

    # For now, I will just be using a number of spaces, however I would like to implement where the acts are supposed to go.
    @spaces.setter
    def spaces(self, spaces):
        if spaces == spaces_list:
            self._spaces = spaces
        else:
            raise ValueError('Must be list of eligible spaces')

    # Add more empty "acts" to the list to fully fill the matrix and generate random schedule
    def fill_acts(self):
        if len(self.acts) < self.size:
            empty_slots = self.size - len(self.acts)
            while empty_slots > 0:
                empty_act = 'None'
                self.acts = np.append(self.acts, empty_act)
                empty_slots -= 1
        rd.shuffle(self.acts)
        self.matrix = np.array(self.acts).reshape(self.hours, len(self.spaces))
        self.matrix = pd.DataFrame(self.matrix, index=['Hour1', 'Hour2', 'Hour3', 'Hour4'], columns=self.spaces)
        return self

    # Separate the schedule into its separate hours and then get the conflict scores for each hour
    def fitness(self):
        hour1 = self.matrix.iloc[0]
        hour2 = self.matrix.iloc[1]
        hour3 = self.matrix.iloc[2]
        hour4 = self.matrix.iloc[3]

        self.evaluate_hour(hour1).check_spaces(hour1)
        self.evaluate_hour(hour2).check_spaces(hour2)
        self.evaluate_hour(hour3).check_spaces(hour3)
        self.evaluate_hour(hour4).check_spaces(hour4)
        print(self.matrix)
        print(self.act_conflicts)
        print(self.space_conflicts)
        return self

    # Evaluates an hour to determine its conflict score, takes total entries in isolated matrix - rows in isolated matrix and adds that value to the conflict score
    def evaluate_hour(self, hour):
        hour_list = []
        for acts in hour:
            hour_list.append(acts)
        isolated_matrix = df.loc[:, hour_list]
        isolated_matrix = isolated_matrix[~(isolated_matrix == 0).all(axis=1)]
        entries_value = sum(isolated_matrix.sum())
        row_value = len(isolated_matrix.index)
        self.act_conflicts += entries_value - row_value
        return self

    # Function checking to see if all the acts are in the correct spaces and adds to the conflict score if they are not.
    def check_spaces(self, hour):
        column_index = 0
        for i in range(len(self.spaces)):
            act = hour.iloc[column_index]
            if self.spaces[i] not in available_spaces[act]:
                self.space_conflicts += 5
                column_index += 1
                self.acts_in_wrong_space.append(act)
            else:
                column_index += 1
        return self

    # Mutation function gets an act from a random row and random column and swaps it with an act from a different row but the same column.
    def mutate(self):
        self.act_conflicts = 0
        self.space_conflicts = 0
        rand_row1, rand_row2 = rd.sample(range(self.hours), 2)
        rand_col = rd.randint(0, (len(self.spaces)-1))
        rand_act1 = self.matrix.iat[rand_row1, rand_col]
        temp_variable = rand_act1
        rand_act2 = self.matrix.iat[rand_row2, rand_col]
        self.matrix.iat[rand_row1, rand_col] = rand_act2
        self.matrix.iat[rand_row2, rand_col] = temp_variable
        return self

    # Different mutation function that only selects acts in the wrong spaces to swap with each other
    def mutate2(self):
        random_act1, random_act2 = rd.sample(self.acts_in_wrong_space,2)
        ...

    # Remember that calling this method converts our schedule into a string, so we only print the matrix properly once we are completely done with the program
    def __str__(self):
        ...
        # use pandas .to_string()

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
sched = Schedule(df.columns, spaces_list, 4)
sched = sched.fill_acts()
sched = sched.fitness()
sched = sched.mutate()
sched = sched.fitness()



# End time
end_time = time()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.4f} seconds')

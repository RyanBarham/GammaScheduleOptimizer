import numpy as np
import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from time import time
import copy
import data_work


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

schedule_size = 20

class Schedule:
    def __init__(self, acts, spaces, hours):
        self.acts = acts
        self.spaces = spaces
        self.hours = hours
        self.matrix = pd.DataFrame(index=['H1', 'H2', 'H3', 'H4'], columns=data_work.spaces_list)
        self.act_conflicts = 0
        self.space_conflicts = 0
        self.acts_in_wrong_space = []


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
        self._hours = hours

    @property
    def spaces(self):
        return self._spaces

    @spaces.setter
    def spaces(self, spaces):
        self._spaces = spaces

    # Add more empty "acts" to the list to fully fill the matrix and generate random schedule
    def fill_acts(self):
        act_size = len(self.acts)
        if act_size < schedule_size:
            empty_slots = schedule_size - len(self.acts)
            while empty_slots > 0:
                empty_act = 'None'
                self.acts = np.append(self.acts, empty_act)
                empty_slots -= 1
        rd.shuffle(self.acts)
        self.matrix = np.array(self.acts).reshape(self.hours, len(self.spaces))
        self.matrix = pd.DataFrame(self.matrix, index=['Hour1', 'Hour2', 'Hour3', 'Hour4'], columns=self.spaces)
        return self

    # Fill acts function for restricted spaces model
    def fill_acts_correctly(self):
        act_size = len(self.acts)
        if act_size < schedule_size:
            empty_slots = schedule_size - len(self.acts)
            while empty_slots > 0:
                empty_act = 'None'
                self.acts = np.append(self.acts, empty_act)
                empty_slots -= 1
        rf_acts = []
        wf_acts = []
        al_acts = []
        cl_acts = []
        oth_acts = []
        for key, value in data_work.available_spaces_restricted.items():
            if value == ['Red Floor']:
                rf_acts.append(key)
            elif value == ['Wood Floor']:
                wf_acts.append(key)
            elif value == ['Aerial Land']:
                al_acts.append(key)
            elif value == ['Classroom']:
                cl_acts.append(key)
            elif value == ['Other']:
                oth_acts.append(key)
            else:
                executed = False
                if not executed:
                    wf_acts.append('None')
                    al_acts.append('None')
                    cl_acts.append('None')
                    executed = True
        rd.shuffle(rf_acts)
        rd.shuffle(wf_acts)
        rd.shuffle(al_acts)
        rd.shuffle(cl_acts)
        rd.shuffle(oth_acts)
        rf_df = pd.DataFrame(rf_acts)
        wf_df = pd.DataFrame(wf_acts)
        al_df = pd.DataFrame(al_acts)
        cl_df = pd.DataFrame(cl_acts)
        oth_df = pd.DataFrame(oth_acts)
        self.matrix = pd.concat([rf_df, wf_df, al_df, cl_df, oth_df], axis=1)
        return self

    # Separate the schedule into its separate hours and then get the conflict scores for each hour
    def fitness(self):
        self.act_conflicts = 0
        self.space_conflicts = 0
        hour1 = self.matrix.iloc[0]
        hour2 = self.matrix.iloc[1]
        hour3 = self.matrix.iloc[2]
        hour4 = self.matrix.iloc[3]

        self.evaluate_hour(hour1).check_spaces(hour1, 0)
        self.evaluate_hour(hour2).check_spaces(hour2, 1)
        self.evaluate_hour(hour3).check_spaces(hour3, 2)
        self.evaluate_hour(hour4).check_spaces(hour4, 3)
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
    def check_spaces(self, hour, hour_index):
        column_index = 0
        for i in range(len(self.spaces)-1):
            act = hour.iloc[column_index]
            if self.spaces[i] not in data_work.available_spaces_restricted[act]:
                self.space_conflicts += 5
                column_index += 1
                self.acts_in_wrong_space.append([column_index, hour_index])
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
        if len(self.acts_in_wrong_space) >= 2:
            self.act_conflicts = 0
            self.space_conflicts = 0
            column_index1, row_index1 = self.acts_in_wrong_space[0]
            column_index2, row_index2 = self.acts_in_wrong_space[1]
            act1 = self.matrix.iat[row_index1, column_index1]
            act2 = self.matrix.iat[row_index2, column_index2]
            temp_variable = act1
            self.matrix.iat[row_index1, column_index1] = act2
            self.matrix.iat[row_index2, column_index2] = temp_variable
            del self.acts_in_wrong_space[0:2]
            return self



# Fixing mutation function so that it can only make the schedule better even if it is still random
def mutation(schedule):
    original_schedule = schedule
    new_schedule = schedule.mutate()
    new_schedule.fitness()
    original_conflict_score = original_schedule.act_conflicts + original_schedule.space_conflicts
    new_conflict_score = new_schedule.act_conflicts + new_schedule.space_conflicts
    if new_conflict_score < original_conflict_score:
        return new_schedule
    else:
        return original_schedule

# Function to create generation of schedule
def create_generation():
    schedules_in_generation = 20
    generation = [Schedule(df.columns, data_work.spaces_list, 4) for i in range(schedules_in_generation)]
    for obj in generation:
        obj.fill_acts_correctly()
        obj.fitness()
    for i in range(len(hall_of_fame)):
        copy_schedule = Schedule(df.columns, data_work.spaces_list, 4)
        copy_schedule.matrix = hall_of_fame[i].matrix
        copy_schedule.fitness()
        generation.append(copy_schedule)
    for j in generation:
        data = j.act_conflicts
        raw_data.append(data)
    best_schedule = min(generation, key=lambda obj: obj.act_conflicts)
    mutation(best_schedule)
    best_schedule.fitness()
    hall_of_fame.append(best_schedule)
    hall_of_fame_scores.append(best_schedule.act_conflicts)


# Main function that runs the algorithm
def main():
    number_of_generations = 50
    create_generation()
    for i in range(number_of_generations-1):
        create_generation()
    best_schedule_index = hall_of_fame_scores.index(min(hall_of_fame_scores))
    best_schedule = hall_of_fame[best_schedule_index]
    final_data = pd.DataFrame(raw_data)
    print(best_schedule.matrix)
    print(f'Act conflicts for best schedule: {best_schedule.act_conflicts}')
    print(f'Space conflicts for best schedule: {best_schedule.space_conflicts}')
    print(f'List of best conflict scores: {hall_of_fame_scores}')
    print(f'Standard Deviation: ', final_data.std())
    print(f'Average: ', final_data.mean())
    print(f'Minimum value: ', final_data.min())
    print(f'Maximum value: ', final_data.max())
    #scatter_plot(hall_of_fame_index, hall_of_fame_best)


# Function to make a scatter plot from our data
def scatter_plot(x, y):
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set(xlim=(0, 50), xticks=np.arange(1, 50),
           ylim=(0, 50), yticks=np.arange(1, 50))
    plt.show()



# List of the best schedules
hall_of_fame = []
hall_of_fame_scores = []
hall_of_fame_best = []
hall_of_fame_index = []
raw_data = []

if __name__ == '__main__':
    main()

# End time
end_time = time()
elapsed_time = end_time - start_time
print(f'Elapsed time: {elapsed_time:.4f} seconds')

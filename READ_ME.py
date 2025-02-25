# Author - Ryan Barham
# Created in the Spring Semester of 2025

# This is a program that will create an optimal schedule for the use of the Gamma Phi Circus at Illinois State University.
# Our practice facility has 5 different available spaces that different acts are able to practice in,
# so we are able to have 5 acts practicing at the same time. Practices last for 4 hours so we break the schedule into 4 separate hours
# to be able to fit every act into the practice schedule. Usually there are between 15-20 acts in a year, this year there are 17 acts.
# We want to optimize our schedule so that every act is practicing in an available space that works for them in our facility,
# and so that we don't cause conflicts between the people in the acts. Each member of the Gamma Phi Circus can be in up to 5 acts
# and there are currently 150 members. As you could expect this causes a lot of problems when some of our members need to be in
# two places at once if two of their acts are practicing during the same hour, so we would like to avoid this as well.
# the goal of this program is two make a schedule that minimizes these space and act conflicts and makes a schedule that works for all of us.

# My first algorithm I built to tackle this problem is a genetic algorithm. The algorithm generates x random schedules,
# evaluates how many conflicts each schedule has in that first generation, and chooses the best schedule out of our first x schedules.
# We then mutate the best schedules to make them even better, swapping around acts that are causing problems for the schedule,
# and then we keep that schedule around while introducing a new generation of x random schedules. This process continues as the best
# of the best are chosen until we end up with a schedule with a low enough conflict score.

# NOTE: at the time of writing this READ_ME file, my algorithm is not yet built. I think that I have my class structure and class functions
# in a good place (except for my mutation function which I will be visiting later) and I will start building my actual main algorithm today.
# Another thing I would like to implement is a function to find the best permutation of a schedule, for example if I have a schedule
# with a low act conflict score but a high space conflict score I would like to keep that schedule since that act conflicts are so low,
# and I would like to be able to find the permutation of that schedule that puts all the acts into the correct spaces
# for where they should be in for that hour.
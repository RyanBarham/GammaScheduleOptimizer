Author - Ryan Barham
Created in the Spring Semester of 2025

This is a program that will create an optimal schedule for the use of the Gamma Phi Circus at Illinois State University.
Our practice facility has 5 different available spaces that different acts are able to practice in, 
so we are able to have 5 acts practicing at the same time. Practices last for 4 hours so we break the schedule into 4 separate hours
to be able to fit every act into the practice schedule. Usually there are between 15-20 acts in a year, this year there are 17 acts.
We want to optimize our schedule so that every act is practicing in an available space that works for them in our facility,
and so that we don't cause conflicts between the people in the acts. Each member of the Gamma Phi Circus can be in up to 5 acts
and there are currently 150 members. As you could expect this causes a lot of problems when some of our members need to be in
two places at once if two of their acts are practicing during the same hour, so we would like to avoid this.
the goal of this program is two make a schedule that minimizes these space and act conflicts and makes a schedule that works for all of us.

My first algorithm I built to tackle this problem is a genetic algorithm. The algorithm generates x random schedules,
evaluates how many conflicts each schedule has in that first generation, and chooses the best schedule out of our first x schedules.
We then mutate the best schedules to make them even better, swapping around acts that are causing problems for the schedule,
and then we keep that schedule around while introducing a new generation of x random schedules. This process continues as the best
of the best are chosen until we end up with a schedule with a low enough conflict score.

UPDATE on 3/28: My genetic algorithm is finished for the most part. There are a lot of things that I want to change about it to make it better,
however for this project I am also making an integer programming model for the same task and I really need to get working on that! 
There are a lot of small problems with the algorithm that are not optimized or as clean as they should be, but my biggest issue with it
is my function I have been using to select the schedules with the lowest conflict scores. You can see this function at line 255, 270, and 
277 in my code. It is supposed to be taking the schedule with the lowest act conflict score from a list of other schedules, however you 
can see from the graphs my algorithm is producing that the function is not doing this.

As for my integer programming model, I have a few ideas but the model is not yet built at all. I was thinking that since restricting
each act to one space worked so well in my last model, I could do the same in my second model and possibly just check all permutations 
in order to build an optimal schedule by seeing which sets of permutations lead to the lowest scores, since it is now feasible to do so
with a restricted space approach. It will be very important if I decide to go this route that I find a replacement for the function I was
talking about earlier so that I can find the actual lowest conflict scores.
from collections import defaultdict
import random
import time
import numpy as np

from population import Population
from visualizer import Visualizer
from disaster import Disaster
from person import Person
from food import Food
from facility import Facility

class Driver(object):
    def __init__(self, vis=False):
        if vis:
            series = ('Population', 'Mcals')
            self.vis = Visualizer(log=True, series=series)

    def drive(self):

        # initial inputs
        random.seed(0) #seed the random number generator
        death_dict = defaultdict(list)
        people_born = {k: 0 for k in range(9)}
        people_born[0] = 50 # initial population
        max_sim_time = 10 # max number of iterations
        population = Population()
        disaster = Disaster(population)
        facility = Facility(10000, 60) #allen/matt: update #'s to be w/e you want, I did this for testing

        for indx, cur_sim_time in enumerate(range(max_sim_time)):
            print 'current sim time:', cur_sim_time
            start = time.time()

            if random.random() <= 0.01:
                ratio = random.random()/4.0
                disaster.create_disaster(ratio)
                print 'DISASTER killed', ratio, 'in:', time.time() - start
                start = time.time()

            # Adding newborns
            for add_count in range (people_born.get(cur_sim_time % 9, 0)):
                population.add_person(Person(cur_sim_time, population.get_rand_death_time(cur_sim_time), random.random()))
            print 'added', people_born.get(cur_sim_time % 9, 0), 'people in', time.time()-start

            # Removing the dead
            start = time.time()
            population.remove_dead(cur_sim_time)
            print 'removed', len(population.death_dict.get(cur_sim_time, [])), 'people in:', time.time() - start

            # Calculating total kcal
            start = time.time()
            total_kcal = population.kcal_requirements(cur_sim_time)
            print 'completed total kcal in:', time.time() - start
            
            # Food initialization/production
            if cur_sim_time == 0:
                foodie = Food(facility, total_kcal)
            else:
                foodie.calculate_food_production()
            foodie.remaining_food = foodie.produced_food - total_kcal #NOTE: INTEGRATE BETTER FOOD CONSUMPTION MODEL HERE
            print 'produced food = ', foodie.produced_food, '; remaining food = ', foodie.remaining_food

            # Calculating how many newborns to be created in 9 months time
            num_people = population.num_people()
            people_born[cur_sim_time % 9] = random.randint(int(num_people*0.01), int(num_people*0.05))
            print 'total people:', num_people, 'and total kcal:', total_kcal

            print('-'*100)

            if indx % 10 == 0:
                self.vis.add_data(indx, { 'Population': num_people, 'Mcals': total_kcal / 1000.0 })
                self.vis.update()

driver = Driver(vis=True)
driver.drive()
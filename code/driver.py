from collections import defaultdict
import random
import time
import numpy as np

from population import Population
from visualizer import Visualizer
from disaster import Disaster
from person import Person

class Driver(object):
    def __init__(self, vis=False):
        """
        Creates a new Driver.

        Args:
            vis: Boolean. Whether or not to show visualization of the simulation
                 runs using matplotlib.

        Returns:
            A new Driver instance.

        """

        # If visualization is selected, show it.
        if vis:
            series = ('Population', 'Mcals')
            self.vis = Visualizer(log=True, series=series)

    def drive(self,
              max_iterations=500,
              random_seed=0,
              initial_pop=50):
        """
        Args:
            max_iterations: Integer. The maximum number of iterations the
                            simulation should run.
            random_seed: Integer. Seed for the random number generator.
            initial_pop: Integer. The initial population for the population.

        Returns:
            None.

        """

        # Seed the random number generator.
        random.seed(random_seed)

        # Create a dictionary that will hold the number of newborns that will
        # be added to the simulation.
        people_born = { k: 0 for k in range(9) }
        people_born[0] = initial_pop

        # Set the maximum number of iterations that the simulation will run.
        max_sim_time = max_iterations

        # Initialize a population.
        population = Population()

        # Create a disaster object for the population - this models uncertainty
        # events that may adversely affect the population.
        disaster = Disaster(population)

        for cur_sim_time in range(max_sim_time):
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

            # Calculating how many newborns to be created in 9 months time
            num_people = population.num_people()
            people_born[cur_sim_time % 9] = random.randint(int(num_people*0.01), int(num_people*0.05))
            print 'total people:', num_people, 'and total kcal:', total_kcal

            print('-'*100)

            if cur_sim_time % 10 == 0:
                self.vis.add_data(cur_sim_time, { 'Population': num_people, 'Mcals': total_kcal / 1000.0 })
                self.vis.update()

        return None

driver = Driver(vis=True)
driver.drive()
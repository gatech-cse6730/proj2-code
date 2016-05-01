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
            series = ('Population', 'Adults', 'Mcals', 'Food')
            self.vis = Visualizer(log_scale=True, series=series)

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

        # Dictionary to keep track of results
        results = defaultdict(list)

        # Seed the random number generator.
        random.seed(random_seed)

        # Create a dictionary that will hold the number of newborns that will
        # be added to the simulation.
        people_born = { k: 0 for k in range(9) }

        # Set the maximum number of iterations that the simulation will run.
        max_sim_time = max_iterations

        # Initialize a population.
        population = Population()

        # Initial Iteration
        cur_sim_time = 0
        start = time.time()

        # Add initial population
        initial_ages = [10, 18, 20, 25, 28, 30, 32, 35, 40, 45, 50, 55]
        for add_count in range (initial_pop):
            init_age = cur_sim_time - initial_ages[add_count % len(initial_ages)]*12.0
            population.add_person(Person(init_age, population.get_rand_death_time(cur_sim_time), random.random()))
        print 'added', people_born.get(cur_sim_time % 9, 0), 'people in', time.time()-start

        start = time.time()
        total_kcal = population.kcal_requirements(cur_sim_time)
        print 'completed total kcal in:', time.time() - start

        # Create a facility for population
        # Crop area of 25000 feeds about 30 people
        facility = Facility(30000.0/30.0*(initial_pop+30), initial_pop+30)

        # Food initialization
        food = Food(facility, total_kcal)

        # Create a disaster object for the population - this models uncertainty
        # events that may adversely affect the population & food
        disaster = Disaster(population, food)

        # Write initial loop results
        results["population"].append(population.num_people())
        results["food"].append(food.produced_food)
        results["kcals"].append(total_kcal)
        results["facility_crop"].append(facility.crop_area)
        results["facility_personnel"].append(facility.personnel_capacity)

        # Main iteration loop
        for cur_sim_time in range(1, max_sim_time):
            print 'current sim time:', cur_sim_time
            start = time.time()

            # Diasters
            if random.random() <= 0.01:
                #ratio = random.random()/10.0
                #disaster.create_disaster(ratio)
                #print 'DISASTER killed', ratio, 'in:', time.time() - start
                death_from_disaster = random.randint(1,20)
                disaster.create_disaster(death_from_disaster)
                print 'DISASTER killed', death_from_disaster, 'people and', (death_from_disaster+10)*2500.0, 'food in:', time.time() - start
                start = time.time()

            # If enough food, expand facility. Assume 3 month build time
            if food.remaining_food > 2500*10 and (facility.personnel_capacity - population.num_people()) <= 10:
                facility.start_pod_construction(cur_sim_time, 3)
                facility.add_pod(cur_sim_time)

            # Adding newborns
            born_count = 0
            for add_count in range (people_born.get(cur_sim_time % 9, 0)):
                if population.num_people() < facility.personnel_capacity:
                    population.add_person(Person(cur_sim_time, population.get_rand_death_time(cur_sim_time), random.random()))
                    born_count += 1
            print 'added', born_count, 'people in', time.time()-start

            # Removing the dead
            start = time.time()
            people_to_kill = len(population.death_dict.get(cur_sim_time, []))
            population.remove_dead(cur_sim_time)
            print 'removed', people_to_kill, 'people in:', time.time() - start

            # Calculating total kcal
            start = time.time()
            total_kcal = population.kcal_requirements(cur_sim_time)
            print 'completed total kcal in:', time.time() - start

            # Food consumption
            food_delta = food.update_food(total_kcal)
            print 'produced food = ', food.produced_food, '; remaining food = ', food.remaining_food
            # if not enough food
            if food_delta < 0:
                # people who are unfed will die, starting with oldest people
                while (food_delta < 0):
                    food_delta = food_delta + population.people[0].kcal_requirements(cur_sim_time)
                    population.remove_person(0)
                population.generate_death_dict()

            # Calculating how many newborns to be created in 9 months time
            num_people = population.num_people()
            num_adults = population.num_adults(cur_sim_time)
            # newborns based on number of adults. Average US birthrate in 2014: 0.01342 (indexmundi.com)
            people_born[cur_sim_time % 9] = random.randint(int(num_adults*0.01), 1 if num_adults*0.020 >= 0.5 else 0)
            print 'total people:', num_people, 'and total adults:', num_adults, 'and total kcal:', total_kcal
            print 'total capacity:', facility.personnel_capacity

            print('-'*100)

            # record results
            results["population"].append(num_people)
            results["food"].append(food.produced_food)
            results["kcals"].append(total_kcal)
            results["facility_crop"].append(facility.crop_area)
            results["facility_personnel"].append(facility.personnel_capacity)

            # visualization
            if cur_sim_time % 10 == 0:
                self.vis.add_data(cur_sim_time, { 'Population': num_people, 'Adults': num_adults, 'Mcals': total_kcal / 1000.0, 'Food': food.produced_food / 1000.0})
                self.vis.update()

        return results

if __name__ == '__main__':
    driver = Driver(vis=True)
    driver.drive(max_iterations=1000,random_seed=0,initial_pop=50)

from collections import defaultdict
import random
import time
import numpy as np

from population import Population
from visualizer import Visualizer
from facility import Facility
from disaster import Disaster
from power import Power
from person import Person
from food import Food
from air import Air

class Driver(object):
    def __init__(self, vis=False):
        """
        Creates a new Driver.

        Args:
            vis: <Boolean>. Flag to show visualization of the simulation
                 runs using matplotlib.

        Returns:
            A new Driver instance.
        """

        self.vis = vis

        # If visualization is selected, show it.
        if self.vis:
            self.vis = Visualizer()

    def drive(self,
              max_iterations=500,
              random_seed=0,
              initial_pop=50,
              food_storage=False):
        """
        Main driver function to run the simulation.

        Args:
            max_iterations: <Integer>. The maximum number of iterations the
                            simulation should run.
            random_seed: <Integer>. Seed for the random number generator.
            initial_pop: <Integer>. The initial population for the population.
            food_storage: <Boolean>. Flag to allow storing excess produced food
                          for use in future iterations.

        Returns:
            None.
        """

        # Dictionary to keep track of results
        self.results = defaultdict(list)

        # Seed the random number generator.
        random.seed(random_seed)

        # Create a dictionary that will hold the number of newborns that will
        # be added to the simulation.
        people_born = { k: 0 for k in range(9) }

        # Set the maximum number of iterations that the simulation will run.
        max_sim_time = max_iterations

        # Initialize a population.
        population = Population()

        # Initialize an air instance for modeling oxygen consumption.
        air = Air(population)

        # Initialize a power instance for modeling power consumption.
        power = Power(population)

        # Initial Iteration
        cur_sim_time = 0

        # Add initial population
        # Ages of initial population
        initial_ages = [10, 18, 20, 25, 28, 30, 32, 35, 40, 45, 50, 55]
        for add_count in range (initial_pop):
            init_age = cur_sim_time - initial_ages[add_count % len(initial_ages)]*12.0
            population.add_person(Person(init_age, population.get_rand_death_time(cur_sim_time), random.random()))

        total_kcal = population.kcal_requirements(cur_sim_time)

        # Create a facility for the population.
        initial_crop_area = (2.5 * total_kcal) / 127.9579417
        facility = Facility(initial_crop_area, initial_pop+30)

        # Food initialization
        food = Food(facility, total_kcal, food_storage=food_storage)

        # Create a disaster object for the population - this models uncertainty
        # events that may adversely affect the population & food
        disaster = Disaster(population, food)

        # Write initial loop results
        self._write_results(population=population.num_people(),
                            food=food.produced_food,
                            kcals=total_kcal,
                            adults=population.num_adults(cur_sim_time),
                            facility_crop=facility.crop_area,
                            facility_personnel=facility.personnel_capacity,
                            air=air.oxygen_consumed(),
                            power=power.power_consumed())

        # Main iteration loop
        for cur_sim_time in range(1, max_sim_time):
            print 'current sim time:', cur_sim_time

            # Disasters
            if random.random() <= 0.01:
                death_from_disaster = random.randint(1,20)
                disaster.create_disaster(death_from_disaster)

            # If enough food and personnel capacity being reached, expand facility.
            # Assume 3 month build time.
            if food.remaining_food > 2500*10 and (facility.personnel_capacity - population.num_people()) <= 10:
                facility.start_pod_construction(cur_sim_time, 3)
                facility.add_pod(cur_sim_time)

            # Adding newborns
            born_count = 0
            for add_count in range (people_born.get(cur_sim_time % 9, 0)):
                if population.num_people() < facility.personnel_capacity:
                    population.add_person(Person(cur_sim_time, population.get_rand_death_time(cur_sim_time), random.random()))
                    born_count += 1

            # Removing the dead
            people_to_kill = len(population.death_dict.get(cur_sim_time, []))
            population.remove_dead(cur_sim_time)

            # Calculating total kcal
            total_kcal = population.kcal_requirements(cur_sim_time)

            # Food consumption
            food_delta = food.update_food(total_kcal)

            # If not enough food
            if food_delta < 0:
                # People who are unfed will die, starting with oldest people
                while (food_delta < 0):
                    food_delta = food_delta + population.people[0].kcal_requirements(cur_sim_time)
                    population.remove_person(0)
                population.generate_death_dict()

            # Calculating how many newborns to be created in 9 months time
            num_people = population.num_people()
            num_adults = population.num_adults(cur_sim_time)

            # Number of newborns is based on number of adults between 18-55.
            # Average US birthrate in 2014: 0.01342 (indexmundi.com)
            people_born[cur_sim_time % 9] = random.randint(np.rint(num_adults*0.01),np.rint(num_adults*0.020))

            # Record results of the iteration.
            self._write_results(population=num_people,
                                food=food.produced_food,
                                kcals=total_kcal,
                                adults=num_adults,
                                facility_crop=facility.crop_area,
                                facility_personnel=facility.personnel_capacity,
                                air=air.oxygen_consumed(),
                                power=power.power_consumed())

            # If the visualization option has been selected, plot the results
            # every 10 timesteps.
            if self.vis and cur_sim_time % 10 == 0:

                # Add data for the chart.
                self.vis.add_data(cur_sim_time, {
                    'Population Count': num_people,
                    'Adult Count': num_adults,
                    'Caloric Requirements (Mcal)': total_kcal / 1000.0,
                    'Produced Food (Mcal)': food.produced_food / 1000.0,
                    'Air (kg O2)': air.oxygen_consumed(),
                    'Power Consumption (kWh)': power.power_consumed()
                })

                # Update the chart, re-rendering.
                self.vis.update()

        # If visualization has been selected,
        if self.vis:
            # Save the last rendered chart as a png image.
            self.vis.savefig()

        # Return the results dict.
        return self.results

    # Private
    def _write_results(self,
                       population=0,
                       food=0,
                       kcals=0,
                       adults=0,
                       facility_crop=0,
                       facility_personnel=0,
                       air=0,
                       power=0):
        """ Writes the results of the simulation to a dictionary. """

        self.results['population'].append(population)
        self.results['food'].append(food)
        self.results['kcals'].append(kcals)
        self.results['adults'].append(adults)
        self.results['facility_crop'].append(facility_crop)
        self.results['facility_personnel'].append(facility_personnel)
        self.results['air'].append(air)
        self.results['power'].append(power)

if __name__ == '__main__':
    driver = Driver(vis=True)
    driver.drive(max_iterations=1500,random_seed=0,initial_pop=50,food_storage=False)

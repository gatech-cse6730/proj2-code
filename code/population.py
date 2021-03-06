from collections import defaultdict
import numpy as np
import random

class Population(object):
    """
    The Population class is used for modeling aggregate-level
    phenomena relevant to the entire population of Person
    instances for a particular simulation run.
    """

    def __init__(self, people=[]):
        """
        Creates a new Population.

        Args:
            people: <List>. A list of <Person> instances that will comprise the
                    population.

        Returns:
            A new Population instance.
        """

        self.people = people
        self.death_age_dist = self.init_death_age_dist()
        self.death_age_dist_len = len(self.death_age_dist)-1
        self.death_dict = defaultdict(list)

        if len(self.people) > 0:
            self.generate_death_dict()

    def generate_death_dict(self):
        """
        Generates a new dictionary of death ages based on current
        list of People in the Population.

        Args:
            None.

        Returns:
            <Boolean> True.
        """

        self.death_dict = defaultdict(list)
        for i in range(self.num_people()):
            self.death_dict[self.people[i].death_age].append(i)
        return True

    def init_death_age_dist(self, filename='data/death_age_dist.txt'):
        """
        Creates a distribution for generating random death ages as a list
        based on a death age distribution text file
        Death distribution text file generated from simplified distribution
        from 2007 death age distribution http://www.cdc.gov/nchs/nvss/mortality/gmwk310.htm

        Args:
            filename: <String>. A filename to read death distribution from.

        Returns:
            <List>. Distribution of death age as a list.
        """

        age = 1
        death_age_dist = []
        for line in open(filename):
            death_age_dist.extend([age for i in range(int(line.rstrip('\n')))])
            age += 1

        return death_age_dist

    def get_rand_death_time(self, sim_time):
        """
        Generates a random death age in simulation time based on death
        age distribution.

        Args:
            sim_time: <Integer>. Current simulation iteration.

        Returns:
            <Integer>. Simulation iteration number to die at.
        """

        return self.death_age_dist[random.randint(0,self.death_age_dist_len)]*12.0 + sim_time

    def add_person(self, person):
        """
        Adds a new person to the population.

        Args:
            person: <Person>. Person instance to add to the Population.

        Returns:
            <Boolean> True.
        """

        self.people.append(person)
        self.death_dict[person.death_age].append(self.num_people()-1)

        return True

    def remove_person(self, index):
        """
        Removes a person from the population given an index.

        Args:
            index: <Integer>. Index in people list of the Population to remove.

        Returns:
            <Boolean> True.
        """

        del self.people[index]

        return True

    def remove_dead(self, sim_time):
        """
        Removes all people from the population whose death age is the
        given sim time.

        Args:
            sim_time: <Integer>. Current simulation iteration.

        Returns:
            <Boolean> True.
        """

        for death_index in reversed(self.death_dict.get(sim_time, [])):
            del self.people[death_index]
        # Need to regenerate death dict every time due to index issues
        self.generate_death_dict()
        return True

    def num_people(self):
        """
        Returns the current number of people in the population.

        Args:
            None.

        Returns:
            <Integer> Number of people in the Population.
        """

        return (len(self.people))

    def kcal_requirements(self, sim_time):
        """
        Returns the aggregate monthly kcal requirements for the entire population.

        Args:
            sim_time: <Integer>. Current simulation iteration.

        Returns:
            <Integer> Total Kcal requirements of the Population.
        """

        return np.sum([person.kcal_requirements(sim_time) for person in self.people])

    def num_adults(self, sim_time):
        """
        Returns the number of people between the ages of 18 and 50.

        Args:
            sim_time: <Integer>. Current simulation iteration.

        Returns:
            <Integer> Number of adults between the ages of 18-50 in the Population.
        """

        within_age = lambda age: age >= 18 and age <= 50
        return np.sum([1 if within_age(person.current_age(sim_time)) else 0 for person in self.people])

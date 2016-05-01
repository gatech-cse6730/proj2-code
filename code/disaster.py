import random

class Disaster(object):
    """
    The Disaster class is used for modeling natural disasters that affects a
    Population instance by destroying Person instances and resources.
    """

    def __init__(self, population, food):
        """
        Creates a new Disaster.

        Args:
            population: A <Population> instance that will
                be affected by the disaster.

        Returns:
            A new Disaster instance.
        """

        self.population = population
        self.food = food

    def create_disaster(self, num_people_to_die):
        """
        Create a disaster that destroys the given number of people in the
        population and chooses people randomly to kill within the population.
        Also destroys remaining food to feed given number of people plus ten
        additional people.
        """

        max_index = self.population.num_people()-1

        if max_index+1 < num_people_to_die:
            num_people_to_die = max_index+1

        for i in range(num_people_to_die):
            self.population.remove_person(random.randint(0,max_index))
            max_index -= 1

        # this regeneration of the death dict makes it slow (90 sec for 200k deaths for population of 1mil)
        self.population.generate_death_dict()

        self.food.remaining_food = self.food.remaining_food - (num_people_to_die+10)*2500.0

        return True

    def create_disaster_ratio(self, ratio):
        """
        Create a disaster that destroys the given ratio of the population
        and chooses people randomly to kill within the population.
        """

        max_index = self.population.num_people()-1
        for i in range(int(self.population.num_people()*ratio)):
            self.population.remove_person(random.randint(0,max_index))
            max_index -= 1

        # this regeneration of the death dict makes it slow (90 sec for 200k deaths for population of 1mil)
        self.population.generate_death_dict()

        self.food.remaining_food = self.food.remaining_food * ratio

        return True

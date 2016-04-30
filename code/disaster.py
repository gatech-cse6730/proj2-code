import random

class Disaster(object):
    """
    The Disaster class is used for modeling natural disasters that affects a
    Population instance by destroying Person instances and resources.
    """

    def __init__(self, population):
        """
        Creates a new Disaster.

        Args:
            population: A <Population> instance that will
                        be affected by the disaster.

        Returns:
            A new Disaster instance.
        """

        self.population = population

    def create_disaster(self, ratio):
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

        return True
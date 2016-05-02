class Air(object):
    """
    The Air class is used for modeling air.

    """

    OXYGEN_PER_HUMAN_PER_MONTH = 25.55

    def __init__(self, population):
        """
        Creates a new Air instance.

        Args:
            population: <Population>. Population instance to consider when
                computing consumption information.

        Returns:
            A new Air instance.

        """

        self.population = population


    def oxygen_consumed(self):
        """
        Returns the oxygen consumed by the population this timestep.

        Args:
            None.

        Returns:
            Float. Oxygen consumed in a month (kg).

        """

        return self.population.num_people() * self.OXYGEN_PER_HUMAN_PER_MONTH
class Power(object):
    """
    The Power class is used for modeling power.

    """

    PER_CAPITA_CONSUMPTION = 12985

    def __init__(self, population):
        """
        Creates a new Power instance.

        Args:
            population: <Population>. Population instance to consider when
                computing consumption information.

        Returns:
            A new Power instance.

        """

        self.population = population


    def power_consumed(self):
        """
        Returns the power consumed by the population this timestep.

        Args:
            None.

        Returns:
            Float. Power consumed in a month (kWh).

        """

        return self.population.num_people() * self.PER_CAPITA_CONSUMPTION / 12.0
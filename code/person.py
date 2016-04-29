class Person(object):
    """
    The Person class is used for modeling an individual
    human instance in the simulation.

    """

    def __init__(self, birthday, death_age, gender):
        """
        Creates a new Person.

        Args:
            birthday: Integer. Birth moment of the person, in a
                      number of simulation timesteps.
            death_age: Integer. Simulation timestep that the person will die at
            gender: String. Sex of the person: must be one of 'm',
                    or 'f'.

        Returns:
            A new Person instance.

        """

        self.birthday = birthday
        self.death_age = death_age
        self.gender = 'f' if gender < 0.5 else 'm'

    def current_age(self, sim_time):
        """
        Computes the current age of the person in years from the current
        simulation time (as an integer number of timesteps). Assumes each
        timestep corresponds to one month.

        """

        return (sim_time - self.birthday) / 12.0

    def kcal_requirements(self, sim_time):
        """
        Computes the monthly kcal intake requirements for the person.
        Depends on age and gender.

        Returns the number of kcals as an integer.

        """

        # Find the current age of the person.
        age = self.current_age(sim_time)

        # Initialize our kcals.
        kcals = None

        if age <= 1:
            kcals = 820
        elif age <= 3:
            kcals = 1350
        elif age <= 5:
            kcals = 1550
        else:
            if self.gender == 'm':
                if age <= 7:
                    kcals = 1850
                elif age <= 10:
                    kcals = 2100
                elif age <= 12:
                    kcals = 2200
                elif age <= 14:
                    kcals = 2400
                elif age <= 16:
                    kcals = 2650
                elif age <= 18:
                    kcals = 2850
                else:
                    kcals = 3050
            elif self.gender == 'f':
                if age <= 7:
                    kcals = 1750
                elif age <= 10:
                    kcals = 1800
                elif age <= 12:
                    kcals = 1950
                elif age <= 14:
                    kcals = 2100
                elif age <= 16:
                    kcals = 2150
                elif age <= 18:
                    kcals = 2150
                else:
                    kcals = 2350
            else:
                raise Exception('Person does not have a gender.')

        # Return the number of kcals required.
        return (kcals * 365) / 12.0
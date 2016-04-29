import numpy as np

class Food(object):
    """
    The Food class is used for generically modeling food (which in
    this case entails both solid food and water) in an aggregate
    way for the population. Food is a finite resource that can be
    requested by individual <Person> instances.

    """

    def __init__(self, facility, population, sim_time):
        """
        Creates a new Food instance.

        Args:
            facility: Facility. Facility instance that is supporting
                      the growing of the food.
            population: Population. Instance of the population class
                        that is consuming food.

        Returns:
            A new Food instance.

        """

        self.facility                  = facility
        self.population                = population
        self.F_r                       = 2.0 # number of replications (ie stories) in food growing area
        self.alpha                     = 54492.7 * 0.00001 * 365.0 / 12.0 * 3.86 * self.F_r * self.facility.crop_area
        self.beta                      = 200.0
        self.gamma                     = 5.43E-3
        self.crop_energy_protein_ratio = 2150 / 46 * 1000
        self.crop_energy_to_food_mass  = 3.2747E-4
        self.remaining_food            = 0.0
        self.previous_f                = 0.0
        self.previous_e_dot_pop        = 0.0
        self.previous_sim_time         = 0.0


        # Initialize the amount food production.
        self.initialize_food_production(sim_time)

    def initialize_food_production(self, sim_time):
        """
        Initializes food production based on the crop area
        available for crop production.

        """

        crop_area = self.facility.crop_area

        # get population's food requirements
        e_dot_pop = self.population.kcal_requirements(sim_time)

        # make sure a maxed out crop can feed the population's needs
        if e_dot_pop > self.alpha:
            self.remaining_food = 0.0
            raise Exception('Not enough food production capability for initial population.')
            return

        # compute initial fertilization
        self.previous_f = -1.0 / self.beta * np.log(1.0 - e_dot_pop / self.alpha)

        # save other previous step data
        self.remaining_food     = e_dot_pop
        self.previous_e_dot_pop = e_dot_pop
        self.previous_sim_time  = sim_time

        print(self.remaining_food)

    def reset_food_production(self, sim_time):
        """
        Resets the food production (*remaining_food* attribute).
        Used for resetting the amount of food available after the
        completion of each timestep.

        """

        self.initialize_food_production(sim_time)

    def calculate_food_production(self, sim_time):
        """
        Calculates the amount of food produced in a time step;
        call after updating population so that calorie needs
        are correct
        """

        delta_t = sim_time - previous_sim_time

        # get population calorie needs
        e_dot_pop = self.population.kcal_requirements(sim_time)

        # compute soil reconstitution parameter
        xi_1 = 0.22 * self.previous_e_dot_pop / (self.F_r * self.facility.crop_area * self.crop_energy_protein_ratio)

        # compute soil fertilization density derivative
        soil_f_dot = xi_1 - (self.gamma * self.crop_energy_to_food_mass * self.alpha *
                             (1.0 - np.exp(-self.beta * self.previous_f)) / (self.F_r * self.facility.crop_area))
        soil_f = self.previous_f + delta_t * soil_f_dot

        # compute food output
        self.remaining_food = alpha * (1.0 - np.exp(-self.beta * soil_f))

        print(self.remaining_food)

        # save state
        self.previous_f         = soil_f
        self.previous_e_dot_pop = e_dot_pop
        self.previous_sim_time  = sim_time

    def request_food(self, amount):
        """
        Allows a <Person> instance to request food.

        Returns true if enough food exists; else, returns false.
        """

        # If enough food remains, deduct the requested amount and
        # grant the request.
        if self.remaining_food >= amount:
            self.remaining_food -= amount

            return True
        # Else, deny the request.
        else:
            return False
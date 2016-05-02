# Running the simulation

Hi there! To run the simulation, please first ensure you have Python 2.7 or
greater and the NumPy and matplotlib Python modules installed. Then, simply
execute from this directory:

```
python driver.py
```

This will run 1500 iterations (where one iteration = one month) of our
simulation with N=50 as the starting number of humans in the simulation.

# Parameterization

If you wish to change the starting number of humans in the simulation, simply
edit line 215 in `driver.py`, changing the `initial_pop` parameter value:

```
driver.drive(max_iterations=1500,random_seed=0,initial_pop=50,food_storage=False)
```

Then, re-execute the file:

```
python driver.py
```

You can change the `initial_pop` parameter to any value of 50 or greater.

# What you should see when you run the simulation

When you execute `driver.py`, you will also see a matplotlib graph launch, which
will show the amount of produced food each iteration in megacalories, the
population count, power consumption of the population in kWh, caloric
requirements in megacalories, oxygen consumed in kg O_2, and the count of adults
in the simulation.

Thank you.
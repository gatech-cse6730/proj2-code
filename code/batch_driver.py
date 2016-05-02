from driver import Driver
import numpy as np

class BatchDriver(object):
    """
    Performs a batch of simulation runs. Only for use by analyzer.py.
    
    """

    def __init__(self, num_sims=20):
        self.num_sims = num_sims

    def drive(self, initial_pop=50):
        random_seed = 0

        results = []

        print('-'*50)
        print('---> Initializing batch for initial_pop %d.', initial_pop)

        for i in xrange(self.num_sims):
            print('---> Initializing simulation run %d for initial pop %d.' % (i, initial_pop))

            driver = Driver(vis=False)
            result = driver.drive(max_iterations=1500,
                                  random_seed=random_seed,
                                  initial_pop=initial_pop)
            results.append(result)

            random_seed += 2

        return results

if __name__ == '__main__':
    driver = BatchDriver()
    driver.drive()
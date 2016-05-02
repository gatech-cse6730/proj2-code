from driver import Driver
import numpy as np

class BatchDriver(object):
    def __init__(self, num_sims=20):
        self.num_sims = num_sims

    def drive(self, initial_pop=50):
        random_seed = 0

        results = []

        for i in xrange(self.num_sims):
            print('Initializing simulation run %d for initial pop %d.' % (i, initial_pop))

            driver = Driver(vis=False)

            while True:
                try:
                    results = driver.drive(max_iterations=1500,
                                           random_seed=random_seed,
                                           initial_pop=initial_pop)
                    results.append(result)
                    
                except Exception:
                    random_seed += 2
                    continue

                break

            random_seed += 2

        return results

if __name__ == '__main__':
    driver = BatchDriver()
    driver.drive()
from driver import Driver

class BatchDriver(object):
    def __init__(self, num_sims=20):
        self.num_sims = num_sims

    def drive(self):
        random_seed = 0

        for i in xrange(self.num_sims):
            
            print("Initializing simulation run %d." % i)

            driver = Driver(vis=False)

            results = driver.drive(max_iterations=1000,
                                   random_seed=random_seed,
                                   initial_pop=50)

            print(results)

            random_seed += 1

if __name__ == '__main__':
    driver = BatchDriver()
    driver.drive()
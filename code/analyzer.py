import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math

from batch_driver import BatchDriver

class Analyzer(object):
    def __init__(self, num_sims=20):
        """
        Creates a new Analyzer instance.

        Args:
            num_sims: Integer. Num of simulations to perform per batch.

        Returns:
            A new Analyzer instance.

        """

        self.num_sims = num_sims

    def prepare_results(self, initial_pops=[50,100]):
        self.initial_pops = initial_pops
        self.result_dict = {}

        for pop in self.initial_pops:
            self.result_dict[pop] = {}

            print('Starting batch for %d.' % pop)

            batch = BatchDriver(self.num_sims)
            results = batch.drive(initial_pop=pop)

            stdevs = []

            for indx, result in enumerate(results):
                adults = result['adults']
                minus_120 = len(adults) - 120
                last_120 = adults[minus_120:]

                stdev = np.std(last_120)
                stdevs.append(stdev)

            stdev_of_stdev = np.std(stdevs)

            self.result_dict[pop]['mean_stdev'] = np.mean(stdevs)
            self.result_dict[pop]['ci'] = (1.96 * stdev_of_stdev) / math.sqrt(self.num_sims)

        print(self.result_dict)

    def prepare_plots(self):
        sns.set_style('darkgrid')
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlabel('Initial population size (N)')
        ax.set_ylabel('Variation of adult counts over 10 years')

        a = np.arange(1, len(self.initial_pops)+1, 1)
        b, c = [], []

        for pop in self.initial_pops:
            result = self.result_dict[pop]

            b.append(result['mean_stdev'])
            c.append(result['ci'])

        ax.errorbar(a,b,yerr=c)
        ax.scatter(a,b,s=40)
        ax.plot(a,b)

        plt.show()
        plt.savefig('results/results.png', bbox_inches='tight')

if __name__ == '__main__':
    analyzer = Analyzer(num_sims=30)
    analyzer.prepare_results(initial_pops=[50,100,150,250,500,1000,1250])
    analyzer.prepare_plots()
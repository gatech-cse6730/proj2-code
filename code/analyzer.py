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
        # self.result_dict = {}
        #
        # for pop in self.initial_pops:
        #     self.result_dict[pop] = {}
        #
        #     print('Starting batch for %d.' % pop)
        #
        #     batch = BatchDriver(self.num_sims)
        #     results = batch.drive(initial_pop=pop)
        #
        #     stdevs = []
        #
        #     for indx, result in enumerate(results):
        #         adults = result['adults']
        #         minus_120 = len(adults) - 120
        #         last_120 = adults[minus_120:]
        #
        #         stdev = np.std(last_120)
        #         stdevs.append(stdev)
        #
        #     stdev_of_stdev = np.std(stdevs)
        #
        #     self.result_dict[pop]['mean_stdev'] = np.mean(stdevs)
        #     self.result_dict[pop]['ci'] = (1.96 * stdev_of_stdev) / math.sqrt(self.num_sims)
        #
        # print(self.result_dict)

    def prepare_plots(self):
        sns.set_style('darkgrid')
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlabel('Initial population size (N)')
        ax.set_ylabel('Mean variation in adult counts over a 10-year period')

        a = np.arange(1, len(self.initial_pops)+1, 1)
        b, c = [], []

        self.result_dict = {5000: {'ci': 107.2688846834053, 'mean_stdev': 531.04372702715523}, 10000: {'ci': 44.480208484728102, 'mean_stdev': 1742.1837535473371}, 2500: {'ci': 52.352292157722786, 'mean_stdev': 324.64108307110723}, 200: {'ci': 61.818194103387398, 'mean_stdev': 243.4039887309462}, 1250: {'ci': 2.157872180249738, 'mean_stdev': 52.349627034556207}, 100: {'ci': 8.9023215324361935, 'mean_stdev': 84.507699620623569}, 1000: {'ci': 3.2219210610598248, 'mean_stdev': 75.888702713003539}, 50: {'ci': 14.483541995694903, 'mean_stdev': 61.225696451918004}, 500: {'ci': 4.0779799440094031, 'mean_stdev': 111.15924942621139}, 150: {'ci': 23.533732825847604, 'mean_stdev': 213.08938278679028}, 250: {'ci': 6.3941709408915743, 'mean_stdev': 160.80310029499523}, 400: {'ci': 5.9846148376286763, 'mean_stdev': 136.27323783261383}, 300: {'ci': 21.775493254610492, 'mean_stdev': 184.25969976371289}}

        for initial_pop in self.initial_pops:
            result = self.result_dict[initial_pop]
            b.append(result['mean_stdev'])
            c.append(result['ci'])

        print('result dict', self.result_dict)
        print('a', a)
        print('b', b)
        print('c', c)

        ax.errorbar(a,b,yerr=c)
        ax.scatter(a,b,s=40)
        ax.plot(a,b)
        plt.xticks(a, self.initial_pops)

        plt.show()
        plt.savefig('results/results-final.png', bbox_inches='tight')

if __name__ == '__main__':
    analyzer = Analyzer(num_sims=30)
    analyzer.prepare_results(initial_pops=[50,100,150,200,250,300,400,500,1000,1250,2500,5000])
    analyzer.prepare_plots()
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import csv

from batch_driver import BatchDriver

class Analyzer(object):
    def __init__(self):
        """
        Creates a new Analyzer instance.

        Args:

        Returns:
            A new Analyzer instance.

        """
        pass

    def prepare_results(self):
        batch = BatchDriver()
        results = batch.drive()

        print(results['adults'])

    def prepare_plots(self):
        sns.set_style('darkgrid')
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlabel('Parameter Set')
        ax.set_ylabel('Mean Growth Rate')

        c=[1,2,3]

        ax.errorbar(a,b,yerr=c)
        ax.scatter(a,b,s=40)
        ax.plot(a,b)

        ax.errorbar(a,d,yerr=c)
        ax.scatter(a,d,s=40)
        ax.plot(a,d)

        plt.xticks(np.arange(np.min(a), np.max(a)+1, 1))
        plt.savefig('results.png', bbox_inches='tight')

if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.prepare_results()
    #analyzer.prepare_plots()

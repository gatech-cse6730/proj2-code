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

    def prepare_plots(self):
        sns.set_style('darkgrid')
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlabel('Parameter Set')
        ax.set_ylabel('Mean Growth Rate')


        a=np.arange(1,4,1)
        b=np.arange(14,17,1)
        c=[1,2,3]

        ax.errorbar(a,b,yerr=c)
        ax.scatter(a,b,s=40)

        plt.xticks(np.arange(np.min(a), np.max(a)+1, 1))
        rname = 'results-%d.png' % i
        print rname
        plt.savefig(rname, bbox_inches='tight')

if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.prepare_results()
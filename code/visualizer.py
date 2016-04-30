import matplotlib.pyplot as plt

class Visualizer(object):
    def __init__(self):
        # Enable interactive mode.
        plt.ion()

        # Initialize the plot.
        fig = plt.figure()
        self.ax = fig.add_subplot(111)

    def setup(self, series):
        self.x = []
        self.y = { s: [] for s in series }

        self._plot()

        # Create the legend.
        plt.legend(loc='upper left');

    def advance_x(self, x):
        self.x.append(x)

    def update(self):
        # Plot the data.
        self._plot()

        # A short pause so Mac OS X 10.11.3 doesn't break.
        plt.pause(0.0001)

    def add_data(self, data = {}):
        for label, datum in data.iteritems():
            self.y[label].append(datum)

    def _plot(self):
        for label, data in self.y.iteritems():
            self.ax.scatter(self.x, data, c='green', label=label)
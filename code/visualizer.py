import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as plticker
import time

class Visualizer(object):
    def __init__(self, log_scale=False, series=()):
        """
        Creates a new Visualizer.

        Args:
            log: <Boolean>. Flag for using the log scale.

        Returns:
            A new Visualizer instance.
        """

        # Set whether or not to use a log scale.
        self.log_scale = log_scale

        # Set the data series for the graph.
        self.series = ('Population Count',
                       'Adult Count',
                       'Caloric Requirements (Mcal)',
                       'Produced Food (Mcal)',
                       'Air (kg O2)',
                       'Power Consumption (kWh)')

        # Enable interactive mode.
        plt.ion()

        # Initialize the plot.
        f, self.axarr = plt.subplots(len(self.series), sharex=True)
        self._setup()

    def update(self):
        """
        Updates the scatter plot, re-rendering it for viewing by the user.

        Args:
            None.

        Returns:
            None.
        """

        # Plot the data.
        self._plot()

        # If the log scale option has been provided, plot the data using a
        # log-scale.
        if self.log_scale:
            for indx, series in enumerate(self.series):
                self.axarr[indx].set_yscale('log')

        # A short pause so Mac OS X 10.11.3 doesn't break.
        plt.pause(0.0001)

    def add_data(self, x, data={}):
        """
        Adds data for plotting.

        Args:
            x: <Integer>. A data point for the x-axis on the graph.
            data: <Dictionary>. Should be a dictionary of the form:
                  { 'series1': Integer, 'series2': Integer }
                  The provided integer data points will be appended to the
                  existing data arrays for each of the provided series.

        Returns:
            None.
        """

        # Append the given x-axis data point.
        self.x.append(x)

        # For each provided series, append the given data point to the list
        # for the correct series.
        for label, datum in data.iteritems():
            self.y[label]['data'].append(datum)

    def savefig(self):
        """
        Saves the current figure as an image.

        Args:
            None.

        Returns:
            None.
        """

        fname = 'results/results-%s.png' % time.strftime('%H_%M_%S')
        plt.savefig(fname, bbox_inches='tight')

    # Private methods

    def _setup(self):
        """
        Sets up the plot. Initializes each series and adds a legend.

        Args:
            None.

        Returns:
            None.
        """

        # Initialize the x-axis data points.
        self.x = []

        # Initialize the y-axis series.
        self.y = { s: { 'color': np.random.rand(3,1), 'data': [] } for s in self.series }

        # Render the plot.
        self._plot()

        # Create the legend.
        for indx, s in enumerate(self.series):
            self.axarr[indx].legend(loc='center right', bbox_to_anchor=(1.3, 0.5), fancybox=True)

    def _plot(self):
        """
        Re-renders the plot.

        Args:
            None.

        Returns:
            None.
        """

        # For each series, plot the current data points.
        for indx, (label, data_dict) in enumerate(self.y.iteritems()):
            data = data_dict['data']

            if len(data) is not 0:
                the_min = np.min(data)
                the_max = np.max(data)

                spacing = int((the_max - the_min) / float(3.0))
                spacing = 1 if spacing == 0.0 else spacing
                spacing = self._roundup(spacing)

                loc = plticker.MultipleLocator(base=spacing)
                self.axarr[indx].yaxis.set_major_locator(loc)

            self.axarr[indx].scatter(self.x, data, c=data_dict['color'], label=label)

    def _roundup(self, x):
        """
        Rounds x up to a nice number

        Args:
            x: <Float> Input number to round up.

        Returns:
            <Integer> .
        """

        if x < 100:
            fact = 10
        elif x < 1000:
            fact = 100
        elif x < 10000:
            fact = 1000
        elif x < 100000:
            fact = 10000
        else:
            fact = 100000

        return x if x % fact == 0 else x + fact - x % fact

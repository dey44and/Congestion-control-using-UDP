from pathlib import Path

import numpy
import matplotlib.pyplot as plt


class Stats(object):
    def __init__(self):
        self.__items = []

    def add_point(self, value: int):
        self.__items.append(value)

    def save_plot(self):
        # Create data
        x = numpy.arange(0, len(self.__items), 1)
        y = numpy.array(self.__items)

        # Create plot
        plt.plot(x, y)
        plt.title("Evolution of congestion window size over every RTT")
        plt.xlabel("RTT")
        plt.ylabel("Congestion Window")
        ROOT_DIR = Path(__file__).parent.parent.__str__()
        plt.savefig(ROOT_DIR + '\\Statistics\\grafic.png')

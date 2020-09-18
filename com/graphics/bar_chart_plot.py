from com.graphics.chart_plot import ChartPlot
import matplotlib.pyplot as plt
import numpy as np
from constants import IMAGES


class BarChartPlot(ChartPlot):
    def __init__(self, x_labels, values, file, x_axis_legend, y_axis_legend):
        self.x_labels = x_labels
        self.values = values
        self.file = file
        self.locations_labels = np.arange(len(x_labels))  #The label locations
        self.width = 0.45    #The width of bars
        self.fig, ax = plt.subplots(figsize=(10, 8))    #Create a figure and a set of subplots.
        self.bars = self.create_bars(ax)
        self.set_value_top_bar(ax)
        self.set_legend(ax, x_axis_legend, y_axis_legend)
        self.fig.tight_layout() #Automatically adjust subplot parameters to give specified padding.
        plt.xticks(rotation='vertical')
        #Para prevenir la no visualización de las etiquetas del eje de las x
        plt.subplots_adjust(bottom=0.35)
        #plt.show()

    def create_bars(self, ax):
        return ax.bar(self.x_labels, self.values)

    def set_legend(self, ax, x_axis_label, y_axis_label):
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel(y_axis_label)
        ax.set_title(x_axis_label)
        ax.set_xticks(self.locations_labels)
        ax.set_xticklabels(self.x_labels)
        #ax.legend()

    def set_value_top_bar(self, ax):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in self.bars:
            height = rect.get_height()
            #height = self.locale_format(height)
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

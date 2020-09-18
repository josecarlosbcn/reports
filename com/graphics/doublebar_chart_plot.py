import matplotlib.pyplot as plt
import numpy as np
from com.graphics.chart_plot import ChartPlot


class MultiBarChatPlot(ChartPlot):
    '''Object to create a grouped 2 bar chart. We receive three parameters
        x_labels: We group values around each label. This labels will be located in x-axis
        values: It's a list of lists. The length of the list will be the number of bars grouped around each label. Each element
        of he list contains a list of values. For example:
        values[0]  = [1, 2, 4, 5, 6]
        values[1] = [0, 3, 5, 7, 8]
        legends: Name of labels for the legend
        file: route to the image file
        x_axis_legend: Text of the x axis legend
        y_axis_legend: Text of the y axis legend
    '''
    def __init__(self, x_labels, values, legends, file, x_axis_legend, y_axis_legend):
        self.x_labels = x_labels
        self.legends = legends
        self.values = values
        self.file = file
        self.locations_labels = np.arange(len(x_labels))  #The label locations
        self.width = 0.45    #The width of bars
        fig, ax = plt.subplots(figsize=(7, 5))    #Create a figure and a set of subplots.
        self.bars = self.create_bars(ax)
        self.set_legend(ax, x_axis_legend, y_axis_legend)
        self.set_value_top_bar(ax)
        fig.tight_layout() #Automatically adjust subplot parameters to give specified padding.
        #plt.show()

    def create_bars(self, ax):
        ''' We create a bar for each positions of values list
            If we want to have more than two bars grouped we need to modify this method
        '''
        bars = []
        bars.append(ax.bar(self.locations_labels - self.width/2, self.values[0], self.width, label = self.legends[0]))
        bars.append(ax.bar(self.locations_labels + self.width/2, self.values[1], self.width, label = self.legends[1]))
        return bars

    def set_legend(self, ax, x_axis_label, y_axis_label):
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel(y_axis_label)
        ax.set_title(x_axis_label)
        ax.set_xticks(self.locations_labels)
        ax.set_xticklabels(self.x_labels)
        ax.legend()

    def set_value_top_bar(self, ax):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for bar in self.bars:
            for rect in bar:
                height = rect.get_height()
                #height = self.locale_format(height)
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')



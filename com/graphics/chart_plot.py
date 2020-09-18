import matplotlib.pyplot as plt
from constants import IMAGES
import locale


class ChartPlot:
    @staticmethod
    def locale_format(d):
        '''Returns a number in spanish format'''
        return locale.format('%0.2f', d, grouping=True)

    def save_file(self):
        '''If the image saved is blanked this is due to we show first the image and then we try to save it. When we show the image, the image is created again so
        it's possible that when we try to save it we save the new blanked image'''
        plt.savefig(IMAGES.IMAGE_ROUTE + self.file)

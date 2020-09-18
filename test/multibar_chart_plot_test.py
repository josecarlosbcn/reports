import unittest
from com.graphics.doublebar_chart_plot import MultiBarChatPlot
import os


class TestMultiBarChartPlot(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))

    def test_create_bars(self):
        legends = ["GIR", "AVE"]
        labels = ["T2P%", "T3P%", "TL%", "BR%"]
        values = []
        values.append([35.48, 35.48, 75.48, 14.59])
        values.append([42.58, 37.25, 78.68, 19.52])
        destiny = "770.769.report"
        mb = MultiBarChatPlot(labels, values, legends, destiny)
        self.assertEqual(len(mb.bars), 2, "ERROR:test_create_bars: El núnero de bars creados no es 2")

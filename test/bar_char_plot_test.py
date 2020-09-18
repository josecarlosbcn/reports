import unittest
from com.graphics.bar_chart_plot import BarChartPlot


class TestBarChartPlot(unittest.TestCase):
    def test_create_bar(self):
        labels = ["María Antonieta Pérez", "María Conde Alcolado", "Irene Borra Serrano", "María Antonieta Pérez1", "María Conde Alcolado1", "Irene Borra Serrano1",
                  "María Antonieta Pérez2", "María Conde Alcolado2", "Irene Borra Serrano2", "María Antonieta Pérez3", "María Conde Alcolado3", "Irene Borra Serrano3",
                  "María Antonieta Pérez4", "María Conde Alcolado4", "Irene Borra Serrano4"]
        values = [35.48, 35.48, 75.48, 35.48, 35.48, 75.48, 35.48, 35.48, 75.48, 35.48, 35.48, 75.48, 35.48, 35.48, 75.48]
        destiny = "770.769.report"
        mb = BarChartPlot(labels, values, destiny, "Distribución de puntos por jugadora", "Porcentaje")
        self.assertEqual(len(mb.bars), 3, "ERROR:test_create_bars: El núnero de bars creados no es 1")

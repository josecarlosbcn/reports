import unittest
from com.shotchart.images.shotchartimage import ShotChartImage
from constants import IMAGES
import os
import pandas as pd


class TestImage(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
        pd.set_option("display.max_columns", None)

    def test_create_image(self):
        i = ShotChartImage(IMAGES.BASKET_COURT)

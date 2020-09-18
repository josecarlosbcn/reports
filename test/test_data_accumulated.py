import unittest
import os
import pandas as pd
from reports.data.data_team_accumulated import DataTeamAccumulated
from decimal import Decimal


class TestDataAccumulated(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
        pd.set_option("display.max_columns", None)

    def test_list_games(self):
        params = {
            "report" : 4,
            "competition": "FEB-LF1",
            "home" : 770,
            "away" : None,
            "destiny" : 770
        }
        d = DataTeamAccumulated(params)
        #print(d.list_games)
        self.assertEqual(len(d.list_games), 26, "test_list_games:: El número de filas devuelto no es el correcto")
        self.assertEqual("Supercopa", d.list_games["competition"][0], "test_list_games:: La competición obtenida no es la correcta")

    def test_get_team_standard_stats(self):
        params = {
            "report" : 4,
            "competition": "FEB-LF1",
            "home" : 770,
            "away" : None,
            "destiny" : 770
        }
        d = DataTeamAccumulated(params)
        self.assertEqual(26, d.tss["games"], "test_get_team_standard_stats:: El número de partidos devuelto no es correcto")
        self.assertEqual(1136, d.tss["t2p_int"], "test_get_team_standard_stats:: El número de tiros de 2 puntos intentado no es correcto")
        self.assertEqual(round(Decimal(74.73), 2), d.tss["total_puntos_pp"], "test_get_team_standard_stats:: El total de puntos anotados por partido no es correcto")

    def test_get_team_advanced_stats(self):
        params = {
            "report" : 4,
            "competition": "FEB-LF1",
            "home" : 770,
            "away" : None,
            "destiny" : 770
        }
        d = DataTeamAccumulated(params)
        self.assertEqual(round(Decimal(51.97), 2), d.tas["etc"], "test_get_team_advanced_stats:: El %etc no es el correcto")
        self.assertEqual(round(Decimal(30.76), 2), d.tas["p_reb_of"], "test_get_team_advanced_stats:: El %rebotes ofensivos no es el correcto")
        self.assertEqual(round(Decimal(0.90), 2), d.tas["steals_x_turnovers"], "test_get_team_advanced_stats:: El ratio entre robos y pérdidas no es correcto")
        self.assertEqual(round(Decimal(109.32), 2), d.tas["ortg"], "test_get_team_advanced_stats:: El ORTG no es correcto")
        self.assertEqual(round(Decimal(78.77), 2), d.tas["drtg"], "test_get_team_advanced_stats:: El DRTG no es correcto")

    def test_get_opp_standard_stats(self):
        params = {
            "report" : 4,
            "competition": "FEB-LF1",
            "home" : 770,
            "away" : None,
            "destiny" : 770
        }
        d = DataTeamAccumulated(params)
        self.assertEqual(round(Decimal(14.69), 2), d.oss["t2p_conv_pp"], "test_get_opp_team_standard_stats:: El número de tiros de dos puntos anotados por partido no es correcto")
        self.assertEqual(round(Decimal(31.71), 2), d.oss["p_t3p_puntos"], "test_get_opp_team_standard_stats:: El % de puntos anotados de 3 no es correcto")
        self.assertEqual(round(Decimal(0.77), 2), d.oss["pointsbyposs"], "test_get_opp_team_standard_stats:: El numero de puntos por posesión no es correcto")

    def test_get_opp_advanced_stats(self):
        params = {
            "report" : 4,
            "competition": "FEB-LF1",
            "home" : 770,
            "away" : None,
            "destiny" : 770
        }
        d = DataTeamAccumulated(params)
        self.assertEqual(round(Decimal(41.68), 2), d.oas["etc"], "test_get_team_advanced_stats:: El %etc no es el correcto")
        self.assertEqual(round(Decimal(24.97), 2), d.oas["p_reb_of"], "test_get_team_advanced_stats:: El %rebotes ofensivos no es el correcto")
        self.assertEqual(round(Decimal(0.41), 2), d.oas["steals_x_turnovers"], "test_get_team_advanced_stats:: El ratio entre robos y pérdidas no es correcto")
        self.assertEqual(round(Decimal(78.77), 2), d.oas["ortg"], "test_get_team_advanced_stats:: El ORTG no es correcto")
        self.assertEqual(round(Decimal(109.32), 2), d.oas["drtg"], "test_get_team_advanced_stats:: El DRTG no es correcto")

    def test_get_shots(self):
        params = {
            "report" : 4,
            "competition": "FEB-LF1",
            "home" : 770,
            "away" : None,
            "destiny" : 770
        }
        d = DataTeamAccumulated(params)
        self.assertEqual(1546, len(d.shots), "test_get_shots:: El número de filas del dataframe es el correcto")

    def test_get_abrev(self):
        params = {
            "report" : 4,
            "competition": "FEB-LF1",
            "home" : 770,
            "away" : None,
            "destiny" : 770
        }
        d = DataTeamAccumulated(params)
        self.assertEqual("AVE", d.abrev, "test_get_abrev:: La abreviatura del equipo no es correcta")

    def test_get_players(self):
        params = {
            "report" : 4,
            "competition": "FEB-LF1",
            "home" : 770,
            "away" : None,
            "destiny" : 770
        }
        d = DataTeamAccumulated(params)
        self.assertEqual(13, len(d.list_players), "test_get_player:: El total de filas recibidas NO es correcta")

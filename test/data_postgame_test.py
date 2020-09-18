import unittest
from reports.data.data_post_game import DataPostGame
from constants import COMPETITIONS
import os


class TestDataMethods(unittest.TestCase):
    def test_get_id_game(self):
        os.chdir("../") #We need to do this to go to the main directory of the app. If we don't do this, the code will run over ./test
        params = {"report" : 2, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPostGame(params)
        game = data.game
        self.assertEqual(game.get_result().getTotalRows(), 1, "Error: Se ha devuelto un número no correcto de filas")
        self.assertEqual(game.get_result().getData()[0]["id"], 10929, "Error: El id de partido no es el correcto")
        self.assertEqual(game.get_result().getData()[0]["home_score"], 76, "Error: El marcador del equipo de casa no es correcto")

    def test_team_standard_stats(self):
        params = {"report" : 2, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPostGame(params)
        home_team_ss = data.home_standard_stats
        self.assertEqual(home_team_ss.get_result().getTotalRows(), 1, "Error: Se ha devuelto un número no correcto de filas")
        self.assertEqual(home_team_ss.get_result().getData()[0]["steals"], 13, "Error: El número de robos no es el correcto")
        self.assertEqual(home_team_ss.get_result().getData()[0]["fouls_cm"], 22, "Error: El número de faltas cometidas no es la correcta")
        params = {"report" : 2, "league" : COMPETITIONS.EUROLEAGUE, "home": 86, "away": 79}
        data = DataPostGame(params)
        away_team_ss = data.away_standard_stats
        self.assertEqual(away_team_ss.get_result().getTotalRows(), 1, "Error: Se ha devuelto un número no correcto de filas")
        self.assertEqual(away_team_ss.get_result().getData()[0]["tl_conv"], 7, "Error: El número de tiros libres convertidos no es el correcto")
        self.assertEqual(away_team_ss.get_result().getData()[0]["assists"], 26, "Error: El número de asistencias no es el correcto")

    def test_players_standard_stats(self):
        params = {"report" : 2, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPostGame(params)
        players_home_ss = data.home_pt_ss
        self.assertEqual(players_home_ss.get_result().getTotalRows(), 10, "Error: Se ha devuelto un número no correcto de filas")
        self.assertEqual(players_home_ss.get_result().getData()[4]["reb_def"], 5, "Error: El número de rebotes defensivos no es el correcto")
        self.assertEqual(players_home_ss.get_result().getData()[2]["total_puntos"], 25, "Error: El número puntos no es el correcto")
        params = {"report" : 2, "league" : COMPETITIONS.EUROLEAGUE, "home": 86, "away": 79}
        data = DataPostGame(params)
        players_away_ss = data.away_pt_ss
        self.assertEqual(players_away_ss.get_result().getTotalRows(), 10, "Error: Se ha devuelto un número no correcto de filas")
        self.assertEqual(players_away_ss.get_result().getData()[3]["tl_conv"], 2, "Error: El número de tiros libres convertidos no es el correcto")
        self.assertEqual(players_away_ss.get_result().getData()[5]["tc_int"], 18, "Error: El número de tiros de campo intentados no es el correcto")

    def test_players_advanced_stats(self):
        params = {"report" : 2, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPostGame(params)
        players_home_as = data.home_pt_as
        self.assertEqual(players_home_as.get_result().getTotalRows(), 10, "Error: El  númoro de filas devulves no es el correcto")
        self.assertEqual(float(players_home_as.get_result().getData()[7]["ts"]), 90.91, "Error: El valor de TS% no es el correcto")
        self.assertEqual(float(players_home_as.get_result().getData()[0]["nrtg"]), -22.02, "Error: El valor de NRTG no es el correcto")
        params = {"report" : 2, "league" : COMPETITIONS.EUROLEAGUE, "home": 86, "away": 79}
        data = DataPostGame(params)
        players_away_as = data.away_pt_as
        self.assertEqual(players_away_as.get_result().getTotalRows(), 10, "Error: El número de filas devueltas no es el correcto")
        self.assertEqual(float(players_away_as.get_result().getData()[2]["ts"]), 70.83, "Error: El valor de TS% no es el correcto")
        self.assertEqual(float(players_away_as.get_result().getData()[5]["p_tot_reb"]), 23.21, "Error el porcentaje del total de rebotes no es el correcto")

if __name__== "__main__":
    unittest.main()

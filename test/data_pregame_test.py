import unittest
from reports.data.data_pre_game import DataPreGame
from constants import COMPETITIONS
import os
from decimal import Decimal


class TestDataMethods(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))

    def test_team_standard_stats(self):
        params = {"report" : 1, "competition" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        home_tss = data.home_standard_stats
        self.assertEqual(len(home_tss), 1, "Error al devolver datos. No se devuelve 1 única fila de datos")
        self.assertEqual(int(home_tss[0]["t2p_int"]), 1136, "Error al devolver el número de t2p_int")
        self.assertEqual(Decimal(home_tss[0]["t2p_percentage"]), round(Decimal(51.32), 2), "Error al devolver el número de t2p_percentage")
        self.assertEqual(Decimal(home_tss[0]["ppa"]), round(Decimal(0.98), 2), "Error al devolver los puntos por intento del equipo")
        params = {"report" : 1, "competition" : COMPETITIONS.EUROLEAGUE, "home": 79, "away": 93}
        data = DataPreGame(params)
        home_tss = data.home_standard_stats
        self.assertEqual(len(home_tss), 1, "Error al devolver datos. No se devuelve 1 única fila de datos")
        self.assertEqual(int(home_tss[0]["t2p_int"]), 848, "Error al devolver el número de t2p_int")
        self.assertEqual(Decimal(home_tss[0]["t2p_percentage"]), round(Decimal(49.53), 2), "Error al devolver el número de t2p_percentage")
        self.assertEqual(Decimal(home_tss[0]["ppa"]), round(Decimal(0.92), 2), "Error al devolver los puntos por intento del equipo")

    def test_opp_team_standard_stats(self):
        params = {"report" : 1, "competition" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        home_opps_tss = data.home_opps_standard_stats
        self.assertEqual(len(home_opps_tss), 1, "Error al devolver datos. No se devuelve 1 única fila de datos")
        self.assertEqual(int(home_opps_tss[0]["t2p_int"]), 966, "Error al devolver el número de t2p_int")
        self.assertEqual(Decimal(home_opps_tss[0]["t2p_percentage"]), round(Decimal(39.54), 2), "Error al devolver el número de t2p_percentage")
        self.assertEqual(Decimal(home_opps_tss[0]["ppa"]), round(Decimal(0.81), 2), "Error al devolver los puntos por intento del equipo")
        params = {"report" : 1, "competition" : COMPETITIONS.EUROLEAGUE, "home": 79, "away": 93}
        data = DataPreGame(params)
        away_opps_tss = data.away_opps_standard_stats
        self.assertEqual(len(away_opps_tss), 1, "Error al devolver datos. No se devuelve 1 única fila de datos")
        self.assertEqual(int(away_opps_tss[0]["t2p_int"]), 639, "Error al devolver el número de t2p_int")
        self.assertEqual(Decimal(away_opps_tss[0]["t2p_percentage"]), round(Decimal(48.20), 2), "Error al devolver el número de t2p_percentage")
        self.assertEqual(Decimal(away_opps_tss[0]["ppa"]), round(Decimal(0.96), 2), "Error al devolver los puntos por intento del equipo")

    def test_team_advanced_stats(self):
        params = {"report": 1, "competition": COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        home_tas = data.home_advanced_stats
        self.assertEqual(len(home_tas), 1, "Local:: Error al devolver datos. No se devuelve 1 única fila de datos")
        self.assertEqual(Decimal(home_tas[0]["ortg"]), round(Decimal(109.32), 2), "Local:: Error al devolver el ORTG")
        params = {"report": 1, "competition": COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        away_tas = data.away_advanced_stats
        self.assertEqual(len(away_tas), 1, "Visitante:: Error al devolver datos. No se devuelve 1 única fila de datos")
        self.assertEqual(Decimal(away_tas[0]["drtg"]), round(Decimal(81.84), 2), "Visitante: Error al deveolver el DRTG")
        params = {"report": 1, "competition": COMPETITIONS.EUROLEAGUE, "home": 79, "away": 93}
        data = DataPreGame(params)
        away_tas = data.away_advanced_stats
        self.assertEqual(len(away_tas), 1, "Visitante:: Error al devolver datos. No se devuelve 1 única fila de datos")
        self.assertEqual(Decimal(away_tas[0]["drtg"]), round(Decimal(106.45), 2), "Visitante: Error al deveolver el DRTG")

    def test_players_teams_ss(self):
        params = {"report" : 1, "competition" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        home_pt_ss = data.players_team_ss(params["home"], params["competition"])
        self.assertEqual(len(home_pt_ss), 13, "Error: Número de registros recibido no es correcto")
        self.assertEqual(home_pt_ss[8]["numero"], 44, "Error: El número de la jugadora no es correcto")
        self.assertEqual(Decimal(home_pt_ss[3]["t2p_percentage"]), round(Decimal(55.03), 2), "Error: El porcentaje de acierto de T2P no es correcto")
        params = {"report" : 1, "competition" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        away_pt_ss = data.players_team_ss(params["away"], params["competition"])
        self.assertEqual(len(away_pt_ss), 15, "Error: Número de registros recibido no es correcto")
        self.assertEqual(away_pt_ss[8]["numero"], 3, "Error: El número de la jugadora no es correcto")
        self.assertEqual(Decimal(away_pt_ss[3]["t2p_percentage"]), round(Decimal(37.25), 2), "Error: El porcentaje de acierto de T2P no es correcto")

    def test_players_teams_as(self):
        params = {"report" : 1, "competition" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        home_pt_as = data.players_team_as(params["home"], params["competition"])
        self.assertEqual(len(home_pt_as), 13, "Error: Número de registros recibido no es correcto")
        self.assertEqual(Decimal(home_pt_as[8]["etc"]), round(Decimal(60.24), 2), "Error: El número de la jugadora no es correcto")
        self.assertEqual(Decimal(home_pt_as[3]["usg"]), round(Decimal(27.19), 2), "Error: El porcentaje de acierto de T2P no es correcto")
        params = {"report" : 1, "competition" : COMPETITIONS.EUROLEAGUE, "home": 79, "away": 93}
        data = DataPreGame(params)
        away_pt_ss = data.players_team_as(params["away"], params["competition"])
        self.assertEqual(len(away_pt_ss), 15, "Error: Número de registros recibido no es correcto")
        self.assertEqual(Decimal(away_pt_ss[8]["p_assists"]), round(Decimal(14.30), 2), "Error: El número de la jugadora no es correcto")
        self.assertEqual(Decimal(away_pt_ss[3]["ortg"]), round(Decimal(99.79), 2), "Error: El porcentaje de acierto de T2P no es correcto")

    def test_players_team_as(self):
        params = {"report" : 1, "competition" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        players_home_as = data.players_home_as
        players_away_as = data.players_away_as
        self.assertEqual(len(players_home_as), 13, "Error: El total de elementos de la lista de jugadoras locales no es correcta")
        self.assertEqual(len(players_away_as), 15, "Error: El total de elementos de la lista de jugadoras visitantes no es correcta")
        self.assertEqual(Decimal(players_home_as[8]["etc"]), round(Decimal(60.24), 2), "Error: El eFG% de la jugadora no es correcta")
        self.assertEqual(Decimal(players_home_as[3]["usg"]), round(Decimal(27.19), 2), "Error: El USG% de la jugadora no es correcto")
        self.assertEqual(Decimal(players_away_as[8]["p_assists"]), round(Decimal(35.27), 2), "Error: El %Assists de la jugadora no es correcta")
        self.assertEqual(Decimal(players_away_as[3]["ortg"]), round(Decimal(95.32), 2), "Error: El ORTG de la jugadora no es correcto")



if __name__== "__main__":
    unittest.main()

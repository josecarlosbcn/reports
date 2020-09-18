import unittest
from constants import COMPETITIONS
from reports.data.data_monthly import DataMonthly
import os


class TestDataMonthly(unittest.TestCase):
    # def test_team_standard_stats(self):
    #     #os.chdir("../")
    #     params = {"report" : 3, "league" : COMPETITIONS.LF1, "home": 770, "away": 769, "month": 1, "year": 2020}
    #     data = DataMonthly(params)
    #     home_standard_stats = data.home_standard_stats
    #     self.assertEqual(int(home_standard_stats.get_result().getTotalRows()), 1, "Error: Se ha devuelto un número no correcto de filas")
    #     self.assertEqual(int(home_standard_stats.get_result().getData()[0]["games"]), 5, "Error: El número de partidos no es correcto")
    #     self.assertEqual(int(home_standard_stats.get_result().getData()[0]["t3p_conv"]), 36, "Error: Los tiros de tres puntos convertidos no son correctos")
    #     away_standard_stats = data.away_standard_stats
    #     self.assertEqual(float(away_standard_stats.get_result().getData()[0]["ppa"]), 0.79, "Error: El número de puntos por intento no es correcto")
    #     self.assertEqual(float(away_standard_stats.get_result().getData()[0]["total_puntos_pp"]), 63.20, "Error: Los puntos por partido no son correctos ")
    #     self.assertEqual(int(away_standard_stats.get_result().getData()[0]["reb_def"]), 135, "Error: Los rebotes defensivos no son correctos")
    #
    # def test_opp_team_standard_stats(self):
    #     os.chdir("../")
    #     params = {"report" : 3, "league" : COMPETITIONS.LF1, "home": 770, "away": 769, "month": 1, "year": 2020}
    #     data = DataMonthly(params)
    #     home_opps_tss = data.home_opps_standard_stats
    #     self.assertEqual(home_opps_tss.get_result().getTotalRows(), 1, "Error al devolver datos. No se devuelve 1 única fila de datos")
    #     self.assertEqual(int(home_opps_tss.get_result().getData()[0]["t2p_int"]), 197, "Error al devolver el número de t2p_int")
    #     self.assertEqual(float(home_opps_tss.get_result().getData()[0]["t2p_percentage"]), 35.53, "Error al devolver el número de t2p_percentage")
    #     self.assertEqual(float(home_opps_tss.get_result().getData()[0]["ppa"]), 0.81, "Error al devolver los puntos por intento del equipo")
    #     away_opps_tss = data.away_opps_standard_stats
    #     self.assertEqual(away_opps_tss.get_result().getTotalRows(), 1, "Error al devolver datos. No se devuelve 1 única fila de datos")
    #     self.assertEqual(int(away_opps_tss.get_result().getData()[0]["t2p_int"]), 205, "Error al devolver el número de t2p_int")
    #     self.assertEqual(float(away_opps_tss.get_result().getData()[0]["t2p_percentage"]), 42.44, "Error al devolver el número de t2p_percentage")
    #     self.assertEqual(float(away_opps_tss.get_result().getData()[0]["ppa"]), 0.84, "Error al devolver los puntos por intento del equipo")

    # def test_team_advanced_stats(self):
    #     os.chdir("../")
    #     params = {"report" : 3, "league" : COMPETITIONS.LF1, "home": 770, "away": 769, "month": 1, "year": 2020}
    #     data = DataMonthly(params)
    #     home_tas = data.home_advanced_stats
    #     self.assertEqual(float(home_tas.get_etc()), 62.34, "Local:: Error al devolver el %eTC")
    #     self.assertEqual(float(home_tas.get_ortg()), 122.94, "Local:: Error al devolver el ORTG")
    #     away_tas = data.away_advanced_stats
    #     self.assertEqual(away_tas.get_rival_etc(), 42.79, "Visitante:: Error al devolver %eTC del rival")
    #     self.assertEqual(float(away_tas.get_ts()), 43.93, "Visitante: Error al devolver el TS%")

    # def test_players_team_ss(self):
    #     os.chdir("../")
    #     params = {"report" : 3, "league" : COMPETITIONS.LF1, "home": 770, "away": 769, "month": 1, "year": 2020}
    #     data = DataMonthly(params)
    #     home_pt_ss = data.home_pt_ss
    #     self.assertEqual(home_pt_ss.get_result().getTotalRows(), 11, "Error: El total de filas devueltas no es 11")
    #     self.assertEqual(float(home_pt_ss.get_result().getData()[2]["mpp"]), 18.25, "Error: Los minutos por partido jugados no son correctos")
    #     self.assertEqual(home_pt_ss.get_result().getData()[5]["numero"], 21, "Error: El número de la jugadora no es correcto")
    #     self.assertEqual(home_pt_ss.get_result().getData()[5]["total_rebs"], 23, "Error: El total de rebotes capturados no es correcto")
    #     params = {"report" : 3, "league" : COMPETITIONS.EUROLEAGUE, "home": 91, "away": 79, "month": 1, "year": 2020}
    #     data = DataMonthly(params)
    #     away_pt_ss= data.away_pt_ss
    #     self.assertEqual(away_pt_ss.get_result().getTotalRows(), 11, "Error: El número de filas devueltas no es 11")
    #     self.assertEqual(float(away_pt_ss.get_result().getData()[0]["t2p_percentage"]), 46.67, "Error: El T2P% no es correcto")
    #     self.assertEqual(float(away_pt_ss.get_result().getData()[3]["tc_int_pp"]), 15.00, "Error: El TC% no es correcto")
    #     self.assertEqual(float(away_pt_ss.get_result().getData()[3]["pointsbyposs"]), 1.04, "Error: Los puntos anotados por posesión no son correctos")

    def test_players_team_as(self):
        os.chdir("../")
        params = {"report" : 3, "league" : COMPETITIONS.LF1, "home": 770, "away": 769, "month": 1, "year": 2020}
        data = DataMonthly(params)
        players_home_as = data.players_home_as
        #players_away_as = data.players_away_as
        self.assertEqual(len(players_home_as), 11, "Error: El total de elementos de la lista de jugadoras locales no es correcta")
        #self.assertEqual(len(players_away_as), 12, "Error: El total de elementos de la lista de jugadoras visitantes no es correcta")
        self.assertEqual(float(players_home_as[0].game_score), 6.12, "Error: El GameScore de la jugadora no es correcta")
        self.assertEqual(float(players_home_as[4].ortg), 119.33, "Error: El ORTG de la jugadora no es correcto")
        #self.assertEqual(float(players_away_as[3].game_score), -1.20, "Error: El GameScore de la jugadora no es correcta")
        #self.assertEqual(float(players_away_as[4].ortg), 106.51, "Error: El ORTG de la jugadora no es correcto")


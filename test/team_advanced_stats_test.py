import unittest
from reports.data.data_pre_game import DataPreGame
from com.statistics.advanced.team_advanced_stats import TeamAS
from constants import COMPETITIONS
import os

class TestTeamAdvancedStats(unittest.TestCase):
    def test_set_etc(self):
        os.chdir("../")
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_etc()
        self.assertEqual(tas.get_minutes(), 5200, "Error: El número de minutos no es el correcto")
        self.assertEqual(float(tas.get_etc()), 51.97, "Error: El valor de eTC% no es correcto")

    def test_set_percentage_reb_def(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_percentage_reb_def()
        self.assertEqual(float(tas.get_percentage_reb_def()), 75.03, "Error: El valor del %Reb.Def. no es el correcto")

    def test_set_percentage_reb_of(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_percentage_reb_of()
        self.assertEqual(float(tas.get_percentage_reb_of()), 30.76, "Error: El valor del %Reb.Of. no es el correcto")

    def test_set_rival_percentage_turnovers(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_rival_percentage_turnovers()
        self.assertEqual(float(tas.get_rival_percentage_turnovers()), 22.18, "Error: El valor del Rival %TOV no es el correcto")

    def test_set_percentage_turnovers(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_percentage_turnovers()
        self.assertEqual(float(tas.get_percentage_turnovers()), 15.30, "Error: El valor del %TOV. no es el correcto")

    def test_set_ratio_ft(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_ratio_ft()
        self.assertEqual(float(tas.get_ratio_ft()), 0.17, "Error: El valor del Ratio de TL. no es el correcto")

    def test_set_rival_ratio_ft(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_rival_ratio_ft()
        self.assertEqual(float(tas.get_rival_ratio_ft()), 0.13, "Error: El valor del Ratio de TL. del rival no es el correcto")

    def test_set_rival_etc(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_rival_etc()
        self.assertEqual(float(tas.get_rival_etc()), 41.68, "Error: El valor del %eTC del Rival no es el correcto")

    def test_set_possessions(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_possessions()
        self.assertEqual(float(tas.get_possessions()), 1777.33, "Error: El valor del número de posesiones no es el correcto")

    def test_set_possession_time(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_possessions()
        tas.set_possession_time()
        self.assertEqual(float(tas.get_possession_time()), 1.71, "Error: El valor del número de posesiones  por minuto no es el correcto")

    def test_set_ratio_assists_turnovers(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_ratio_assists_turnovers()
        self.assertEqual(float(tas.get_ratio_assists_turnovers()), 1.28, "Error: El valor del ratio de asistencias por pérdida no es el correcto")

    def test_set_ratio_steals_turnovers(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_ratio_steals_turnovers()
        self.assertEqual(float(tas.get_ratio_steals_turnovers()), 0.90, "Error: El valor del ratio de asistencias por pérdida no es el correcto")

    def test_set_ts(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_ts()
        self.assertEqual(float(tas.get_ts()), 54.85, "Error: El valor del TS% no es el correcto")

    def test_set_ortg(self):
        params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
        data = DataPreGame(params)
        tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
        tas.set_possessions()
        tas.set_ortg()
        self.assertEqual(float(tas.get_ortg()), 109.32, "Error: El valor del ORTG no es el correcto")

    # def test_set_drtg(self):
    #     os.chdir("../")
    #     params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
    #     data = DataPreGame(params)
    #     tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
    #     tas.set_possessions()
    #     tas.set_drtg()
    #     self.assertEqual(float(tas.get_drtg()), 78.77, "Error: El valor del ORTG no es el correcto")

    # def test_set_nrtg(self):
    #     os.chdir("../")
    #     params = {"report" : 1, "league" : COMPETITIONS.LF1, "home": 770, "away": 769}
    #     data = DataPreGame(params)
    #     tas = TeamAS(data.home_standard_stats.get_result().getData()[0], data.home_opps_standard_stats.get_result().getData()[0])
    #     tas.set_possessions()
    #     tas.set_ortg()
    #     tas.set_drtg()
    #     tas.set_nrtg()
    #     self.assertEqual(float(tas.get_nrtg()), 30.55, "Error: El valor del ORTG no es el correcto")






if __name__== "__main__":
    unittest.main()

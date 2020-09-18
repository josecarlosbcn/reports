import unittest
import os
import pandas as pd
from reports.data.data_player_accumulated import DataPlayerAccumulated
from reports.pdf.pdf_player_accumulated import PDFPlayerAccumulated
from decimal import Decimal
from constants import COMPETITIONS
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA


class TestDataPlayerAccumulated(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
        pd.set_option("display.max_columns", None)

    def test_get_player_name(self):
        params = {'report': 5, 'id': 2063, 'id_player_team': None, 'date': '19/08/2020', 'id_season': 45, 'competition': 'FEB-LF1'}
        d = DataPlayerAccumulated(params)
        name = d.name
        self.assertEqual(name, "BUCH ROSELL, ROSO", "test_get_player_name:: El nombre de la jugadora NO es correcto")

    def test_get_player_standard_stats(self):
        params = {'report': 5, 'id': 2063, 'id_player_team': None, 'date': '19/08/2020', 'id_season': 45, 'competition': 'FEB-LF1'}
        d = DataPlayerAccumulated(params)
        self.assertEqual(len(d.pss), 2, "test_get_player_standard_stats:: El número de filas devultas buscando por id NO es el correecto")
        params = {'report': 5, 'id': None, 'id_player_team': 10778, 'date': '19/08/2020', 'id_season': 45, 'competition': 'FEB-LF1'}
        d = DataPlayerAccumulated(params)
        self.assertEqual(len(d.pss), 1, "test_get_player_standard_stats:: El número de filas devultas buscandor por id_player_team NO es el correecto")
        self.assertEqual(d.pss[0]["games"], 7, "test_get_player_standard_stats:: El número de partidos jugados NO es el correcto")

    def test_get_player_advanced_stats(self):
        params = {'report': 5, 'id': 2063, 'id_player_team': None, 'date': '19/08/2020', 'id_season': 45, 'competition': 'FEB-LF1'}
        d = DataPlayerAccumulated(params)
        self.assertEqual(len(d.pas), 2, "test_get_player_advanced_stats:: El número de filas devultas buscando por id NO es el correecto")
        params = {'report': 5, 'id': None, 'id_player_team': 10778, 'date': '19/08/2020', 'id_season': 45, 'competition': 'FEB-LF1'}
        d = DataPlayerAccumulated(params)
        self.assertEqual(len(d.pas), 1, "test_get_player_advanced_stats:: El número de filas devultas buscandor por id_player_team NO es el correecto")
        self.assertEqual(d.pas[0]["game_score"], round(Decimal(5.01), 2), "test_get_player_advanced_stats:: El game_score NO es el correcto")

    def test_create_pdf(self):
        params = {'report': 5, "type": "player_acc", 'id': 2063, 'id_player_team': None, 'date': '19/08/2020', 'id_season': 45, 'competition': 'FEB-LF1'}
        d = DataPlayerAccumulated(params)
        pdf = PDFPlayerAccumulated(params, d)

    def test_players_from_team(self):
        params = {'report': 5, "destiny": 770, "type": "player_acc", 'id': 2063, 'id_player_team': None, 'date': '19/08/2020', 'id_season': 45, 'competition': 'FEB-LF1'}
        args = [params["destiny"]]
        if params["competition"] == COMPETITIONS.LF1 or params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "team.players=")
        else:
            data = SearchDataFIBA(args, "team.players=")
        players = data.get_result().getData()
        for player in players:
            args = {
                "type": "player_acc",
                "destiny": params["destiny"],
                "competition": params["competition"],
                "id": None,
                "id_player_team": player["id"],
                "id_season": params["id_season"],
                "date": params["date"]
            }
            data = DataPlayerAccumulated(args)
            pdf = PDFPlayerAccumulated(args, data)

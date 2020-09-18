import unittest
from com.shotchart.shots.team_shots import TeamShots
from com.shotchart.shots.player_shots import PlayerShots
from constants import COMPETITIONS, IMAGES
import os
import pandas as pd
import PIL.Image
from com.shotchart.images.shotchartimage import ShotChartImage


class TestTeamShots(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
        pd.set_option("display.max_columns", None)

    # def test_get_player_data(self):
    #     ts =TeamShots(108, COMPETITIONS.EUROCUP)
    #     ps = PlayerShots(ts.get_player_data(204187), 108, COMPETITIONS.EUROCUP)
    #     self.assertEqual(228, ps.player_total_shots(), "ERROR(test_get_player_data): El número de lanzamientos del id_player_Team con id 204187 no es correcto")
    #
    # def test_team_total_scored_shots_from_position(self):
    #     ts = TeamShots(770, COMPETITIONS.LF1)
    #     self.assertEqual(ts.team_total_shots_from_position('C3R'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde C3R no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('ER3'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde ER3 no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('Ce3R'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde Ce3R no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('MBR'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MBR no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('MER'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MER no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('PR'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde PR no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('PC'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde PC no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('PL'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde PL no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('MEL'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MEL no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('MBL'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MBL no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('Ce3L'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde Ce3L no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('E3L'), 119, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde E3L no son correctos")
    #     self.assertEqual(ts.team_total_shots_from_position('C3L'), 118, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde C3L no son correctos")
    #
    # def test_team_total_scored_shots_from_position(self):
    #     ts = TeamShots(770, COMPETITIONS.LF1)
    #     self.assertEqual(ts.team_total_scored_shots_from_position('C3R'), 55, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde C3R no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('ER3'), 47, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde ER3 no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('Ce3R'), 59, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde Ce3R no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('MBR'), 48, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MBR no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('MER'), 61, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MER no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('PR'), 51, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde PR no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('PC'), 65, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde PC no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('PL'), 59, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde PL no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('MEL'), 56, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MEL no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('MBL'), 60, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MBL no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('Ce3L'), 55, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde Ce3L no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('E3L'), 51, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde E3L no son correctos")
    #     self.assertEqual(ts.team_total_scored_shots_from_position('C3L'), 54, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde C3L no son correctos")
    #
    # def test_team_total_failed_shots_from_position(self):
    #     ts = TeamShots(770, COMPETITIONS.LF1)
    #     self.assertEqual(ts.team_total_failed_shots_from_position('C3R'), 64, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde C3R no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('ER3'), 72, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde ER3 no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('Ce3R'), 60, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde Ce3R no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('MBR'), 71, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MBR no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('MER'), 58, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MER no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('PR'), 68, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde PR no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('PC'), 54, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde PC no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('PL'), 60, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde PL no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('MEL'), 63, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MEL no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('MBL'), 59, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde MBL no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('Ce3L'), 64, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde Ce3L no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('E3L'), 68, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde E3L no son correctos")
    #     self.assertEqual(ts.team_total_failed_shots_from_position('C3L'), 64, "ERROR(test_team_total_scored_shots_from_position): Los lanzamientos realizados desde C3L no son correctos")

    def test_set_positions(self):
        ts = TeamShots(770, COMPETITIONS.LF1)
        ts.get_all_colors()

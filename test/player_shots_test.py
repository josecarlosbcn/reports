import unittest
from com.shotchart.shots.team_shots import TeamShots
from com.shotchart.shots.player_shots import PlayerShots
from constants import COMPETITIONS
import os
import pandas as pd


class TestPlayerShots(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
        pd.set_option("display.max_columns", None)

    # def test_total_shots(self):
    #     ts =TeamShots(108, COMPETITIONS.EUROCUP)
    #     ps = PlayerShots(ts.get_player_data(204187), ts.id_team_club, ts.competition)
    #     self.assertEqual(ps.player_total_shots(), 228, "ERROR(test_total_shots): El número de lanzamientos no es el correcto")
    #
    # def test_player_total_shots_from_position(self):
    #     ts =TeamShots(108, COMPETITIONS.EUROCUP)
    #     ps = PlayerShots(ts.get_player_data(204187), ts.id_team_club, ts.competition)
    #     self.assertEqual(ps.player_total_shots_from_position("C3R"), 21, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde C3R no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("ER3"), 16, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde ER3 no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("Ce3R"), 20, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde Ce3R no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("MBR"), 20, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MBR no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("MER"), 16, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MER no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("PR"), 13, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde PR no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("PC"), 18, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde PC no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("PL"), 16, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde PL no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("MEL"), 21, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MEL no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("MBL"), 16, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MBL no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("Ce3L"), 17, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde Ce3L no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("E3L"), 17, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde E3L no es correcto")
    #     self.assertEqual(ps.player_total_shots_from_position("C3L"), 17, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde C3L no es correcto")
    #
    # def test_player_total_scored_shots_from_position(self):
    #     ts =TeamShots(108, COMPETITIONS.EUROCUP)
    #     ps = PlayerShots(ts.get_player_data(204187), ts.id_team_club, ts.competition)
    #     self.assertEqual(ps.player_total_scored_shots_from_position("C3R"), 13, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde C3R no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("ER3"), 8, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde ER3 no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("Ce3R"), 16, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde Ce3R no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("MBR"), 13, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MBR no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("MER"), 6, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MER no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("PR"), 7, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde PR no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("PC"), 11, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde PC no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("PL"), 9, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde PL no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("MEL"), 9, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MEL no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("MBL"), 12, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MBL no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("Ce3L"), 12, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde Ce3L no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("E3L"), 14, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde E3L no es correcto")
    #     self.assertEqual(ps.player_total_scored_shots_from_position("C3L"), 9, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde C3L no es correcto")
    #
    # def test_player_total_failed_shots_from_position(self):
    #     ts = TeamShots(108, COMPETITIONS.EUROCUP)
    #     ps = PlayerShots(ts.get_player_data(204187), ts.id_team_club, ts.competition)
    #     self.assertEqual(ps.player_total_failed_shots_from_position("C3R"), 8, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde C3R no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("ER3"), 8, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde ER3 no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("Ce3R"), 4, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde Ce3R no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("MBR"), 7, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MBR no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("MER"), 10, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MER no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("PR"), 6, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde PR no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("PC"), 7, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde PC no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("PL"), 7, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde PL no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("MEL"), 12, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MEL no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("MBL"), 4, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde MBL no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("Ce3L"), 5, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde Ce3L no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("E3L"), 3, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde E3L no es correcto")
    #     self.assertEqual(ps.player_total_failed_shots_from_position("C3L"), 8, "ERROR(player_tota_shots_from_position): El total de lanzamientos realizdos desde C3L no es correcto")

    def test_set_positions(self):
        ts = TeamShots(108, COMPETITIONS.EUROCUP)
        ps = PlayerShots(ts.get_player_data(204187), ts.id_team_club, ts.competition)

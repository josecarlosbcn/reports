from com.shotchart.shots.shots import Shots
from constants import COMPETITIONS
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA
import pandas as pd


class PlayerShots(Shots):
    def __init__(self, params):
        super().__init__(params["competition"])
        self.params = params
        self.df = self.get_shots()
        self.add_column("position")
        self.set_positions()

    def player_total_shots(self):
        '''Total shootings made by a team'''
        return len(self.df)

    def player_total_shots_from_position(self, position):
        data = self.df.query(f"position == '{position}'")
        return len(data)

    def player_total_scored_shots_from_position(self, position):
        data = self.df.query(f"position == '{position}' and m == 1")
        return len(data)

    def player_total_failed_shots_from_position(self, position):
        data = self.df.query(f"position == '{position}' and m == 0")
        return len(data)

    def get_shots(self):
        '''
            Get all shots made it by a player. It doesn't matter if the player played in one or more teams
        :return: A DataFrame
        '''
        if self.params["id"] is not None:
            args = [self.params["id"], self.params["id_season"]]
            if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
                data = SearchData(args, "feb.player.shots.season=")
            else:
                data = SearchDataFIBA(args, "fiba.player.accumulated=")
        else:
            if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
                args = [self.params["id_player_team"]]
                data = SearchData(args, "feb.player.shots=")
            else:
                args = [self.params["id_player_team"], self.params["id_season"]]
                data = SearchDataFIBA(args, "fiba.player.accumulated=")
        return pd.DataFrame(data.get_result().getData())

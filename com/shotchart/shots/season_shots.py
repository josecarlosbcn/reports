from constants import COMPETITIONS
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA
from com.shotchart.shots.shots import Shots
import pandas as pd


class SeasonShots(Shots):
    def __init__(self, competition, id_season):
        super().__init__(competition)
        self.id_season  = id_season
        self.df = SeasonShots.get_shots_from_season(competition, id_season)
        self.add_column("position")
        self.set_positions()

    @staticmethod
    def get_shots_from_season(competition, id_season):
        args = [id_season]
        if competition == COMPETITIONS.LF1:
            data = SearchData(args, "feb.season.shots=")
        else:
            if competition == COMPETITIONS.EUROLEAGUE or competition == COMPETITIONS.EUROCUP:
                data = SearchDataFIBA(args, "fiba.season.shots=")
        return pd.DataFrame(data.get_result().getData())

    def season_total_shots_from_position(self, position):
        data = self.df.query(f"position == '{position}'")
        return len(data)

    def season_total_shots_scored_from_position(self, position):
        data = self.df.query(f"position == '{position}' and m == 1")
        return len(data)

    def season_total_shots_failed_from_position(self, position):
        data = self.df.query(f"position == '{position}' and m == 0")
        return len(data)

    def season_total_shots(self):
        '''Total shots made in a whole season'''
        return len(self.df)

from constants import COMPETITIONS
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA
from com.shotchart.shots.shots import Shots
import pandas as pd


class TeamShots(Shots):
    def __init__(self, id_team_club, competition):
        super().__init__(competition)
        self.id_team_club = id_team_club
        self.df = TeamShots.get_shots_from_team(id_team_club, competition)
        self.add_column("position")
        self.set_positions()

    @staticmethod
    def get_shots_from_team(id_team_club, competition):
        '''Returns a dataFrame with the shots made it for all the players of a team in a whole season'''
        args = [id_team_club]
        data = None
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            data = SearchData(args, "feb.team.shots=")
        else:
            if competition == COMPETITIONS.EUROLEAGUE or competition == COMPETITIONS.EUROCUP:
                data = SearchDataFIBA(args, "fiba.team.shots=")
        return pd.DataFrame(data.get_result().getData())

    def get_shots_from_month(self, id_team_club, competition, month, year):
        '''
            Returns a DataFrame with the shots of a team in a month played
        :param id_team_club:
        :param competition:
        :param month:
        :param year:
        :return:
        '''
        args = [id_team_club, year, month]
        data = None
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            data = SearchData(args, "team.shots.by.month=")
        else:
            data = SearchDataFIBA(args, "team.shots.by.month=")
        self.df = pd.DataFrame(data.get_result().getData())
        #We have a new dataframe, so we have to add "position" column and set positions
        self.add_column("position")
        self.set_positions()

    def get_opp_shots_from_month(self, id_team_club, competition, month, year):
        args = [id_team_club, id_team_club, id_team_club, year, month]
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            data = SearchData(args, "opp.shots.by.month=")
        else:
            data = SearchDataFIBA(args, "opp.shots.by.month=")
        self.df = pd.DataFrame(data.get_result().getData())
        #We have a new dataframe, so we have to add "position" column and set positions
        self.add_column("position")
        self.set_positions()


    def get_player_data(self, id_player_team):
        '''Return the shots made it by a player'''
        if self.competition == COMPETITIONS.LF1 or self.competition == COMPETITIONS.LF2:
            data = self.df.query(f"id_player_team == {id_player_team}")
        else:
            data = self.df.query(f"id_fiba == {id_player_team}")
        return data

    # def team_total_shots(self):
    #     '''Total shootings made by a team'''
    #     return len(self.df)

    def team_total_shots_from_position(self, position):
        #filter = self.df["position"] == position
        #self.df.where(filter, inplace=True)
        data = self.df.query(f"position == '{position}'")
        # data = self.df.dropna(thresh=len(self.df.columns))
        return len(data)

    def team_total_scored_shots_from_position(self, position):
        data = self.df.query(f"position == '{position}' and m == 1")
        return len(data)

    def team_total_failed_shots_from_position(self, position):
        data = self.df.query(f"position == '{position}' and m == 0")
        return len(data)

    # def team_total_scored_shots(self):
    #     '''Return the total of shots scored by a tam'''
    #     data= self.df.query("m == 1")
    #     return len(data)
    #
    # def team_total_failed_shots(self):
    #     '''Return the total of shots failed by a team'''
    #     data = self.df.query("m == 0")
    #     return len(data)











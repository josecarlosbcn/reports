from reports.data.data import Data
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA
from constants import COMPETITIONS
import pandas as pd


class DataPlayerAccumulated(Data):
    def __init__(self, params):
        super().__init__(params)
        self.name = self.get_player_name(self.params["id"])
        self.name_url = self.get_player_name_url(self.params["id"])
        self.season = self.get_season_name(self.params["id"], self.params["id_season"])
        self.pss = self.get_player_standard_stats()
        self.pas = self.get_player_advanced_stats()

    def get_player_name(self, id):
        '''
            Method which returns the name of a player through it's id
        :param id:  id of the player (tbl003_player)
        :return:    A string with the name of the player
        '''
        if id is not None:
            args = [id]
            if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
                data = SearchData(args, "player.name=")
            else:
                data = SearchDataFIBA(args, "player.name=")
            return data.get_result().getData()[0]["name"]
        else:
            return None

    def get_player_name_url(self, id):
        '''
            Method which returns the name of a player through it's id
        :param id:  id of the player (tbl003_player)
        :return:    A string with the name of the player
        '''
        if id is not None:
            args = [id]
            if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
                data = SearchData(args, "player.name=")
            else:
                data = SearchDataFIBA(args, "player.name=")
            return data.get_result().getData()[0]["name_url"]
        else:
            return None

    def get_season_name(self, id, id_season):
        '''
            Method which returns the name of the season where have been played by a player
        :param id:  id of the player (tbl003_player)
        :return:    A string with the name of the season
        '''
        if id is not None:
            args = [id, id_season]
            if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
                data = SearchData(args, "season.name=")
            else:
                data = SearchDataFIBA(args, "season.name=")
            return data.get_result().getData()[0]["description"]
        else:
            return None

    def get_player_standard_stats(self):
        '''
            Get standard stats for a whole season, it doesn't matter if the player has played in one team or more than one team
        :return: A list of dicctionaries with standard stats
        '''
        if self.params["id"] is not None:
            args = [self.params["id"], self.params["id_season"]]
            if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
                data = SearchData(args, "player.standard.stats.by.id=")
            else:
                data = SearchDataFIBA(args, "player.standard.stats.by.id=")
        else:
            args = [self.params["id_player_team"]]
            if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
                data = SearchData(args, "player.standard.stats.by.id_player_team=")
            else:
                data = SearchDataFIBA(args, "player.standard.stats.by.id_player_team=")
            self.name = self.get_player_name(data.get_result().getData()[0]["id_player"])
            self.name_url = self.get_player_name_url(data.get_result().getData()[0]["id_player"])
            self.season = self.get_season_name(data.get_result().getData()[0]["id_player"], self.params["id_season"])
        return data.get_result().getData()

    def get_player_advanced_stats(self):
        '''
            Get advanced stats for a whole season. It doesn't matter if the player has played in one team or more than one team.
        :return: A list of dictionaries with advanced stats
        '''
        if self.params["id"] is not None:
            args = [self.params["id"], self.params["id_season"]]
            if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
                data = SearchData(args, "player.advaced.stats.by.id=")
            else:
                data = SearchDataFIBA(args, "player.advaced.stats.by.id=")
        else:
            args = [self.params["id_player_team"]]
            if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
                data = SearchData(args, "player.advaced.stats.by.id_player_team=")
            else:
                data = SearchDataFIBA(args, "player.advaced.stats.by.id_player_team=")
                self.name = self.get_player_name(data.get_result().getData()[0]["id_player"])
        return data.get_result().getData()

    # def get_shots(self):
    #     '''
    #         Get all shots made it by a player. It doesn't matter if the player played in one or more teams
    #     :return: A DataFrame
    #     '''
    #     if self.params["id"] is not None:
    #         args = [self.params["id"], self.params["id_season"]]
    #         if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
    #             data = SearchData(args, "feb.player.accumulated=")
    #         else:
    #             data = SearchDataFIBA(args, "feb.player.accumulated=")
    #     else:
    #         args = [self.params["id_player_team"]]
    #         if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
    #             data = SearchData(args, "fiba.player.accumulated=")
    #         else:
    #             data = SearchDataFIBA(args, "fiba.player.accumulated=")
    #     return pd.DataFrame(data.get_result().getData())

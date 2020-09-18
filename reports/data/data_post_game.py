from reports.data.data import Data
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA
from constants import COMPETITIONS


class DataPostGame(Data):
    def __init__(self, params):
        super().__init__(params)
        if "id_game" not in params:
            self.game = self.get_id_game(params)
            self.id_game = self.game[len(self.game)-1]["id"]
        else:
            self.id_game = params["id_game"]
        #Recuperamos datos de estadísticas estandard del equipo local y visitante
        self.home_standard_stats = self.get_team_standard_stats(params["home"])
        self.away_standard_stats = self.get_team_standard_stats(params["away"])
        #Recuperamos datos de estadísticas avanzadas del equipo local y visitante
        self.home_advanced_stats = self.get_team_advanced_stats(params["home"])
        self.away_advanced_stats = self.get_team_advanced_stats(params["away"])
        #Recuperamos datos de estadísticas estandard de los jugadores local y visitante
        self.home_pt_ss = self.get_players_standard_stats(params["home"])
        self.away_pt_ss = self.get_players_standard_stats(params["away"])
        #Recuperamos datos de estadísticas avanzadas de los jugadores local y visitantes
        self.home_pt_as = self.get_players_advanced_stats(params["home"])
        self.away_pt_as = self.get_players_advanced_stats(params["away"])

    @staticmethod
    def get_id_game(params):
        '''Returns last game played by two teams'''
        args = [params["home"], params["away"]]
        if params["competition"] == COMPETITIONS.LF1 or params["competition"] == COMPETITIONS.LF2:
            return SearchData(args, "game.last=").get_result().getData()
        if params["competition"] == COMPETITIONS.EUROLEAGUE or params["competition"] == COMPETITIONS.EUROCUP:
            return SearchDataFIBA(args, "game.last=").get_result().getData()

    def get_team_standard_stats(self, id_team):
        '''Returns standard stats of a team in a game'''
        args = [self.id_game, id_team]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            return SearchData(args, "team.std.stats.by.game=").get_result().getData()
        if self.params["competition"] == COMPETITIONS.EUROLEAGUE or self.params["competition"] == COMPETITIONS.EUROCUP:
            return SearchDataFIBA(args, "team.std.stats.by.game=").get_result().getData()

    def get_team_advanced_stats(self, id_team):
        '''Returns advanced stats of a team in a game'''
        args = [self.id_game, id_team]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            return SearchData(args, "team.adv.stats.by.game=").get_result().getData()
        if self.params["competition"] == COMPETITIONS.EUROLEAGUE or self.params["competition"] == COMPETITIONS.EUROCUP:
            return SearchDataFIBA(args, "team.adv.stats.by.game=").get_result().getData()

    def get_players_standard_stats(self, id_team):
        args = [id_team, self.id_game]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            return SearchData(args, "feb.players.std.stats.by.game=").get_result().getData()
        if self.params["competition"] == COMPETITIONS.EUROLEAGUE or self.params["competition"] == COMPETITIONS.EUROCUP:
            return SearchDataFIBA(args, "fiba.players.std.stats.by.game=").get_result().getData()

    def get_players_advanced_stats(self, id_team):
        args = [id_team, self.id_game]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            return SearchData(args, "feb.players.adv.stats.by.game=").get_result().getData()
        if self.params["competition"] == COMPETITIONS.EUROLEAGUE or self.params["competition"] == COMPETITIONS.EUROCUP:
            return SearchDataFIBA(args, "fiba.players.adv.stats.by.game=").get_result().getData()

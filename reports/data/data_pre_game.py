from reports.data.data import Data
from constants import COMPETITIONS
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA


class DataPreGame(Data):
    def __init__(self, params):
        super().__init__(params)
        #Recuperar datos de estadísticas estandard del equipo local y visitante
        self.home_standard_stats = self.team_standard_stats(params["home"], params["competition"])
        self.away_standard_stats = self.team_standard_stats(params["away"], params["competition"])
        #Recuperar datos de estadísticas estándard de los equipos oponentes del equipo local y visitante
        self.home_opps_standard_stats = self.opp_standard_stats(params["home"], params["competition"])
        self.away_opps_standard_stats = self.opp_standard_stats(params["away"], params["competition"])
        #Recuperar datos de estadísticas avanzadas del equipo local y visitante
        self.home_advanced_stats = self.team_advanced_stats(params["home"], params["competition"])
        self.away_advanced_stats = self.team_advanced_stats(params["away"], params["competition"])
        #Recuperar datos de estadísticas estandard de las jugadoras del equipo local y visitante
        self.home_pt_ss = self.players_team_ss(params["home"], params["competition"])
        self.away_pt_ss = self.players_team_ss(params["away"], params["competition"])
        #Recuperar datos de estadísticas avanzadas de las jugadoras del equipo local y visitante
        self.players_home_as = self.players_team_as(params["home"], params["competition"])
        self.players_away_as = self.players_team_as(params["away"], params["competition"])

    @staticmethod
    def team_advanced_stats(id_team, competition) -> []:
        '''Return the standard stats from a team in a whole season'''
        args = [id_team]
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            return SearchData(args, "team.adv.stats=").get_result().getData()
        if competition == COMPETITIONS.EUROLEAGUE or competition == COMPETITIONS.EUROCUP:
            return  SearchDataFIBA(args, "team.adv.stats=").get_result().getData()

    @staticmethod
    def team_standard_stats(id_team, competition) -> []:
        '''Return the standard stats from a team in a whole season'''
        args = [id_team]
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            return SearchData(args, "team.std.stats=").get_result().getData()
        if competition == COMPETITIONS.EUROLEAGUE or competition == COMPETITIONS.EUROCUP:
            return  SearchDataFIBA(args, "team.std.stats=").get_result().getData()

    @staticmethod
    def opp_standard_stats(id_team, competition) -> []:
        '''Return the standard stats of opponents of a team in a whole season'''
        args = [id_team]
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            return SearchData(args, "opp.team.std.stats=").get_result().getData()
        if competition == COMPETITIONS.EUROLEAGUE or competition == COMPETITIONS.EUROCUP:
            return  SearchDataFIBA(args, "opp.team.std.stats=").get_result().getData()

    @staticmethod
    def players_team_ss(id_team, competition) -> []:
        '''Return standard stats of all the players of a team for a whole season'''
        args = [id_team]
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            return SearchData(args, "player.std.stats=").get_result().getData()
        if competition == COMPETITIONS.EUROLEAGUE or competition == COMPETITIONS.EUROCUP:
            return SearchDataFIBA(args, "player.std.stats=").get_result().getData()

    @staticmethod
    def players_team_as(id_team, competition) -> []:
        '''Returns advanced stats of all the players of a team for a whole season'''
        args = [id_team]
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            return SearchData(args, "player.adv.stats=").get_result().getData()
        if competition == COMPETITIONS.EUROLEAGUE or competition == COMPETITIONS.EUROCUP:
            return SearchDataFIBA(args, "player.adv.stats=").get_result().getData()

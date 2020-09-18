from reports.data.data import Data
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA
from constants import COMPETITIONS
from com.statistics.advanced.team_advanced_stats import TeamAS
from com.statistics.advanced.player_advanced_stats import PlayerAS


class DataMonthly(Data):
    def __init__(self, params):
        super().__init__(params)
        #Recuperar datos de estadísticas estandard del equipo local y visitante
        self.team_standard_stats = self.team_standard_stats(params["home"], params["competition"], params["month"], params["year"])
        #self.away_standard_stats = self.team_standard_stats(params["away"], params["competition"], params["month"], params["year"])
        #Recuperar datos de estadísticas estándard de los equipos oponentes del equipo local y visitante
        self.opps_standard_stats = self.opp_standard_stats(params["home"], params["competition"], params["month"], params["year"])
        #self.away_opps_standard_stats = self.opp_standard_stats(params["away"], params["competition"], params["month"], params["year"])
        #Recuperar datos de estadísticas avanzadas del equipo local y visitante
        self.team_advanced_stats = TeamAS(self.team_standard_stats, self.opps_standard_stats)
        self.opp_advanced_stats = TeamAS(self.opps_standard_stats, self.team_standard_stats)
        #Recuperar datos de estadísticas estandard de las jugadoras del equipo local y visitante
        self.players_team_ss = self.players_team_ss(params["home"], params["competition"], params["month"], params["year"])
        #self.away_pt_ss = self.players_team_ss(params["away"], params["competition"], params["month"], params["year"])
        #Generamos una lista de objetos PlayerAS para cada jugadora del equipo local y visitante
        self.players_team_as = self.players_team_as(self.players_team_ss, self.team_standard_stats,
                                                    self.opps_standard_stats, self.team_advanced_stats.get_possessions())
        #self.players_away_as = self.players_team_as(self.away_pt_ss.get_result().getData(), self.away_standard_stats.get_result().getData()[0],
        #                                            self.away_opps_standard_stats.get_result().getData()[0], self.away_advanced_stats.get_possessions())
        self.abrev = self.get_abrev(params["home"], params["competition"])

    def get_abrev(self, id_team, competition):
        args = [id_team]
        if competition == COMPETITIONS.LF1 or competition.LF2:
            data = SearchData(args, "team.abrev=")
        else:
            data = SearchDataFIBA(args, "team.abrev=")
        return data.get_result().getData()[0]["abrev"]

    @staticmethod
    def team_standard_stats(id_team, competition, month, year):
        '''Return the standard stats from a team in a whole season'''
        args = [id_team, id_team, year, month, id_team]
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            return SearchData(args, "team.std.stats.by.month=").get_result().getData()[0]
        if competition == COMPETITIONS.EUROLEAGUE or competition == COMPETITIONS.EUROCUP:
            return  SearchDataFIBA(args, "team.std.stats.by.month=").get_result().getData()[0]

    @staticmethod
    def opp_standard_stats(id_team, competition, month, year):
        '''Return the standard stats of opponents of a team in a whole season'''
        args = [id_team, id_team, year, month, id_team]
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            return SearchData(args, "opp.team.std.stats.by.month=").get_result().getData()[0]
        if competition == COMPETITIONS.EUROLEAGUE or competition == COMPETITIONS.EUROCUP:
            return  SearchDataFIBA(args, "opp.team.std.stats.by.month=").get_result().getData()[0]

    @staticmethod
    def players_team_ss(id_team, competition, month, year):
        '''Return standard stats of all the players of a team for a whole season'''
        args = [id_team, id_team, id_team, year, month]
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            return SearchData(args, "feb.players.std.stats.by.month=").get_result().getData()
        if competition == COMPETITIONS.EUROLEAGUE or competition == COMPETITIONS.EUROCUP:
            return SearchDataFIBA(args, "fiba.players.std.stats.by.month=").get_result().getData()

    @staticmethod
    def players_team_as(players_ss, team_ss, opp_ss, possessions):
        '''Returns advanced stats of all the players of a team for a whole season'''
        list_players = []
        for player in players_ss:
            pas = PlayerAS(player, team_ss, opp_ss, possessions)
            list_players.append(pas)
        return list_players

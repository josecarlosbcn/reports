from reports.data.data import Data
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA
from constants import COMPETITIONS
import pandas as pd


class DataTeamAccumulated(Data):
    def __init__(self, params):
        super().__init__(params)
        #Listado de partidos
        self.list_games = self.get_list_games(self.params["destiny"])
        #Stadísticas standard equipo
        self.tss = self.get_team_standard_stats(self.params["destiny"])
        #Estadísticas estánard oponentes
        self.oss = self.get_opp_standard_stats(self.params["destiny"])
        #Estadísticas avanzadas equipo
        self.tas = self.get_team_advanced_stats(self.params["destiny"])
        #Estadísticas avanzadas oponentes
        self.oas = self.get_opp_advanced_stats(self.params["destiny"])
        #Carta de tiro
        self.shots = self.get_shots(self.params["destiny"])
        #Abreviatura del equipo
        self.abrev = self.get_abrev(self.params["destiny"], self.params["competition"])
        #Lista de jugadoras
        self.list_players = self.get_players(self.params["destiny"])
        #Puntos por jugadora
        self.points_players = self.get_points_x_player(self.params["destiny"], self.params["competition"])

    def get_list_games(self, id_team):
        '''
            This method returns a DataFrame with the list of games played by a team in a whole season
            :param id_team: id of the team
            :return: DataFrame
        '''
        args = [id_team, id_team, id_team, id_team]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "team.list.games=")
        else:
            data = SearchDataFIBA(args, "team.list.games=")
        return pd.DataFrame(data.get_result().getData())

    def get_team_standard_stats(self, id_team):
        '''
            This method returns a dictionary with standard stats from a team
            :param id_team: Team searched
            :return: Returns a dictionary
        '''
        args = [id_team]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "team.standard.stats=")
        else:
            data = SearchDataFIBA(args, "team.standard.stats=")
        return data.get_result().getData()[0]

    def get_team_advanced_stats(self, id_team):
        '''
            This method returns a dictionary with advanced stats from a team
            :param id_team: Team searched
            :return: Returns a dictionary
        '''
        args = [id_team]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "team.advanced.stats=")
        else:
            data = SearchDataFIBA(args, "team.advanced.stats=")
        return data.get_result().getData()[0]

    def get_opp_standard_stats(self, id_team):
        '''
            This method returns a dictionary with standard stats from opponents of a team
            :param id_team: Team searched
            :return: Returns a dictionary
        '''
        args = [id_team]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "opp.standard.stats=")
        else:
            data = SearchDataFIBA(args, "opp.standard.stats=")
        return data.get_result().getData()[0]

    def get_opp_advanced_stats(self, id_team):
        '''
            This method returns a dictionary with advanced stats from opponents of a team
            :param id_team: Team searched
            :return: Returns a dictionary
        '''
        args = [id_team]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "opp.advanced.stats=")
        else:
            data = SearchDataFIBA(args, "opp.advanced.stats=")
        return data.get_result().getData()[0]

    def get_shots(self, id_team):
        '''
            Devuelve un DataFrame del total de los tiros lanzados por un equipo
            :param id_team: Identificador del equipo sobre el que queremos obtener la informacion
            :return: DaraFrame
        '''
        args = [id_team]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "team.shots=")
        else:
            data = SearchDataFIBA(args, "team.shots=")
        return pd.DataFrame(data.get_result().getData())

    def get_abrev(self, id_team, competition):
        '''
            Devuelve la abreviatra del equipo
            :param id_team: Identificador del equipo del que queremos la abreviatura
            :param competition: Identificador de la competición en la que juega
            :return: Devuelte un string
        '''
        args = [id_team]
        if competition == COMPETITIONS.LF1 or competition.LF2:
            data = SearchData(args, "team.abrev=")
        else:
            data = SearchDataFIBA(args, "team.abrev=")
        return data.get_result().getData()[0]["abrev"]

    def get_players(self, id_team):
        '''
            Devuelve una lista de diccionarios con los datos de las jugadoras del equipo
            :param id_team: Identificador del equipo por el que buscamos las jugadoras
            :return: list
        '''
        args = [id_team]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "team.players=")
        else:
            data = SearchDataFIBA(args, "team.players=")
        return data.get_result().getData()

    def get_points_x_player(self, id_team, competition):
        args = [id_team]
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            data = SearchData(args, "player.total.points=")
        else:
            data = SearchDataFIBA(args, "player.total.points=")
        return data.get_result().getData()

from com.shotchart.shots.shots import Shots
from com.shotchart.shots.shot_colors import ShotColors
from constants import COMPETITIONS
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA
import pandas as pd


class AccumulatedTeamShots(Shots):
    def __init__(self, id_team, competition):
        self.id_team_club = id_team
        self.competition = competition
        sc = ShotColors()
        self.colors = sc.maristas_colors
        self.df = self.get_team_shots(id_team)
        #Add column
        self.df["position"] = None
        #Set positions
        self.set_positions()

    def get_team_shots(self, id_team):
        '''
            Devuelve un DataFrame del total de los tiros lanzados por un equipo
            :param id_team: Identificador del equipo sobre el que queremos obtener la informacion
            :return: DaraFrame
        '''
        args = [id_team]
        if self.competition == COMPETITIONS.LF1 or self.competition == COMPETITIONS.LF2:
            data = SearchData(args, "team.shots=")
        else:
            data = SearchDataFIBA(args, "team.shots=")
        return pd.DataFrame(data.get_result().getData())

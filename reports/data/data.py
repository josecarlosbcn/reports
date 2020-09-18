from ddbb.fiba.data.search import SearchDataFIBA
from ddbb.feb.data.search import SearchData
from constants import COMPETITIONS


class Data():
    def __init__(self, params):
        self.params = params
        self.home_standard_stats = None         #Standard stats of home team
        self.away_standard_stats = None         #Standard stats of away team
        self.home_opps_standard_stats = None    #Standard stats of rivals of home team
        self.away_opps_standard_stats = None    #Standard stats of rivals of away team
        self.home_advanced_stats = None         #Advanced stats of home team
        self.away_advanced_stats = None         #Advanced stats of away team
        self.home_pt_ss = None                  #Standard stats of players of home team
        self.away_pt_ss = None                  #Standard stats of players of away team
        self.home_pt_as = None                  #Advanced stats of players of home team
        self.away_pt_as = None                  #Advanced stats of players of away team




from reports.report import Report
from reports.data.data_pre_game import DataPreGame
from reports.data.data_post_game import DataPostGame
from com.shotchart.shots.team_shots import TeamShots
from reports.pdf.pdf_press_pregame import PDFPressPreGame
from reports.pdf.pdf_press_postgame import PDFPressPostGame
from constants import COMPETITIONS
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA
from reports.pregame import PreGame
from reports.postgame import PostGame


class PressReport(Report):
    def __init__(self, params):
        '''
            Constructor
            :param params: List of variables
            report: type of report
            team: id of the team, could be None when we ask for all the games of a gameday
            competition: value of the constant of the competition selected
            date: date of creation of the report
        '''
        super().__init__(params)
        games = self.searchGames(params)
        for g in games:
            params.update(g)
            if params["report"] == 6 or params["report"] == 7: #pre-game
                self.data = DataPreGame(params)
                self.shots_home = TeamShots(params["home"], params["competition"])
                self.shots_away = TeamShots(params["away"], params["competition"])
                self.home_data = PreGame.get_name_team(params["home"], params["competition"])
                self.away_data = PreGame.get_name_team(params["away"], params["competition"])
            else: #post.game
                self.data = DataPostGame(params)
                self.shots_home = TeamShots(params["home"], params["competition"])
                self.shots_away = TeamShots(params["away"], params["competition"])
                self.home_data = PostGame.get_name_team(params["home"], params["competition"])
                self.away_data = PostGame.get_name_team(params["away"], params["competition"])
            self.build_pdf(params, self.data)

    def build_pdf(self, params, data):
        if params["report"] == 6 or params["report"] == 7:
            args = {
                "type": "preGame",
                "competition": params["competition"],
                "destiny": None,
                "home": params["home"],
                "away": params["away"],
                "date": params["date"],
                "home_team": self.home_data["name"],
                "away_team": self.away_data["name"],
                "home_url": self.home_data["url_name"],
                "away_url": self.away_data["url_name"]
            }
            pdf = PDFPressPreGame(args, data)
        else:
            args = {
                "type": "postGame",
                "competition": params["competition"],
                "destiny": None,
                "home": params["home"],
                "away": params["away"],
                "date": params["date"],
                "home_team": self.home_data["name"],
                "away_team": self.away_data["name"],
                "home_url": self.home_data["url_name"],
                "away_url": self.away_data["url_name"]
            }
            pdf = PDFPressPostGame(args, data)

    def searchGames(self, params):
        '''
            :param params:
                team: id of the team we are going to search for the data of the next game or game played. Its value could be None
            :return: We return next game or games to play or game played or list of games played
        '''
        if params["report"] == 6: #pre-game of a team
            games = PressReport.searchNextGame(params)
        if params["report"] == 7: #pre-game of all games of a gameday
            games = PressReport.searchNextGameDay(params)
        if params["report"] == 8: #post-game of a team
            games = PressReport.searchGamePlayed(params)
        if params["report"] == 9: #post-game of all games of a gameday
            games = PressReport.searchGamesFromGameDay(params)
        return games

    @staticmethod
    def searchNextGame(params):
        '''
            Return a list of dictionaries with the data of next game
            :param params: list with values like
        :return:
        '''
        args = [params["team"], params["team"]]
        if params["competition"] == COMPETITIONS.LF1:
            data = SearchData(args, "feb.lf1.next.game=")
        if params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "feb.lf2.next.game=")
        if params["competition"] == COMPETITIONS.EUROLEAGUE:
            data = SearchDataFIBA(args, "fiba.euroleague.next.game=")
        if params["competition"] == COMPETITIONS.EUROCUP:
            data = SearchDataFIBA(args, "fiba.eurocup.next.game=")
        return data.get_result().getData()

    @staticmethod
    def searchNextGameDay(params):
        '''
            :param params:
                competition: id of competition
            :return: list of dictionaries with the data of all games of next gameday
        '''
        if params["competition"] == COMPETITIONS.LF1:
            data = SearchData(None, "feb.lf1.next.gameday=")
        if params["competition"] == COMPETITIONS.LF2:
            data = SearchData(None, "feb.lf2.next.gameday=")
        if params["competition"] == COMPETITIONS.EUROLEAGUE:
            data = SearchDataFIBA(None, "fiba.euroleague.next.gameday=")
        if params["competition"] == COMPETITIONS.EUROCUP:
            data = SearchDataFIBA(None, "fiba.eurocup.next.gameday=")
        return data.get_result().getData()

    @staticmethod
    def searchGamePlayed(params):
        args = [params["id_game"]]
        if params["competition"] == COMPETITIONS.LF1 or params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "post.game.by.id=")
        else:
            data = SearchDataFIBA(args, "post.game.by.id=")
        return data.get_result().getData()

    @staticmethod
    def searchGamesFromGameDay(params):
        args = [params["id_jornada"]]
        if params["competition"] == COMPETITIONS.LF1 or params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "post.game.by.id.jornada=")
        else:
            data = SearchDataFIBA(args, "post.game.by.id.jornada=")
        return data.get_result().getData()

from reports.report import Report
from reports.data.data_team_accumulated import DataTeamAccumulated
from reports.pdf.pdf_team_accumulated import PDFTeamAccumulated
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA
import locale
from constants import COMPETITIONS
from reports.data.data_player_accumulated import DataPlayerAccumulated
from reports.pdf.pdf_player_accumulated import PDFPlayerAccumulated


class TeamAccumulated(Report):
    def __init__(self, params):
        super().__init__(params)
        print("Team Accumulated Report")
        self.data = DataTeamAccumulated(params)
        self.build_pdf(self.params, self.data)
        #Send PDF
        #self.send_pdf()
        #Remove PDF
        print("TeamAccumulated:: Borramos PDF")
        #os.remove(self.pdf.fileName)
        self.create_players_pdf(params)
        print("TeamAccumulated:: ¡¡¡FIN DE PROCESO!!!")

    def build_pdf(self, params, data_accumulated):
        team = TeamAccumulated.get_name_team(params["destiny"], params["competition"])
        args = {
            "type": "accumulated",
            "destiny": params["destiny"],
            "competition": params["competition"],
            "team_name": team["name"],
            "team_url": team["url_name"],
            "date": params["date"]
        }
        pdf = PDFTeamAccumulated(args, data_accumulated)

    def create_players_pdf(self, params):
        args = [self.params["destiny"]]
        if params["competition"] == COMPETITIONS.LF1 or params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "team.players=")
        else:
            data = SearchDataFIBA(args, "team.players=")
        players = data.get_result().getData()
        for player in players:
            args = {
                "type": "player_acc",
                "destiny": params["destiny"],
                "competition": params["competition"],
                "id": None,
                "id_player_team": player["id"],
                "id_season": params["id_season"],
                "date": params["date"]
            }
            data = DataPlayerAccumulated(args)
            pdf = PDFPlayerAccumulated(args, data)

    def send_pdf(self):
        print("Team Accumulated:: Vamos a enviar un correo con el PDF")
        html = """\
        <html>
            <head></head>
            <body>
                <p>
                    ¡¡¡Hola!!!
                </p>
                <p>
                    Os enviamos el informe de estadísticas acumuladas de vuestro equipo.
                </p>
                <p>
                    Saludos
                </p>
                <p>
                    Basketmetrics.com
                </p>
            </body>
        </html>
        """
        locale.setlocale(locale.LC_TIME, "")
        subject = "Informe acumulado del equipo"
        home_data = TeamAccumulated.get_name_team(self.params["destiny"], self.params["competition"])
        fileName = f"accumulated-{home_data['url_name']}.pdf"
        self.send_mail(subject, html, fileName)

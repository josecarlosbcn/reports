from reports.report import Report
from reports.data.data_post_game import DataPostGame
from com.shotchart.shots.team_shots import TeamShots
from reports.pdf.pdf_postgame import PDFPostGame


class PostGame(Report):
    def __init__(self, params):
        super().__init__(params)
        print("PostGame Report")
        self.data = DataPostGame(params)
        self.shots_home = TeamShots(params["home"], params["competition"])
        self.shots_away = TeamShots(params["away"], params["competition"])
        self.home_data = PostGame.get_name_team(params["home"], params["competition"])
        self.away_data = PostGame.get_name_team(params["away"], params["competition"])
        self.build_pdf(params, self.data)
        #Send PDF
        self.send_pdf()
        #Remove PDF
        print("PostGame:: Borramos PDF")
        #os.remove(self.pdf.fileName)
        print("PostGame:: ¡¡¡FIN DE PROCESO!!!")

    def build_pdf(self, params, data_post_game):
        # home_data = PostGame.get_name_team(params["home"], params["competition"])
        # away_data = PostGame.get_name_team(params["away"], params["competition"])
        # rival_team = home_data["name"] if params["destiny"] == params["home"] else away_data["name"]
        args = {
            "type": "postGame",
            "competition": params["competition"],
            "destiny": params["destiny"],
            "home": params["home"],
            "away": params["away"],
            "date": params["date"],
            "home_team": self.home_data["name"],
            "away_team": self.away_data["name"],
            "home_url": self.home_data["url_name"],
            "away_url": self.away_data["url_name"]
        }
        pdf = PDFPostGame(args, data_post_game)

    def send_pdf(self):
        print("PostGame:: Vamos a enviar un correo con el PDF")
        html = """\
        <html>
            <head></head>
            <body>
                <p>
                    ¡¡¡Hola!!!
                </p>
                <p>
                    Os enviamos el informe post partido de vuestro último partido.
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
        subject = "Informe post partido: " + self.home_data["name"] + " - " + self.away_data["name"]
        fileName = f"postGame-{self.home_data['url_name']}.vs.{self.away_data['url_name']}.pdf"
        self.send_mail(subject, html, fileName)

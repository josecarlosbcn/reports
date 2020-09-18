from reports.report import Report
from reports.data.data_pre_game import DataPreGame
from com.shotchart.shots.team_shots import TeamShots
from reports.pdf.pdf_pregame import PDFPreGame


class PreGame(Report):
    def __init__(self, params):
        super().__init__(params)
        print("PreGame Report")
        self.data = DataPreGame(params)
        self.shots_home = TeamShots(params["home"], params["competition"])
        self.shots_away = TeamShots(params["away"], params["competition"])
        self.home_data = PreGame.get_name_team(params["home"], params["competition"])
        self.away_data = PreGame.get_name_team(params["away"], params["competition"])
        self.build_pdf(params, self.data)
        #Send PDF
        self.send_pdf()
        #Remove PDF
        print("PreGame:: Borramos PDF")
        #os.remove(self.pdf.fileName)
        print("PreGame:: ¡¡¡FIN DE PROCESO!!!")

    def build_pdf(self, params, data_pre_game):
        args = {
            "type": "preGame",
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
        self.pdf = PDFPreGame(args, data_pre_game)

    def send_pdf(self):
        print("PreGame:: Vamos a enviar un correo con el PDF")
        html = """\
        <html>
            <head></head>
            <body>
                <p>
                    ¡¡¡Hola!!!
                </p>
                <p>
                    Os enviamos el informe pre partido previo a vuestro próximo partido.
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
        subject = "Informe pre partido: " + self.home_data["name"] + " - " + self.away_data["name"]
        fileName = f"preGame-{self.home_data['url_name']}.vs.{self.away_data['url_name']}.pdf"
        self.send_mail(subject, html, fileName)

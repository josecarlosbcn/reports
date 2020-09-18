from reports.report import Report
from reports.data.data_monthly import DataMonthly
from reports.pdf.pdf_monthly import PDFMonthly
import datetime
import locale


class Monthly(Report):
    def __init__(self, params):
        super().__init__(params)
        print("Monthly Report")
        self.data = DataMonthly(params)
        self.build_pdf(params, self.data)
        #Send PDF
        self.send_pdf()
        #Remove PDF
        print("Monthly:: Borramos PDF")
        #os.remove(self.pdf.fileName)
        print("Monthly:: ¡¡¡FIN DE PROCESO!!!")

    def build_pdf(self, params, data_monthly):
        home_data = Monthly.get_name_team(params["home"], params["competition"])
        args = {
            "type": "monthly",
            "destiny": params["destiny"],
            "competition": params["competition"],
            "month": params["month"],
            "year": params["year"],
            "home_team": home_data["name"],
            "home_url": home_data["url_name"],
        }
        locale.setlocale(locale.LC_TIME, "")
        d = datetime.date(params["year"], params["month"], 1)
        pdf = PDFMonthly(args, data_monthly)

    def send_pdf(self):
        print("Monthly:: Vamos a enviar un correo con el PDF")
        html = """\
        <html>
            <head></head>
            <body>
                <p>
                    ¡¡¡Hola!!!
                </p>
                <p>
                    Os enviamos el informe mensual de vuestro equipo.
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
        d = datetime.date(self.params["year"], self.params["month"], 1)
        subject = f"Informe mensual {d.strftime('%B/%Y').capitalize()}"
        home_data = Monthly.get_name_team(self.params["home"], self.params["competition"])
        fileName = f"{d.strftime('%B')}-{home_data['url_name']}.pdf"
        self.send_mail(subject, html, fileName)

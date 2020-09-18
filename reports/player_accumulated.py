from reports.report import Report
from reports.data.data_player_accumulated import DataPlayerAccumulated
from reports.pdf.pdf_player_accumulated import PDFPlayerAccumulated
import locale


class PlayerAccumulated(Report):
    def __init__(self, params):
        '''
            Data accumulated of a player in a whole season.
        :param params:
            id or id_player_team can be informed not both
            id: id of player which belongos to table tbl003_player
            date: date of report creation
            destiny: Team which belongs the player. It could be not exists
            id_player_team: id_player which belongs to a team. A player in the same season can have been playing for more than a team.
        '''
        super().__init__(params)
        print("Player Accumulated Report")
        print(f"Params Accumulated Report: {params}")
        self.data = DataPlayerAccumulated(params)
        self.build_pdf(self.params, self.data)
        #Send PDF
        # print("TeamAccumulated:: Vamos a enviar un correo con el PDF")
        # message = "¡¡¡Hola!!!\n\nOs enviamos el informe mensual de vuestro equipo.\n\nSaludos,\n\nBasketmetrics.com"
        # locale.setlocale(locale.LC_TIME, "")
        # subject = "Informe acumulado del equipo"
        # fileName = f"player-accumulated-{self.data.name}.pdf"
        # self.send_mail(subject, message, fileName)
        #Remove PDF
        #print("TeamAccumulated:: Borramos PDF")
        #os.remove(self.pdf.fileName)
        print("PlayerAccumulated:: ¡¡¡HECHO!!!")

    def build_pdf(self, params, data):
        args = {
            "type": "player_acc",
            "destiny": params["destiny"] if "destiny" in params else None,
            "competition": params["competition"],
            "id": params["id"] if self.params["id"] is not None else None,
            "id_player_team": params["id_player_team"] if self.params["id_player_team"] is not None else None,
            "id_season": params["id_season"],
            "date": params["date"]
        }
        pdf = PDFPlayerAccumulated(args, data)

import abc
from ddbb.feb.data.search import SearchData
from ddbb.fiba.data.search import SearchDataFIBA
from constants import COMPETITIONS
from com.mail.mail import Mail


class Report(object, metaclass=abc.ABCMeta):

    def __init__(self, params):
        self.params = params

    @abc.abstractmethod
    def build_pdf(self, params, data = None):
        raise NotImplementedError("Report", "build_pdf", None, "El usuario no ha implementado el método")

    @staticmethod
    def get_name_team(id_team, competition):
        args = [id_team]
        if competition == COMPETITIONS.LF1 or competition == COMPETITIONS.LF2:
            return SearchData(args, "team.name=").get_result().getData()[0]
        else:
            return SearchDataFIBA(args, "team.name=").get_result().getData()[0]

    def send_mail(self, subject, txt, fileName):
        args = self.params["destiny"]
        if self.params["competition"] == COMPETITIONS.LF1 or self.params["competition"] == COMPETITIONS.LF2:
            data = SearchData(args, "subscriptors.emails=")
        else:
            data = SearchDataFIBA(args, "subscriptors.emails=")
        emails = data.get_result().getData()

        for item in emails:
            print(f"Enviamos informe a la cuenta: {item['email']}")
            params = {
                "from" : "basketmetrics@gmail.com",
                "to" : item["email"],
                "subject": subject,
                "message" : txt,
                "fileName" : fileName,
                "routeFile" : f"output/reports/{self.params['destiny']}/"
            }
            mail = Mail(params)
            message = mail.create_message()
            service = mail.get_service()
            mail.send_message(service, "basketmetrics@gmail.com", message)

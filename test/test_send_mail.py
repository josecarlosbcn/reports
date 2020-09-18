import unittest
import os
from com.mail.mail import Mail


class TestSendMail(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))

    def test_send_mail(self):
        txt = """\
        <html>
            <head></head>
            <body>
                <p>
                    Hola, esto es una prueba!!!
                </p>
                <p>
                    Saludos
                </p>
            </body>
        </html>
        """
        subject = "Informe pre partido"
        fileName = "preGame-PERFUMERIAS-AVENIDA.vs.SPAR-CITYLIFT-GIRONA.pdf"
        emails = [{"email" : "josecarlosbcn@gmail.com"}, {"email" : "josecarlosbcn@gmail.com"}]

        for item in emails:
            print(f"Enviamos informe a la cuenta: {item['email']}")
            params = {
                "from" : "basketmetrics@gmail.com",
                "to" : item["email"],
                "subject": subject,
                "message" : txt,
                "fileName" : fileName,
                "routeFile" : "output/reports/770/"
            }
            mail = Mail(params)
            message = mail.create_message()
            service = mail.get_service()
            mail.send_message(service, "basketmetrics@gmail.com", message)

import base64
import logging
import os
import os.path
import pickle
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors
from googleapiclient.discovery import build


class Mail:
    def __init__(self, params):
        '''
        :param params: It's a dictionary with these keys:
        from: Email account from the email is sended
        to: Email account who will receive the email
        subject: Subject of the email
        message: Message of the email.
        game: Next games
        '''
        self.params = params

    @staticmethod
    def get_service():
        """Gets an authorized Gmail API service instance.

        Returns:
            An authorized Gmail API service instance..
        """

        # If modifying these scopes, delete the file token.pickle.
        SCOPES = [
            #'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.send',
        ]
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'com/mail/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('gmail', 'v1', credentials=creds)
        return service

    @staticmethod
    def send_message(service, sender, message):
      """Send an email message.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

      Returns:
        Sent Message.
      """
      try:
        sent_message = (service.users().messages().send(userId=sender, body=message)
                   .execute())
        logging.info('Message Id: %s', sent_message['id'])
        return sent_message
      except errors.HttpError as error:
        logging.error('An HTTP error occurred: %s', error)

    def create_message(self):
        """Create a message for an email.

        Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

        Returns:
        An object containing a base64url encoded email object.
        """
        #message = MIMEText(message_text)
        message = MIMEMultipart()
        message['from'] = self.params["from"]
        message['to'] = self.params["to"]
        message['subject'] = self.params["subject"]
        message.attach(MIMEText(self.params["message"], "html"))
        routeFile = self.params["routeFile"] + self.params["fileName"]
        fileName = self.params["fileName"]
        # Open PDF file in binary mode
        with open(routeFile, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {fileName}",
        )
        # Add attachment to message and convert message to string
        message.attach(part)
        s = message.as_string()
        b = base64.urlsafe_b64encode(s.encode('utf-8'))
        return {'raw': b.decode('utf-8')}


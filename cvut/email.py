import os
from flask import Flask
from flask_mail import Mail, Message, Attachment


__all__ = ['EmailReporter', ]


class EmailReporter(object):
    def __init__(self, username, password, receivers):
        assert isinstance(receivers, list)
        self.receivers = receivers
        mail_settings = {
            "MAIL_SERVER": 'smtp.gmail.com',
            "MAIL_PORT": 465,
            "MAIL_USE_TLS": False,
            "MAIL_USE_SSL": True,
            "MAIL_USERNAME": username,
            "MAIL_PASSWORD": password,
            "MAIL_ASCII_ATTACHMENTS": True
        }
        self.app = Flask(__name__)
        self.app.config.update(mail_settings)
        self.mail = Mail(self.app)

    def __call__(self, subject, body, files=None):
        with self.app.app_context():
            # Get attachment files
            attachments = None

            if files is not None:
                attachments = []
                for file in files:
                    filename = os.path.basename(file)
                    data = self.app.open_resource(file).read()
                    attachments.append(Attachment(
                        filename, 'text/plain', data))

            # Create message
            msg = Message(
                subject=subject,
                sender=self.app.config.get("MAIL_USERNAME"),
                recipients=self.receivers,
                body=body,
                attachments=attachments)

            # Send email
            self.mail.send(msg)

import abc

import sendgrid
from flask import Flask
from sendgrid.helpers.mail import Content, Email, Mail, To


class AbstractMailService(abc.ABC):
    @abc.abstractmethod
    def send(self, _from: str, to: str, subject: str, content: str):
        raise NotImplementedError


class SendGridMailService(AbstractMailService):
    def __init__(self, app: Flask = None) -> None:
        self.__app = app

    def init_app(self, app: Flask):
        self.__app = app

    def send(self, _from: str, to: str, subject: str, content: str):
        sg = sendgrid.SendGridAPIClient(
            api_key=self.__app.config["SENDGRID_API_KEY"]
        )
        text_content = Content("text/plain", content)
        mail_json = Mail(Email(_from), To(to), subject, text_content).get()
        return sg.send(mail_json)

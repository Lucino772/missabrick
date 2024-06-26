from typing import Any

import sendgrid
from flask import current_app
from sendgrid.helpers.mail import Content, Email, Mail, To


class MailService:
    def send(self, _from: str, to: str, subject: str, content: str) -> Any:
        sg = sendgrid.SendGridAPIClient(api_key=current_app.config["SENDGRID_API_KEY"])
        text_content = Content("text/plain", content)
        mail_json = Mail(Email(_from), To(to), subject, text_content).get()
        return sg.send(mail_json)

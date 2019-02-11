# -*- coding: utf-8 -*-
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class MessageHandler:

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get("url")
        self.port = kwargs.get("port")
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")
        self.sender = kwargs.get("sender")

    def _send_email(self, message, subject, recipients):
        subject = subject
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = recipients
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "html"))

        server = self._build_server()
        server.starttls()
        server.login(self.user, self.password)
        server.sendmail(self.sender, recipients, msg.as_string())
        server.quit()

    def _build_server(self):
        return smtplib.SMTP(self.url, self.port)

    def process_message(self, message_raw):
        recipients = message_raw["receiver_emails"]
        message = message_raw["message_html"]
        subject = message_raw["title"]

        try:
            self._send_email(message, subject, recipients)
            logger.info("Sent Email notification to address {}. msg: {}".format(recipients,
                                                                                message))
        except Exception as ex:
            logger.error("Error Sending Email notification to address {}. {}".format(recipients, ex))

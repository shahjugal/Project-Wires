import os
import getpass, smtplib
from pathlib import Path
import smtplib, ssl
from fastapi import BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

HOST = "smtp-mail.outlook.com"

PORT = 587

SENDER_EMAIL: str = "project-wires@outlook.com"

SENDER_PASSWORD: str = "r7Hp*D6qC2HU(QQ"

class EmailSender:

    def __init__(self) -> None: 
        self.templates = Jinja2Templates(directory="templates")
        self.conf = ConnectionConfig(
            MAIL_USERNAME = SENDER_EMAIL,
            MAIL_PASSWORD = SENDER_PASSWORD,
            MAIL_FROM = SENDER_EMAIL,
            MAIL_PORT = PORT,
            MAIL_SERVER = HOST,
            MAIL_STARTTLS = True,
            MAIL_SSL_TLS = False,
            TEMPLATE_FOLDER = Path(__file__).parent.parent / 'templates',
        )

    def send_welcome_mail(self, recipient_email, name, bg: BackgroundTasks):

        try:
            dataVars = {
                "name":name,
                "link":"wires.onrender.com"
            }

            message = MessageSchema(
            subject="Welcome to Wires Student Network",
            recipients=[recipient_email],
            template_body=dataVars,
            subtype=MessageType.html,
            )
            fm = FastMail(self.conf)
            bg.add_task(fm.send_message,message, template_name="WelcomeMail.html")
        except Exception as e:
            # Print any error messages to stdout
            print(e)

    def send_verification_mail(self, recipient_email, name, link, bg: BackgroundTasks):

        try:
            dataVars = {
                "name":name,
                "link":link
            }

            message = MessageSchema(
            subject="Account Verification",
            recipients=[recipient_email],
            template_body=dataVars,
            subtype=MessageType.html,
            )
            fm = FastMail(self.conf)
            bg.add_task(fm.send_message,message, template_name="EmailVerificationMail.html")
        except Exception as e:
            # Print any error messages to stdout
            print(e)

    def send_reset_password_mail(self, recipient_email, name, link, bg: BackgroundTasks):

        try:
            dataVars = {
                "name":name,
                "link":link
            }

            message = MessageSchema(
            subject="Password Reset",
            recipients=[recipient_email],
            template_body=dataVars,
            subtype=MessageType.html,
            )
            fm = FastMail(self.conf)
            bg.add_task(fm.send_message,message, template_name="PasswordResetMail.html")
        except Exception as e:
            # Print any error messages to stdout
            print(e)    
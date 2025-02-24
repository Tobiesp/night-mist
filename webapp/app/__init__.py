from typing import Optional
from flask_sqlalchemy import SQLAlchemy

from app.servant.email_servant import EmailServant


SQL_DB = SQLAlchemy()
EMAIL_SERVANT: Optional[EmailServant] = None


def send_email(subject: str, body: str, to: str):
    if EMAIL_SERVANT is not None:
        EMAIL_SERVANT.send_email(subject, body, to)
    else:
        # Do nothing if the email servant is not set up
        pass
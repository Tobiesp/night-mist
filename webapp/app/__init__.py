from typing import Optional

from flask_limiter import Limiter

from app.servant.email_servant import EmailServant


EMAIL_SERVANT: Optional[EmailServant] = None
LIMITER: Optional[Limiter] = None


def set_limter(limiter: Limiter):
    global LIMITER
    LIMITER = limiter


def set_email_servant(email_servant: EmailServant):
    global EMAIL_SERVANT
    EMAIL_SERVANT = email_servant


def send_email(subject: str, body: str, to: str):
    if EMAIL_SERVANT is not None:
        EMAIL_SERVANT.send_email(subject, body, to)
    else:
        # Do nothing if the email servant is not set up
        pass
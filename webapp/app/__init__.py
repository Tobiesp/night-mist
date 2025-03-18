import base64
from typing import Optional

from flask_limiter import Limiter

from app.servant.email_servant import EmailServant


EMAIL_SERVANT: Optional[EmailServant] = None
LIMITER: Optional[Limiter] = None
ADMIN_KEY: Optional[str] = None


def set_admin_secret(key: str):
    global ADMIN_KEY
    bytes = key.encode()
    if len(bytes) > 32:
        bytes = bytes[:32]
    ADMIN_KEY = base64.urlsafe_b64encode(bytes).decode()


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
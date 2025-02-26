from typing import Optional

from app.servant.email_servant import EmailServant


EMAIL_SERVANT: Optional[EmailServant] = None


def send_email(subject: str, body: str, to: str):
    if EMAIL_SERVANT is not None:
        EMAIL_SERVANT.send_email(subject, body, to)
    else:
        # Do nothing if the email servant is not set up
        pass
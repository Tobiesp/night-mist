class EmailServant:
    def __init__(self):
        self.email_service = None

    def send_email(self, subject: str, body: str, to: str):
        raise NotImplementedError
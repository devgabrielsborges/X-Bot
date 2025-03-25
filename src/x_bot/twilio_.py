from twilio.rest import Client


class TwilioAPI:
    """ class for operations with Twilio SMS API"""
    def __init__(self, account_sid: str, auth_token: str):
        """__init__ Set the account sid and authenticantion token

        Args:
            account_sid (str): account sid
            auth_token (str): authentication token
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client: Client | None = None
        self.sid: str = ''

    def send_sms(self, from_number: str, to_number: str, msg: str):
        """send_sms _summary_

        Args:
            from_number (str): Number from Twilio
            to_number (str): Number you want to send the message.
            msg (str): Message
        """
        self.client = Client(self.account_sid, self.auth_token)
        message = self.client.messages.create(
            to=to_number,
            from_=from_number,
            body=msg
        )
        self.sid: str = message.sid

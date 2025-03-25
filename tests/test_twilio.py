from os import getenv
from dotenv import load_dotenv
from unittest.mock import patch
from src.x_bot.twilio_ import TwilioAPI  # Updated import path

load_dotenv()


def test_twilio_init():
    # Arrange
    twilio_sid = getenv("TWILIO_SID")
    twilio_token = getenv("TWILIO_TOKEN")

    # Act
    twilio_api = TwilioAPI(twilio_sid, twilio_token)

    # Assert
    assert twilio_api.account_sid == twilio_sid
    assert twilio_api.auth_token == twilio_token
    assert twilio_api.client is None


def test_twilio_send_sms():
    # Arrange
    twilio_sid = getenv("TWILIO_SID")
    twilio_token = getenv("TWILIO_TOKEN")
    to = getenv("NUMBER_TO")
    from_ = getenv("NUMBER_FROM")
    body = "Hello Python!"

    # Act
    with patch("src.x_bot.twilio_.Client") as mock_client:  # Updated patch path
        instance = mock_client.return_value
        instance.messages.create.return_value.sid = twilio_sid
        twilio_api = TwilioAPI(twilio_sid, twilio_token)
        twilio_api.send_sms(from_, to, body)

    # Assert
    assert twilio_api.sid == twilio_sid
    instance.messages.create.assert_called_once_with(to=to, from_=from_, body=body)

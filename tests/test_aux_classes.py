from dotenv import load_dotenv
from unittest.mock import patch
from aux_classes import Product, TwilioAPI, GroqCloud

load_dotenv()


def test_product_init():
    product = Product("TestProduct", 10.0, 15.0, "http://example.com")
    assert product.produto == "TestProduct"
    assert product.valor == 10.0
    assert product.ultimo_valor == 15.0
    assert product.link == "http://example.com"
    assert product.info is None


def test_product_list_info():
    product = Product("TestProduct", 10.0, 15.0, "http://example.com")
    info = product.list_info()
    assert isinstance(info, list)
    assert len(info) == 4
    assert info[0] == "TestProduct"
    assert info[1] == 10.0
    assert info[2] == 15.0
    assert info[3] == "http://example.com"


def test_twilio_init():
    twilio_api = TwilioAPI("account_sid_test", "auth_token_test")
    assert twilio_api.account_sid == "account_sid_test"
    assert twilio_api.auth_token == "auth_token_test"
    assert twilio_api.client is None
    assert twilio_api.sid is None


def test_twilio_send_sms():
    with patch("aux_classes.Client") as mock_client:
        instance = mock_client.return_value
        instance.messages.create.return_value.sid = "MockSid"
        twilio_api = TwilioAPI("test_sid", "test_token")
        twilio_api.send_sms("+100", "+200", "Hello SMS")
        assert twilio_api.sid == "MockSid"
        instance.messages.create.assert_called_once_with(
            to="+200",
            from_="+100",
            body="Hello SMS"
        )


def test_groqcloud_init():
    groq = GroqCloud("TestJob", 0.2, "llama3-8b-8192")
    assert groq.job == "TestJob"
    assert groq.criativity == 0.2
    assert groq.model == "llama3-8b-8192"
    assert groq.response is None
    assert groq.chain is None


def test_groqcloud_request(mocker):
    mocker.patch.object(GroqCloud, 'request', return_value="Mocked response")
    groq = GroqCloud("TestJob")
    response = groq.request("Hello")
    assert response == "Mocked response"

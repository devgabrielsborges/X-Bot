from os import getenv
from dotenv import load_dotenv
from unittest.mock import patch
from aux_classes import Product, TwilioAPI, GroqCloud

load_dotenv()


def test_product_init():
    # Arrange
    name = "TestProduct"
    price = 10.0
    discount = 15.0
    url = "http://example.com"
    
    # Act
    product = Product(name, price, discount, url)
    
    # Assert
    assert product.produto == name
    assert product.valor == price
    assert product.ultimo_valor == discount
    assert product.link == url
    assert product.info is None


def test_product_list_info():
    # Arrange
    name = "TestProduct"
    price = 10.0
    discount = 15.0
    url = "http://example.com"
    product = Product(name, price, discount, url)
    
    # Act
    info = product.list_info()
    
    # Assert
    assert isinstance(info, list)
    assert len(info) == 4
    assert info[0] == name
    assert info[1] == price
    assert info[2] == discount
    assert info[3] == url


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
    with patch("src.aux_classes.Client") as mock_client:
        instance = mock_client.return_value
        instance.messages.create.return_value.sid = twilio_sid
        twilio_api = TwilioAPI(twilio_sid, twilio_token)
        twilio_api.send_sms(from_, to, body)
    
    # Assert
    assert twilio_api.sid == twilio_sid
    instance.messages.create.assert_called_once_with(
        to=to,
        from_=from_,
        body=body
    )


def test_groqcloud_init():
    # Arrange
    groq = GroqCloud("TestJob", 0.2, "llama3-8b-8192")

    # Assert
    assert groq.job == "TestJob"
    assert groq.criativity == 0.2
    assert groq.model == "llama3-8b-8192"
    assert groq.response is None
    assert groq.chain is None


def test_groqcloud_request(mocker):
    # Arrange
    mocker.patch.object(GroqCloud, 'request', return_value="Mocked response")
    groq = GroqCloud("TestJob")

    # Act
    response = groq.request("Hello")

    # Assert
    assert response == "Mocked response"

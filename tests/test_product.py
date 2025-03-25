from os import getenv
from dotenv import load_dotenv
from src.x_bot.product import Product  # Updated import path

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

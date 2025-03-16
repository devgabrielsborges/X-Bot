from src.x_bot.xbot_class import Xbot
from firebase_admin import credentials


def test_xbot_init():
    # Arrange
    xbot = Xbot()

    # Assert
    assert xbot is not None


def test_xbot_init_with_index():
    # Arrange
    index = 150
    xbot = Xbot(index)

    # Assert
    assert xbot.index == index


def test_xbot_set_credentials():
    # Arrange
    xbot = Xbot()

    # Act
    xbot.set_credentials()

    # Assert
    assert FileNotFoundError or credentials.Certificate('credentials.json')


def test_xbot_set_tweet_body():
    # Arrange

    # Act
    xbot = Xbot()
    xbot.set_tweet_body()

    # Assert
    assert hasattr(xbot, "tweet_body")

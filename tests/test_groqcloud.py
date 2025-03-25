import pytest
from os import getenv
from dotenv import load_dotenv
from src.x_bot.groqcloud import GroqCloud  # Updated import path

load_dotenv()


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
    mocker.patch.object(GroqCloud, "request", return_value="Mocked response")
    groq = GroqCloud("TestJob")

    # Act
    response = groq.request("Hello")

    # Assert
    assert response == "Mocked response"

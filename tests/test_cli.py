import sys
import pytest
from unittest.mock import patch, MagicMock
from src.cli import main


def test_cli_no_args():
    """
    Test that main() returns immediately when no CLI args are provided.
    """
    # Arrange
    test_args = ["program"]

    # Act
    with patch.object(sys, "argv", test_args):
        with patch("src.cli.Xbot") as mock_xbot:
            result = main()

    # Assert
    assert result is None
    mock_xbot.assert_not_called()


def test_cli_with_valid_index():
    """
    Test that main() runs Xbot logic when a valid index is provided.
    """
    # Arrange
    test_args = ["program", "3"]

    # Create a mock Xbot instance
    mock_xbot_instance = MagicMock()
    mock_xbot_instance.item.list_info.return_value = ['product', 'value', 'last_value', 'link']
    mock_xbot_instance.set_tweet_body.return_value = "Tweet body"

    # Act
    with patch.object(sys, "argv", test_args):
        with patch("src.cli.Xbot", return_value=mock_xbot_instance) as mock_xbot:
            main()

    # Assert
    mock_xbot.assert_called_once_with(3)
    mock_xbot_instance.item.list_info.assert_called_once()
    mock_xbot_instance.set_tweet_body.assert_called_once()


def test_cli_with_non_integer_index():
    """
    Test that main() raises ValueError when a non-integer index is used.
    """
    # Arrange
    test_args = ["program", "abc"]

    # Act & Assert
    with patch.object(sys, "argv", test_args):
        with pytest.raises(ValueError):
            main()


def test_cli_with_negative_index():
    """
    Test that main() handles negative indices appropriately.
    """
    # Arrange
    test_args = ["program", "-1"]

    # Create a mock Xbot instance
    mock_xbot_instance = MagicMock()
    mock_xbot_instance.item.list_info.return_value = ['product', 'value', 'last_value', 'link']
    mock_xbot_instance.set_tweet_body.return_value = "Tweet body"

    # Act
    with patch.object(sys, "argv", test_args):
        with patch("src.cli.Xbot", return_value=mock_xbot_instance) as mock_xbot:
            main()

    # Assert
    mock_xbot.assert_called_once_with(-1)
    mock_xbot_instance.item.list_info.assert_called_once()
    mock_xbot_instance.set_tweet_body.assert_called_once()


def test_cli_xbot_raises_exception():
    """
    Test that main() propagates exceptions raised by Xbot.
    """
    # Arrange
    test_args = ["program", "2"]

    # Create a mock Xbot that raises an exception
    with patch.object(sys, "argv", test_args):
        with patch("src.cli.Xbot", side_effect=Exception("Test Exception")):
            # Act & Assert
            with pytest.raises(Exception) as exc_info:
                main()
            assert str(exc_info.value) == "Test Exception"


def test_cli_main_guard():
    """
    Test that main() is not executed when cli.py is imported.
    """
    with patch("src.cli.main") as mock_main:
        mock_main.assert_not_called()

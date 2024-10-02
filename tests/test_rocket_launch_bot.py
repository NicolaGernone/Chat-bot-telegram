import pytest
from unittest.mock import patch, MagicMock
from bot.rocket_launch_bot import get_frame_image, start, button
from bot.config import logger as lg

# Tests for get_frame_image
@patch("bot.rocket_launch_bot.requests.get")
def test_get_frame_image_success(mock_get):
    """Test successful image retrieval from the API."""
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.content = b"test_image_data"

    result = get_frame_image(1)
    assert result == b"test_image_data"
    mock_get.assert_called_once_with("http://framex-api.example.com/1")

@patch("bot.rocket_launch_bot.requests.get")
@patch.object(lg, "error")
def test_get_frame_image_failure(mock_error, mock_get):
    """Test failure to retrieve image from the API."""
    mock_get.side_effect = Exception("Connection failed")

    result = get_frame_image(1)
    assert result is None
    mock_error.assert_called_with("Error fetching frame image 1: Connection failed")

# Tests for start command
@patch("bot.rocket_launch_bot.get_frame_image")
def test_start_send_photo(mock_get_frame_image):
    """Test sending photo on /start command."""
    mock_get_frame_image.return_value = b"test_image_data"
    
    mock_update = MagicMock()
    pytest.raises(asyncio.run, start(mock_update, MagicMock()))

    mock_update.message.reply_photo.assert_called_once_with(
        b"test_image_data", caption="Frame 0"
    )

# Tests for button handling
@patch("bot.rocket_launch_bot._update_bounds")
@patch("bot.rocket_launch_bot._get_next_frame")
@patch("bot.rocket_launch_bot._send_frame_image")
def test_button_yes_response(mock_send_frame_image, mock_get_next_frame, mock_update_bounds):
    """Test handling of 'yes' response in button callback."""
    mock_query = MagicMock()
    mock_query.data = "yes"

    button(mock_query, MagicMock())

    mock_update_bounds.assert_called_once_with("yes")
    mock_get_next_frame.assert_called_once()
    mock_send_frame_image.assert_called_once()

@patch("bot.rocket_launch_bot._update_bounds")
@patch("bot.rocket_launch_bot._get_next_frame")
@patch("bot.rocket_launch_bot._send_frame_image")
def test_button_no_response(mock_send_frame_image, mock_get_next_frame, mock_update_bounds):
    """Test handling of 'no' response in button callback."""
    mock_query = MagicMock()
    mock_query.data = "no"

    button(mock_query, MagicMock())

    mock_update_bounds.assert_called_once_with("no")
    mock_get_next_frame.assert_called_once()
    mock_send_frame_image.assert_called_once()

@patch("bot.rocket_launch_bot._send_frame_image")
def test_button_final_frame(mock_send_frame_image):
    """Test button handling when the final frame is determined."""
    mock_query = MagicMock()
    mock_query.data = "yes"

    # Simulate the bisector limits to force the final frame
    global lower_bound, upper_bound, current_frame
    lower_bound = 61500
    upper_bound = 61696
    current_frame = (lower_bound + upper_bound) // 2

    button(mock_query, MagicMock())

    mock_query.edit_message_text.assert_called_once_with(
        f"The rocket has launched in frame {current_frame}"
    )

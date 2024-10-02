import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from bot.rocket_launch_bot import get_frame_image, start, button
from config import FRAMEX_API_URL, logger as lg
from bot.frame_bisect import FrameBisection

@pytest.mark.asyncio
async def test_get_frame_image_success():
    with patch("bot.rocket_launch_bot.requests.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.content = b"test_image_data"
        
        result = await get_frame_image(1)
        assert result == b"test_image_data"
        mock_get.assert_called_once_with(f"{FRAMEX_API_URL}/1")

@pytest.mark.asyncio
async def test_get_frame_image_failure():
    with patch("bot.rocket_launch_bot.requests.get") as mock_get, \
         patch.object(lg, "error") as mock_error:
        mock_get.side_effect = Exception("Connection failed")
        result = await get_frame_image(1)
        assert result is None
        mock_error.assert_called_with("Error fetching frame image 1: Connection failed")

@pytest.mark.asyncio
async def test_start_send_photo():
    with patch("bot.rocket_launch_bot.get_frame_image", new_callable=AsyncMock) as mock_get_frame_image:
        mock_get_frame_image.return_value = b"test_image_data"
        mock_update = MagicMock()
        await start(mock_update, MagicMock())
        mock_update.message.reply_photo.assert_called_once_with(b"test_image_data", caption="Frame 0")

@pytest.mark.asyncio
async def test_button_yes_response():
    with patch("bot.rocket_launch_bot.frame_bisection.update_bounds", new_callable=AsyncMock) as mock_update_bounds, \
         patch("bot.rocket_launch_bot._send_frame_image", new_callable=AsyncMock) as mock_send_frame_image:
        mock_query = MagicMock()
        mock_query.data = "yes"
        await button(mock_query, MagicMock())
        mock_update_bounds.assert_called_once_with("yes")
        mock_send_frame_image.assert_called_once()

@pytest.mark.asyncio
async def test_button_no_response():
    with patch("bot.rocket_launch_bot.frame_bisection.update_bounds", new_callable=AsyncMock) as mock_update_bounds, \
         patch("bot.rocket_launch_bot._send_frame_image", new_callable=AsyncMock) as mock_send_frame_image:
        mock_query = MagicMock()
        mock_query.data = "no"
        await button(mock_query, MagicMock())
        mock_update_bounds.assert_called_once_with("no")
        mock_send_frame_image.assert_called_once()

@pytest.mark.asyncio
async def test_start_reset_called():
    with patch("bot.rocket_launch_bot.frame_bisection.reset", new_callable=AsyncMock) as mock_reset, \
            patch("bot.rocket_launch_bot._send_frame_image", new_callable=AsyncMock) as mock_send_frame_image:
        mock_update = MagicMock()
        await start(mock_update, MagicMock())
        mock_reset.assert_called_once()
        mock_send_frame_image.assert_called_once_with(mock_update, 0)

@pytest.mark.asyncio
async def test_button_reset_after_final_frame():
    with patch("bot.rocket_launch_bot.frame_bisection.reset", new_callable=AsyncMock) as mock_reset, \
            patch("bot.rocket_launch_bot._send_frame_image", new_callable=AsyncMock) as mock_send_frame_image:
        mock_query = MagicMock()
        mock_query.data = "yes"
        frame_bisection = FrameBisection()
        frame_bisection.lower_bound = 61500
        frame_bisection.upper_bound = 61501
        frame_bisection.current_frame = 61500
        with patch("bot.rocket_launch_bot.frame_bisection", frame_bisection):
            await button(mock_query, MagicMock())
            mock_query.edit_message_text.assert_called_once_with("The rocket has launched in frame 61500")
            mock_reset.assert_called_once()
            mock_query.message.reply_text.assert_called_once_with("The search has been reset. You can /start a new one.")
            mock_send_frame_image.assert_not_called()

@pytest.mark.asyncio
async def test_button_error_handling():
    with patch("bot.rocket_launch_bot.frame_bisection.update_bounds", side_effect=Exception("Test error")), \
            patch.object(lg, "error") as mock_error:
        mock_query = MagicMock()
        await button(mock_query, MagicMock())
        mock_error.assert_called_once_with("Error handling button press: Test error")
        mock_query.message.reply_text.assert_called_once_with("Something went wrong. Please try again later.")

@pytest.mark.asyncio
async def test_button_final_frame():
    with patch("bot.rocket_launch_bot._send_frame_image", new_callable=AsyncMock) as mock_send_frame_image:
        mock_query = MagicMock()
        mock_query.data = "yes"
        frame_bisection = FrameBisection()
        frame_bisection.lower_bound = 61500
        frame_bisection.upper_bound = 61696
        frame_bisection.current_frame = (frame_bisection.lower_bound + frame_bisection.upper_bound) // 2
        with patch("bot.rocket_launch_bot.frame_bisection", frame_bisection):
            await button(mock_query, MagicMock())
            mock_send_frame_image.assert_called_once()

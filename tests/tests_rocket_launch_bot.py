import unittest
from unittest.mock import patch, MagicMock
from bot.rocket_launch_bot import get_frame_image, start, button


class TestRocketLaunchBot(unittest.TestCase):

    @patch('rocket_launch_bot.requests.get')
    def test_get_frame_image_success(self, mock_get):
        """Test successful image retrieval from the API."""
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.content = b'test_image_data'
        
        result = get_frame_image(1)
        self.assertEqual(result, b'test_image_data')
        mock_get.assert_called_once_with('http://framex-api.example.com/1')

    @patch('rocket_launch_bot.requests.get')
    @patch.object(lg, 'error')  # Mock the logger's error method
    def test_get_frame_image_failure(self, mock_error, mock_get):
        """Test failure to retrieve image from the API."""
        mock_get.side_effect = Exception("Connection failed")
        
        result = get_frame_image(1)
        self.assertIsNone(result)
        mock_error.assert_called_with("Error fetching frame image 1: Connection failed")

    @patch('rocket_launch_bot.get_frame_image')
    def test_start_send_photo(self, mock_get_frame_image):
        """Test sending photo on /start command."""
        mock_get_frame_image.return_value = b'test_image_data'
        
        mock_update = MagicMock()
        start(mock_update, MagicMock())
        
        mock_update.message.reply_photo.assert_called_once_with(
            b'test_image_data', caption='Frame 0'
        )

    @patch('rocket_launch_bot._update_bounds')
    @patch('rocket_launch_bot._get_next_frame')
    @patch('rocket_launch_bot._send_frame_image')
    def test_button_yes_response(self, mock_send_frame_image, mock_get_next_frame, mock_update_bounds):
        """Test handling of 'yes' response in button callback."""
        mock_query = MagicMock()
        mock_query.data = "yes"
        
        button(mock_query, MagicMock())
        
        mock_update_bounds.assert_called_once_with("yes")
        mock_get_next_frame.assert_called_once()
        mock_send_frame_image.assert_called_once()

    @patch('rocket_launch_bot._update_bounds')
    @patch('rocket_launch_bot._get_next_frame')
    @patch('rocket_launch_bot._send_frame_image')
    def test_button_no_response(self, mock_send_frame_image, mock_get_next_frame, mock_update_bounds):
        """Test handling of 'no' response in button callback."""
        mock_query = MagicMock()
        mock_query.data = "no"
        
        button(mock_query, MagicMock())
        
        mock_update_bounds.assert_called_once_with("no")
        mock_get_next_frame.assert_called_once()
        mock_send_frame_image.assert_called_once()

    @patch('rocket_launch_bot._send_frame_image')
    def test_button_final_frame(self, mock_send_frame_image):
        """Test button handling when the final frame is determined."""
        mock_query = MagicMock()
        mock_query.data = "yes"

        # Simulamos los límites del bisector para forzar el final
        global lower_bound, upper_bound, current_frame
        lower_bound = 61500
        upper_bound = 61696
        current_frame = (lower_bound + upper_bound) // 2

        button(mock_query, MagicMock())
        
        mock_query.edit_message_text.assert_called_once_with(
            f"The rocket has launched in frame {current_frame}"
        )

if __name__ == '__main__':
    unittest.main()

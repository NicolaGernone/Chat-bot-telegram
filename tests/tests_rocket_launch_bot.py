import unittest
from unittest.mock import patch, MagicMock
from rocket_launch_bot import get_frame_image, start, button
from config import logger as lg

class TestRocketLaunchBot(unittest.TestCase):

    @patch('rocket_launch_bot.requests.get')
    def test_get_frame_image_success(self, mock_get):
        # Configura el valor de retorno simulado para la respuesta
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.content = b'test_image_data'
        
        result = get_frame_image(1)
        self.assertEqual(result, b'test_image_data')
        mock_get.assert_called_once_with('http://framex-api.example.com/1')

    @patch('rocket_launch_bot.requests.get')
    def test_get_frame_image_failure(self, mock_get):
        # Simula una excepción de conexión
        mock_get.side_effect = Exception("Connection failed")
        
        result = get_frame_image(1)
        self.assertIsNone(result)
        lg.error.assert_called_with("Error fetching frame image 1: Connection failed")

    @patch('rocket_launch_bot.get_frame_image')
    def test_start_send_photo(self, mock_get_frame_image):
        # Configura el retorno simulado para la imagen
        mock_get_frame_image.return_value = b'test_image_data'
        
        mock_update = MagicMock()
        start(mock_update, MagicMock())
        
        mock_update.message.reply_photo.assert_called_once_with(
            b'test_image_data', caption='Frame 0: Has the rocket been launched?'
        )
    
    @patch('rocket_launch_bot._update_bounds')
    @patch('rocket_launch_bot._get_next_frame')
    @patch('rocket_launch_bot._send_frame_image')
    def test_button_yes_response(self, mock_send_frame_image, mock_get_next_frame, mock_update_bounds):
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
        mock_query = MagicMock()
        mock_query.data = "no"
        
        button(mock_query, MagicMock())
        
        mock_update_bounds.assert_called_once_with("no")
        mock_get_next_frame.assert_called_once()
        mock_send_frame_image.assert_called_once()

if __name__ == '__main__':
    unittest.main()

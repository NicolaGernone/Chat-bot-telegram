import requests
from config import FRAMEX_API_URL, TELEGRAM_BOT_TOKEN
from config import logger as lg
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Updater)

lower_bound = 0
upper_bound = 61696
current_frame = (lower_bound + upper_bound) // 2


def get_frame_image(frame_number: int) -> bytes:
    """
    Fetches the image content of a specific frame from an external API.
    Args:
        frame_number (int): The number of the frame to retrieve.
    Returns:
        bytes: The content of the frame image in bytes, or None if an error occurs.
    """
    try:
        url = f"{FRAMEX_API_URL}/{frame_number}"
        lg.info(f"Fetching image from: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        lg.info(f"Successfully fetched frame {frame_number}")
        return response.content
    except requests.exceptions.RequestException as e:
        lg.error(f"Error fetching frame image {frame_number}: {e}")
        return None


def start(update: Update, context: CallbackContext) -> None:
    """
    Handles the /start command. Sends the first frame of the bisection process as a photo
    and asks the user if the rocket has been launched. Provides buttons for the user to
    respond with "Yes" or "No".
    """
    global current_frame
    image = get_frame_image(current_frame)

    if image:
        update.message.reply_photo(
            image, caption=f"Frame {current_frame}"
        )
        update.message.reply_text(
            "Has the rocket been launched?", reply_markup=_create_keyboard()
        )
    else:
        lg.error("Failed to send the image; it was not retrieved.")
        update.message.reply_text("Can't get the image. Please try again later.")


def _create_keyboard() -> InlineKeyboardMarkup:
    """
    Creates the inline keyboard markup for user responses.
    Returns:
        InlineKeyboardMarkup: The keyboard markup with "Yes" and "No" buttons.
    """
    keyboard = [
        [
            InlineKeyboardButton("Sí", callback_data="yes"),
            InlineKeyboardButton("No", callback_data="no"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def _update_bounds(response: str) -> None:
    """
    Updates the bisection bounds based on the user's response.
    Args:
        response (str): The user's response ("yes" or "no").
    """
    global lower_bound, upper_bound, current_frame
    if response == "yes":
        upper_bound = current_frame
    else:
        lower_bound = current_frame


def _get_next_frame() -> None:
    """
    Calculates the next frame to display based on current bounds.
    """
    global lower_bound, upper_bound, current_frame
    current_frame = (lower_bound + upper_bound) // 2


def _send_frame_image(query, frame_number: int) -> None:
    """
    Sends the image of the current frame and asks the user if the rocket has been launched.
    Args:
        query: The callback query to respond to.
        frame_number (int): The current frame number to fetch and display.
    """
    image = get_frame_image(frame_number)
    if image:
        query.message.reply_photo(
            image, caption=f"Frame {frame_number}"
        )
        query.message.reply_text(
            "Has the rocket been launched?", reply_markup=_create_keyboard()
        )
    else:
        lg.error("Failed to send the image; it was not retrieved.")
        query.message.reply_text("Can't get the image. Please try again later.")


def button(update: Update, context: CallbackContext) -> None:
    """
    Handles the callback query when a button is pressed in the Telegram bot interface.
    This function adjusts the bisection bounds based on the user's response and calculates
    a new intermediate frame to determine the exact frame when the rocket was launched.
    """
    global lower_bound, upper_bound, current_frame
    query = update.callback_query
    query.answer()

    try:
        _update_bounds(query.data)
        _get_next_frame()

        if lower_bound >= upper_bound - 1:
            query.edit_message_text(
                f"The rocket has launched in the frame {current_frame}"
            )
        else:
            _send_frame_image(query, current_frame)
    except Exception as e:
        lg.error(f"Error handling button press: {e}")
        query.message.reply_text("Something went wrong. Please try again later.")


def main():
    try:
        updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CallbackQueryHandler(button))

        lg.info("Bot started. Waiting for commands...")
        updater.start_polling()
        updater.idle()
    except Exception as e:
        lg.critical(f"An error occurred while starting the bot: {e}")


if __name__ == "__main__":
    main()

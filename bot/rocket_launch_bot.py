import requests
from config import FRAMEX_API_URL, TELEGRAM_BOT_TOKEN, logger as lg
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Application,
)
from bot.frame_bisect import FrameBisection


frame_bisection = FrameBisection()


async def get_frame_image(frame_number: int) -> bytes:
    """
    Fetches the image content of a specific frame from an external API.
    """
    try:
        url = f"{FRAMEX_API_URL}/{frame_number}"
        lg.info(f"Fetching image from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        lg.info(f"Successfully fetched frame {frame_number}")
        return response.content
    except requests.exceptions.RequestException as e:
        lg.error(f"Error fetching frame image {frame_number}: {e}")
        return None


async def start(update: Update, context: CallbackContext) -> None:
    """
    Handles the /start command.
    """
    lg.info("Received /start command")
    frame_bisection.reset()
    await _send_frame_image(update, frame_bisection.current_frame)


def _create_keyboard() -> InlineKeyboardMarkup:
    """
    Creates the inline keyboard markup for user responses.
    """
    keyboard = [
        [
            InlineKeyboardButton("Sí", callback_data="yes"),
            InlineKeyboardButton("No", callback_data="no"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def _send_frame_image(update: Update, frame_number: int) -> None:
    """
    Sends the image of the current frame and asks the user if the rocket has been launched.
    """
    image = await get_frame_image(frame_number)
    if image:
        await update.message.reply_photo(image, caption=f"Frame {frame_number}")
        await update.message.reply_text(
            "Has the rocket been launched?", reply_markup=_create_keyboard()
        )
        lg.info(f"Sent frame {frame_number} to the user")
    else:
        lg.error("Failed to send the image; it was not retrieved.")
        await update.message.reply_text("Can't get the image. Please try again later.")


async def button(update: Update, context: CallbackContext) -> None:
    """
    Handles the callback query when a button is pressed in the Telegram bot interface.
    """
    query = update.callback_query
    await query.answer()

    try:
        lg.info(f"Button pressed: {query.data}")
        frame_bisection.update_bounds(query.data)

        if frame_bisection.lower_bound >= frame_bisection.upper_bound - 1:
            await query.edit_message_text(
                f"The rocket has launched in frame {frame_bisection.current_frame}"
            )
            lg.info(f"Final frame determined: {frame_bisection.current_frame}")

            frame_bisection.reset()
            await query.message.reply_text(
                "The search has been reset. You can /start a new one."
            )
        else:
            await _send_frame_image(query, frame_bisection.current_frame)
    except Exception as e:
        lg.error(f"Error handling button press: {e}")
        await query.message.reply_text("Something went wrong. Please try again later.")


def main():
    try:
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))

        lg.info("Bot started. Waiting for commands...")
        application.run_polling()
    except Exception as e:
        lg.critical(f"An error occurred while starting the bot: {e}")


if __name__ == "__main__":
    main()

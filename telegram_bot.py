import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, Updater, CallbackQueryHandler, filters)




async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Sends a message with three inline buttons attached."""

    keyboard = [

        [

            InlineKeyboardButton("MENU", callback_data="1"),

            InlineKeyboardButton("REGISTRATION", callback_data="2"),

        ],

        [
            InlineKeyboardButton("ORDERING", callback_data="3"),

            InlineKeyboardButton("PAYMENT", callback_data="4")
            
            ],

    ]



    reply_markup = InlineKeyboardMarkup(keyboard)


    await update.message.reply_text("Please choose:", reply_markup=reply_markup)



async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Parses the CallbackQuery and updates the message text."""

    query = update.callback_query


    await query.answer()


    await query.edit_message_text(text=f"Selected option: {query.data}")



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

FIRST_NAME, LAST_NAME, LOCATION, PHONE_NUMBER = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Hello welcome to our bot {update.effective_user.first_name}! \n"
        "First you should register"
        
        )

    return FIRST_NAME

async def first_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    await update.message.reply_text(
        f'Enter your first name'
        
        )
    return LAST_NAME


async def last_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )

    return LOCATION

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:



    app = ApplicationBuilder().token("6395036658:AAE_0MOQ46rAEVLRS6Hn4YunLgNw5IqCYU4").build()



    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler('menu', menu))
    app.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":

    main()
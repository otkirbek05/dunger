from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Updater, CallbackQueryHandler
import logging

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello welcome to our bot {update.effective_user.first_name} first you should register'
        
        )


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




















def main() -> None:



    app = ApplicationBuilder().token("6395036658:AAE_0MOQ46rAEVLRS6Hn4YunLgNw5IqCYU4").build()



    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler('menu', menu))
    app.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":

    main()
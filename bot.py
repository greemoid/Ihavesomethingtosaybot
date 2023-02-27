import logging
import time

from telegram import __version__ as TG_VER
from config import TOKEN, CHAT_ID
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CallbackContext

video_path = 'video.mp4'

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    chat_id = update.effective_chat.id
    # Create a button
    button = InlineKeyboardButton(text='Так, погоджуюся', callback_data='button_clicked')

    # Create a keyboard with the button
    keyboard = InlineKeyboardMarkup([[button]])
    await context.bot.sendMessage(chat_id=chat_id, text="""
Привіт!
    
Цей бот створений для того, щоб ви могли анонімно написати те, що не можете сказати з якоїсь причини вживу.

Ви можете признатися в коханні, вибачитися, розповісти таємницю та будь-що, що вам заманеться. Через кілька днів я оформлю пост, або серію постів з вашими признаннями. 

Повідомлення пройдуть модерацію. Ті, що будуть на мою думку жартівливі, викладені не будуть.

В наступному повідомленні ви побачите відеопідтвердження того, що я не бачу ваших телеграм-акаунтів.
    
    """)

    time.sleep(4)
    with open(video_path, 'rb') as video_file:
        await context.bot.send_video(chat_id=update.effective_chat.id, video=video_file)
        time.sleep(3)
        await context.bot.sendMessage(chat_id=update.effective_chat.id, text="""
Ви погоджуєтеся на те, що ваше повідомлення буде оформлене в пост та викладене на канал або в інстаграм?""",
                                      reply_markup=keyboard)


async def messageHandler(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'button_clicked':
        await context.bot.sendMessage(chat_id=update.effective_chat.id, text="""
Напишіть ваше признання, яке з якоїсь причини не можете сказати вживу.
        """)



async def redirect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    message = update.message.text
    await context.bot.sendMessage(chat_id=CHAT_ID, text=message)
    await context.bot.sendMessage(chat_id=update.effective_chat.id, text="""Дякую! Чекайте пост. Якщо вам є, що написати ще, ви можете просто написати це в бот будь-коли.""")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, redirect))
    application.add_handler(CallbackQueryHandler(messageHandler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

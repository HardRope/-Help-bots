import logging


from environs import Env
from telegram.ext import (
    Filters,
    Updater,
    # CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    # PreCheckoutQueryHandler,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Здравствуйте!'
    )


def echo(update, context):
    message = update.message.text

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=message
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()

    tg_token = env.str('TELEGRAM_TOKEN')

    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()
    updater.idle()

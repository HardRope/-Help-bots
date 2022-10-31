import logging
from functools import partial

from environs import Env
import telegram
from telegram.ext import (
    Filters,
    Updater,
    CommandHandler,
    MessageHandler,
)

from _general_bots_functions import detect_intent_texts, TelegramLogsHandler

logger = logging.getLogger('tg_bot')


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Здравствуйте!'
    )


def answer(update, context):
    message = request_answer(
        session_id=update.message.chat_id,
        text=update.message.text
    )[1]

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=message
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()

    project_id = env.str('DIALOGFLOW_ID')
    request_answer = partial(detect_intent_texts, project_id=project_id)

    tg_token = env.str('TELEGRAM_TOKEN')
    tg_chat_id = env('TELEGRAM_CHAT_ID')
    tg_bot = telegram.Bot(token=tg_token)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s -  %(message)s - %(exc_info)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logger.addHandler(TelegramLogsHandler(tg_bot=tg_bot, tg_chat_id=tg_chat_id))

    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), answer))

    logger.warning('Бот запущен')
    updater.start_polling()
    updater.idle()

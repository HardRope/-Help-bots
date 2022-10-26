import logging

from environs import Env
from google.cloud import dialogflow
import telegram
from telegram.ext import (
    Filters,
    Updater,
    CommandHandler,
    MessageHandler,
)

env = Env()
env.read_env()

logger = logging.getLogger('tg_bot')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, tg_chat_id):
        super().__init__()

        logging_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -  %(message)s - %(exc_info)s')
        self.setFormatter(fmt=logging_format)

        self.tg_bot = tg_bot
        self.tg_chat_id = tg_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.tg_chat_id, text=log_entry)


def detect_intent_texts(session_id, text, project_id=env.str('DIALOGFLOW_ID'), language_code='ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Здравствуйте!'
    )


def answer(update, context):
    message = detect_intent_texts(
        session_id=update.message.chat_id,
        text=update.message.text
    )

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=message
    )


if __name__ == '__main__':
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

    updater.start_polling()
    updater.idle()

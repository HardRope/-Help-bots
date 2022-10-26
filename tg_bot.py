import logging

from environs import Env
from google.cloud import dialogflow
from telegram.ext import (
    Filters,
    Updater,
    CommandHandler,
    MessageHandler,
)

env = Env()
env.read_env()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


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

    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), answer))

    updater.start_polling()
    updater.idle()

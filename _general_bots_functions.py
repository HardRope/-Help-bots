import logging
from google.cloud import dialogflow


def detect_intent_texts(session_id, text, project_id, language_code='ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
    )
    result = response.query_result.intent.is_fallback
    answer_text = response.query_result.fulfillment_text
    return result, answer_text


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

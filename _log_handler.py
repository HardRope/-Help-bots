import logging


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
import random
import logging
import sys
from functools import partial

from google.api_core.exceptions import InvalidArgument
from environs import Env
import telegram
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from _general_bots_functions import detect_intent_texts, TelegramLogsHandler

logger = logging.getLogger('vk_bot')


def answer(event, vk_api):
    text = event.text
    user_id = event.user_id

    check, answer_text = request_answer(
        session_id=user_id,
        text=text
    )

    if not check:
        vk_api.messages.send(
            user_id=user_id,
            message=answer_text,
            random_id=random.randint(1,1000)
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
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.WARNING
    )
    logger.addHandler(TelegramLogsHandler(tg_bot=tg_bot, tg_chat_id=tg_chat_id))

    vk_token = env.str('VK_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)
    logger.warning('Бот запущен')
    while True:
        try:

            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    answer(event, vk_api)
        except InvalidArgument:
            logger.info('Пользователь отправил не текст')
            continue
        except Exception:
            logger.warning('Непредвиденная ошибка!', exc_info=sys.exc_info())
            continue
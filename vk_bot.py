import random
import logging

from google.cloud import dialogflow
from environs import Env
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

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
    result = response.query_result.intent.is_fallback
    answer_text = response.query_result.fulfillment_text
    return result, answer_text


def answer(event, vk_api):
    text = event.text
    user_id = event.user_id

    check, answer_text = detect_intent_texts(
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
    vk_token = env.str('VK_TOKEN')

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api)

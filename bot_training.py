import argparse
import logging

import requests
from environs import Env
from google.cloud import dialogflow

env = Env()
env.read_env()

logger = logging.getLogger('bot_training')


def create_parser():
    parser = argparse.ArgumentParser(description='Add data from url with json to DialogFlow')
    parser.add_argument('url', help='URL with JSON, contains data for create Intents')
    return parser


def create_intent(project_id, display_name, training_phrases_parts, message_text):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)

        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_text)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={'parent': parent, 'intent': intent, 'language_code': 'ru'}
    )

    logger.info('Intent created: {}'.format(response))


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    parser = create_parser()
    namespace = parser.parse_args()

    project_id = env.str('DIALOGFLOW_ID')

    try:
        response = requests.get(namespace.url)
        response.raise_for_status()

        serialized_phrases = response.json()

        for name, phrases in serialized_phrases.items():
            training_phrases_parts = phrases['questions']
            answers = [phrases['answer']]
            create_intent(project_id, name, training_phrases_parts, answers)
    except requests.HTTPError:
        logger.info('Ошибка загрузки. Проверьте ссылку')
    except requests.exceptions.MissingSchema:
        logger.info('Неверный адрес. Требуется ссылка (http://url...')
    except Exception:
        logger.warning('Непредвиденная ошибка!', exc_info=sys.exc_info())

import logging

import requests
from environs import Env
from google.cloud import dialogflow


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

    logging.info('Intent created: {}'.format(response))


if __name__ == '__main__':
    env = Env()
    env.read_env()

    project_id = env.str('DIALOGFLOW_ID')

    url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'

    try:

        response = requests.get(url)
        response.raise_for_status()

        serialized_phrases = response.json()

        for name, phrases in serialized_phrases.items():
            training_phrases_parts = phrases['questions']
            answers = [phrases['answer']]
            create_intent(project_id, name, training_phrases_parts, answers)
    except requests.HTTPError:
        logging.info('Ошибка загрузки. Проверьте ссылку')


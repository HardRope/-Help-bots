# Help_bots

This program created to help support managers answer to typical user questions, that's were sent to 
[Telegram](https://telegram.org/)-bot or to [VK](https://vk.com/)-group messages.

Bot using [DialogFlow](https://dialogflow.cloud.google.com/) to train the bot and choose correct answer for user's
message.

## Install

1. Download code.
2. Install required libs by console command.
  
   ```
   pip install -r requirements.txt
   ```
   
3. Create `.env`-file with tokens

    ```commandline
    TELEGRAM_TOKEN=5368180626:AAH8.....     # Token of your telegram bot
    TELEGRAM_CHAT_ID=999999999              # Your chat_id for sending logs
    VK_TOKEN=vk1.a.L3-9jkocjO...            # Token of your vk_group
    DIALOGFLOW_ID=t-hardrope-sp...          # DialogFlow project ID
    GOOGLE_APPLICATION_CREDENTIALS='application_default_credentials.json'
                                            # Path to applicaton_default_credentials file
    ```

    * Telegram-token: help with obtain TG-Token: [Bot Father](https://telegram.me/BotFather)
    * Chat_id: write [userinfobot](https://t.me/userinfobot) to get your id
    * VK-token: obtaining in settings of your VK Group, API tab
    * DialogFlow_id: setup a DF-project, [instruction](https://cloud.google.com/dialogflow/es/docs/quick/setup)
    * Credentials: creating a JSON-key, [instruction](https://cloud.google.com/docs/authentication/client-libraries)

## Usage

1. tg_bot
   
    Connect your tg-bot to your DialogFlow project, answer to text-messages, if an error occurs, send log to chat from
    `.env/TELEGRAM_CHAT_ID`

    Launch:

   ```
   python tg_bot.py
   ```

2. vk_bot

    Working as well as `tg_bot`, send error to your tg too

    Launch:

   ```
   python vk_bot.py
   ```
   
3. bot_training

    Script creating new Intents in your DialogFlow. Accept url with json, contains intent name, users questions and 
    answer for it

    Json must be looks like:

    ```commandline
   {
        "name_1": {
                "questions": [
                    list of questions(str)
                ],
                "answer": bot answer(str)
        },
        "name_2": {
                "questions": [
                    list of questions(str)
                ],
                "answer": bot answer(str)
        },
   }
   ```
   
    To launch script:

    ```commandline
   python bot_training.py url   # to create new intents
   
   or
   
   python bot_training.py -h    # to help
   ```
   
## Preview

![](tg_example.gif)
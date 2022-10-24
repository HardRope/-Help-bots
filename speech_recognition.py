from environs import Env

if __name__ == '__main__':
    env = Env()
    env.read_env()

    tg_token = env.str('TELEGRAM_TOKEN')
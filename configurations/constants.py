from dotenv import load_dotenv
import os

load_dotenv()


class BOT:
    TOKEN = os.getenv("BOT_TOKEN")
    USERNAME = os.getenv("BOT_USERNAME")


class STEP:
    MAIN = 0
    SELECTING_LANGUAGE = 1

    GETTING_POST_MESSAGE = 2

    DICT = {
        MAIN: "Main",
        SELECTING_LANGUAGE: "Selecting language",
        GETTING_POST_MESSAGE: "Getting post message",
    }

    CHOICES = DICT.items()


class ERROR:
    class TYPE:
        GENERAL = 'general'

        DICT = {
            GENERAL: "General",
        }

        CHOICES = list(DICT.items())

from dotenv import load_dotenv
import os

load_dotenv()


class BOT:
    TOKEN = os.getenv("BOT_TOKEN")
    USERNAME = os.getenv("BOT_USERNAME")


class CONSTANT:
    IS_BOT_WORKING = '0'

    DEFAULT = {
        IS_BOT_WORKING: '0',
    }

    DICT = {
        IS_BOT_WORKING: "Is bot working ?",
    }

    CHOICES = list(DICT.items())


class CALLBACK:
    SELECT_THE_TEXT = 0
    CHANGE_THE_CATEGORY_INTERESTED_STATE = 1

    SELECT_TOP_EPISODES_PAGE = 10
    SELECT_NEWEST_EPISODES_PAGE = 11
    SELECT_SUBSCRIPTIONS_PAGE = 12

    SELECT_COLLECTIONS_PAGE = 20
    SELECT_THE_COLLECTION = 21
    SELECT_THE_COLLECTION_PODCASTS_PAGE = 22

    SELECT_CHANNELS_PAGE = 30
    SELECT_THE_CHANNEL = 31
    SELECT_THE_CHANNEL_PODCASTS_PAGE = 32

    SELECT_PODCASTS_PAGE = 40
    SELECT_THE_PODCAST = 41
    CHANGE_THE_PODCAST_SUBSCRIPTION_STATE = 42
    CHANGE_THE_PODCAST_SUBSCRIPTION_NOTIFICATION_STATE = 43
    DOWNLOAD_ALL_EPISODES_OF_THE_PODCAST = 44
    SELECT_THE_PODCAST_EPISODES_PAGE = 45

    SELECT_THE_EPISODE = 50
    OPEN_THE_TIMELAPSE = 51
    CLOSE_THE_TIMELAPSE = 52
    CHANGE_THE_EPISODE_LIKE_STATE = 53
    DELETE_THE_EPISODE = 55

    SELECT_THE_SEARCH_QUERY_EPISODES_PAGE = 60

    DELETE_THE_MESSAGE = 100


class STEP:
    MAIN = 0

    GETTING_POST_MESSAGE = 2

    DICT = {
        MAIN: "Main",
        GETTING_POST_MESSAGE: "Getting post message",
    }

    CHOICES = DICT.items()


class ERROR:
    class TYPE:
        GENERAL = 'general'
        API_EXCEPTION_ON_CALLBACK_QUERY_HANDLER = 'api_exception_on_callback_query_handler'
        EXCEPTION_ON_CALLBACK_QUERY_HANDLER = 'exception_on_callback_query_handler'
        EXCEPTION_ON_INLINE_QUERY_HANDLER = 'exception_on_inline_query_handler'

        DICT = {
            GENERAL: "General",
            API_EXCEPTION_ON_CALLBACK_QUERY_HANDLER: "API Exception on callback query handler",
            EXCEPTION_ON_CALLBACK_QUERY_HANDLER: "Exception on callback query handler",
            EXCEPTION_ON_INLINE_QUERY_HANDLER: "Exception on inline query handler",
        }

        CHOICES = list(DICT.items())


DELIMITER = "&&&&&"

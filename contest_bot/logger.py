import logging, time
import bot_settings as settings


def setup(logger_path):
    """ Set up the Logger """
    if settings.LOG_TO_CONSOLE:
        return

    # Set up Logger
    curr_time = time.strftime("%Y%m%d-%H%M%S")

    logging.basicConfig(filename=logger_path + curr_time + ".txt",
                        level=logging.INFO,
                        format='%(levelname)s - [%(asctime)s] -- %(message)s')


def info(message):
    """ Log the message """
    if settings.LOG_TO_CONSOLE:
        print(message)
    else:
        logging.info(message)

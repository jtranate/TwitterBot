import logging, time


def setup(logger_path):
    # Set up Logger
    curr_time = time.strftime("%Y%m%d-%H%M%S")

    logging.basicConfig(filename=logger_path + curr_time + ".txt",
                        level=logging.INFO,
                        format='%(levelname)s - [%(asctime)s] -- %(message)s')


def info(message):
    logging.info(message)

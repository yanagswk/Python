import logging.config

logging.config.fileConfig('logging.ini')


def get_logger():
    # __name__ には、root が入る
    return logging.getLogger(__name__)

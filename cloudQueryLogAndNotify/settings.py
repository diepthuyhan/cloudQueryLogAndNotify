import logging
import os


logger = logging.getLogger()


def setLogLevel(log_level):
    logger.setLevel(log_level)

def get_logger():
    return logger

import logging
def get_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig(level = logging.INFO)
    return logger
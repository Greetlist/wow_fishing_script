import logging
import os
import datetime as dt

class FishingLogger:
    log_dir = os.path.dirname(__file__)
    log_filename = 'fishing_{}.log'.format(dt.datetime.now().strftime('%Y-%m-%d-%H%M%S'))
    logger = logging.getLogger(log_filename)

    logger.setLevel(logging.INFO)
    if not logger.handlers:
        formatter = logging.Formatter('[%(filename)s %(lineno)s]| %(message)s')
        file_handler = logging.FileHandler(os.path.join(log_dir, log_filename))
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    @staticmethod
    def info(msg):
        FishingLogger.logger.info(msg)
        FishingLogger.logger.handlers[0].flush()

    @staticmethod
    def warning(msg):
        FishingLogger.logger.warning(msg)
        FishingLogger.logger.handlers[0].flush()

    @staticmethod
    def error(msg):
        FishingLogger.logger.error(msg)
        FishingLogger.logger.handlers[0].flush()
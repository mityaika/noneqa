import logging


def get_logger(name, log_level="DEBUG"):
    """Create logger on demand."""

    logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(log_level.upper()))
    logging.getLogger("paramiko").setLevel(logging.WARNING)

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(threadName)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(handler)

    return logger

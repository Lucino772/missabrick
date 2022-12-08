import logging

def get_logger(module_name: str):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    _config_console_handler(logger)

    return logger

def _config_console_handler(logger: logging.Logger):
    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s][%(name)s] %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

import logging

class Logger:
    _logger = None

    @staticmethod
    def get_logger(name="HuntoAgent"):
        if Logger._logger is None:
            Logger._logger = logging.getLogger(name)
            Logger._logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            if not Logger._logger.handlers:
                Logger._logger.addHandler(handler)
        return Logger._logger

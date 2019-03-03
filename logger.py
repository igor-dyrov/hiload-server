import logging


class Logger:
    def __init__(self):
        self._logger = logging.getLogger('main')
        self._logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(process)s] %(message)s',
            '%H:%M:%S'
        )
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

    @property
    def logger(self):
        return self._logger

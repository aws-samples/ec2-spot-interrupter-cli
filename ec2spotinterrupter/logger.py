import logging

LOG = logging.getLogger(__name__)

class logger:
    @staticmethod
    def info(message):
        LOG.warning(message)
        print(message)
        return

    @staticmethod
    def log(message):
        LOG.warning(message)
        return
    
    @staticmethod
    def exception(error):
        LOG.exception(error)




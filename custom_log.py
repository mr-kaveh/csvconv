import logging
import os


class clog:
    """
    Customization of log including file handler to keep
    debug level logs as well as two stream handlers for error
    and critical log level handling
    """

    def __init__(self):
        """
        initializes logger by adding file handler, console handler,
         and log format
        """
        self.logger = logging.getLogger("Document Converter")
        self.logger.setLevel(logging.DEBUG)
        # file handler which logs DEBUG messages
        if os.path.exists("./convert.log"):
            pass
        else:
            os.system("touch ./convert.log")
        self.file_handler = \
            logging.FileHandler("./convert.log")
        self.file_handler.setLevel(logging.DEBUG)

        # Stream handler with a ERROR log level handling
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.ERROR)

        # Stream handler for CRITICAL log level handling
        self.criticals = logging.StreamHandler()
        self.criticals.setLevel(logging.CRITICAL)

        # creates formatter and adds it to the handlers
        self.formatter = \
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.console_handler.setFormatter(self.formatter)
        self.file_handler.setFormatter(self.formatter)

        # adds the handlers to logger
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.criticals)

    def propagate_logger(self) -> logging:
        """
        Returns the custom logger for use in others classes
        :param self: Initialized and configured instance of logging
        :return logging: the configuration will be propagated to the caller
        """
        return self.logger

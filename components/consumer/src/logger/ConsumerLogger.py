import logging

LOGGER_LEVEL = logging.INFO # Set the logging level to INFO as default
FORMATTER = "%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s" # Define the log message format


class ConsumerLogger:
    """Singleton logger class for logging messages with timestamps.
    
    - Ensures only one instance of the logger is created.
    - Logs messages with timestamps, severity level, filename, and line number.
    """

    _logger = None # Private class variable to store the logger instance

    def __new__(cls, *args, **kwargs):
        """Creates a singleton logger instance if not already created.

        - Uses `logging.getLogger()` to configure the logger.
        - Sets log level to `LOGGER_LEVEL`.
        - Attaches a `StreamHandler` to output logs to the console.

        Returns:
            logging.Logger: A singleton logger instance.
        """
        if cls._logger is None:
            cls._logger = super().__new__(cls, *args, **kwargs) # Create a new logger instance
            cls._logger = logging.getLogger() # Get the logger instance
            cls._logger.setLevel(LOGGER_LEVEL) # Set the logging level
            handler = logging.StreamHandler() # Create a StreamHandler to output logs to the console
            handler.setFormatter(logging.Formatter(FORMATTER)) # Set the log message format
            cls._logger.addHandler(handler) # Attach the handler to the logger
        return cls._logger

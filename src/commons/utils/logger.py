"""Logger for project."""

import logging
from logging import Formatter, Logger, StreamHandler

from commons.utils import singleton


@singleton
class ProcessLogger:
    """Singleton class for project logging."""

    def __init__(self, process_name: str, log_level: int = logging.INFO) -> None:
        """Initialize console logger.

        Args:
            process_name (str): Name of the process for log identification
            log_level (int): Logging level (default: logging.INFO)
        """
        self.process_name: str = process_name

        # Configure logger
        self.logger: Logger = logging.getLogger(process_name)
        self.logger.setLevel(log_level)

        # Avoid handler duplication
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Formatter for logs
        formatter: Formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler
        console_handler: StreamHandler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def info(self, message: str, *args, **kwargs) -> None:
        """Log information message with optional formatting parameters.

        Args:
            message: Message to log
            *args: Positional arguments for % formatting
            **kwargs: Keyword arguments for str.format() formatting
        """
        if args:
            self.logger.info(message % args)
        elif kwargs:
            self.logger.info(message.format(**kwargs))
        else:
            self.logger.info(message)

    def error(self, message: str, *args, **kwargs) -> None:
        """Log error message with optional formatting parameters"""
        if args:
            self.logger.error(message % args)
        elif kwargs:
            self.logger.error(message.format(**kwargs))
        else:
            self.logger.error(message)

    def warning(self, message: str, *args, **kwargs) -> None:
        """Log warning message with optional formatting parameters"""
        if args:
            self.logger.warning(message % args)
        elif kwargs:
            self.logger.warning(message.format(**kwargs))
        else:
            self.logger.warning(message)

    def debug(self, message: str, *args: tuple, **kwargs: dict) -> None:
        """Log debug message with optional formatting parameters"""
        if args:
            self.logger.debug(message % args)
        elif kwargs:
            self.logger.debug(message.format(**kwargs))
        else:
            self.logger.debug(message)

    def critical(self, message: str, *args: tuple, **kwargs: dict) -> None:
        """Log critical message with optional formatting parameters"""
        if args:
            self.logger.critical(message % args)
        elif kwargs:
            self.logger.critical(message.format(**kwargs))
        else:
            self.logger.critical(message)

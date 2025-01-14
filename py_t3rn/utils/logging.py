import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with consistent configuration.

    Args:
        name (str): Name of the logger, typically `__name__`.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.propagate = False

    if not logger.handlers:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)
        stdout_formatter = logging.Formatter("%(message)s")
        stdout_handler.setFormatter(stdout_formatter)

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR)
        stderr_formatter = logging.Formatter("%(message)s")
        stderr_handler.setFormatter(stderr_formatter)

        logger.addHandler(stdout_handler)
        logger.addHandler(stderr_handler)

        logger.setLevel(logging.INFO)

    return logger

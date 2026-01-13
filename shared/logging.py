import logging
import os


def setup_logging(log_file: str = "app.log"):
    """
    Set up logging for the application.

    Args:
        log_file (str): The path to the log file. Defaults to "app.log".
    """
    # Clear any existing handlers to avoid conflicts with pytest
    logging.root.handlers.clear()

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logging.info("Logging setup complete.")

    # Flush the log messages to ensure the file is created and written to
    for handler in logging.root.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.flush()

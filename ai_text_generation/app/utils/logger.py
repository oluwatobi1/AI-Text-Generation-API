import os
import logging

def setup_logging():
    """Configures logging ."""
    
    log_level = logging.DEBUG if os.getenv("FLASK_ENV") == "development" else logging.INFO
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    


    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(log_format))

    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)

    root_logger.info("Logging has been set up successfully.")
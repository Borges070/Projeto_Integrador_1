import logging
import os

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)


def setup_logger(name, filename):
    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(
            os.path.join(LOG_DIR, filename),
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger


etl_logger = setup_logger("etl", "etl.log")
api_logger = setup_logger("api", "api_errors.log")
validation_logger = setup_logger(
    "validation",
    "validation_errors.log"
)

skipped_logger = setup_logger(
    "skipped",
    "skipped_records.log"
)
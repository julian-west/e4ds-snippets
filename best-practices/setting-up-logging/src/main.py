"""Entry point"""
import logging
import logging.config
import os
from datetime import datetime

from data_processing.processor import process_data
from dotenv import find_dotenv, load_dotenv
from model_training.trainer import train

# find .env file in parent directory
env_file = find_dotenv()
load_dotenv()

CONFIG_DIR = "./config"
LOGS_DIR = "./logs"


def setup_logging():
    if os.environ["ENVIRONMENT"] == "production":
        config_path = f"{CONFIG_DIR}/logging.prod.ini"
    else:
        config_path = f"{CONFIG_DIR}/logging.dev.ini"

    timestamp = datetime.now().strftime("%Y%m%d-%H:%M:%S")
    log_output_filepath = f"{LOGS_DIR}/{timestamp}.log"

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": log_output_filepath},
    )


if __name__ == "__main__":

    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Program started")
    process_data()
    train()
    logger.info("Program finished")

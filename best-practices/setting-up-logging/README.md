# Setting up logging for data science projects

It is common for developers to default to using standard 'print' statements in their code to signal key milestones in the code's execution and help with debugging. This works OK for small projects, but can quickly become difficult to manage as projects get larger.

> Print statements (logging) are for the developer's benefit. Not the computer's.

Simple 'print' statements miss out on some powerful features of Python's inbuilt logging library that can make the developer's life easier. For example:
- saving logging outputs to a file for future reference and debugging
- adding log severity levels for more informative messages and additional context (e.g. debug vs info vs warning)
- highlighting the origin of the log message (i.e which file/line number the message came from)
- using configurations to enforce consistent formatting across the project and enable multiple loggers for different purposes and use cases (e.g. dev vs production)
- automatically recording timestamps of the log messages

The Python [logging library](https://docs.python.org/3/library/logging.html) can help maximise the utility of your print statements. It just takes a couple lines of code in your main script and a configuration file.

At first, I found it challenging to understand how to implement Python logging in my projects in a minimal way. I wanted to be able to instantiate a logger in one place without a ton of boiler plate code. But didn't really understand how to achieve this. Where should I instantiate the logger? Do I need to do it in every file? Where do I put my configuration?

This repository is intended to demonstrate how you can set up logging with minimal code for your Python/data science projects. I use this template whenever I start with a new project to use logging from the outset.

## Features
- Typical data science project structure
- Logging configuration driven by configuration files not code
- Different logging configuration for development and production environments
- Logs printed to the terminal
- Logs saved to a new file for each run with the timestamp of the program execution

## Project Structure

```
├── .env                             <- environment variables
├── README.md
├── config                           <- configuration files
│   ├── logging.dev.ini
│   └── logging.prod.ini
├── logs                             <- log files
├── requirements.txt                 <- dependencies
├── setup.py                         <- setup local package
└── src                              <- project source code
    ├── __init__.py
    ├── data_processing              <- data processing code
    │   ├── __init__.py
    │   └── processor.py
    ├── model_training               <- model training code
    │   ├── __init__.py
    │   └── trainer.py
    └── main.py                      <- main function
```

## Getting started

To run this demo project, create an virtual environment and install the src package:

```bash
# install src package in development mode
pip install -e .

# install dependencies in requirements.txt file
pip install -r requirements.txt
```

Run the main program:
```bash
python src/main.py
```

```
# terminal output
2022-08-29 12:52:33,499 - INFO - __main__ - Program started
2022-08-29 12:52:33,499 - INFO - data_processing.processor - Pre-processing data
2022-08-29 12:52:33,499 - INFO - data_processing.processor - Data pre-processing complete
2022-08-29 12:52:33,499 - INFO - model_training.trainer - Training model
2022-08-29 12:52:33,499 - INFO - model_training.trainer - Model training complete
2022-08-29 12:52:33,499 - INFO - __main__ - Program finished
```

The main program is configured to print the logs to the console and as save to a file which is stored in the `logs` directory.

The logs sent to the file also include additional information about the function calls, such as the line location in the file. This can be helpful for debugging after the run has completed.

```
# log file output
2022-08-29 12:59:09,017 - INFO - __main__ - <module>:40 - Program started
2022-08-29 12:59:09,017 - INFO - data_processing.processor - process_data:9 - Pre-processing data
2022-08-29 12:59:09,017 - INFO - data_processing.processor - process_data:11 - Data pre-processing complete
2022-08-29 12:59:09,017 - INFO - model_training.trainer - train:10 - Training model
2022-08-29 12:59:09,017 - INFO - model_training.trainer - train:12 - Model training complete
2022-08-29 12:59:09,017 - INFO - __main__ - <module>:43 - Program finished
```

## Alternative to using a configuration file

If you do not want to use a configuration file, here is a short snippet of code to add 'no-thrills' logging to your projects without a config file.

```python
# src/main.py
import logging
import sys

from data_processing.processor import process_data
from model_training.trainer import train

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Program started")
    process_data()
    train()
    logger.info("Program finished")
```

```python
# src/model_training/trainer.py
import logging

logger = logging.getLogger(__name__)


def train():
    """Dummy training function"""
    logger.info("Training model")
    # model training code here
    logger.info("Model training complete")
```

```python
# src/data_processing/processor.py
import logging

logger = logging.getLogger(__name__)


def process_data():
    """Dummy data processing function"""
    logger.info("Pre-processing data")
    # data preprocessing code here...
    logger.info("Data pre-processing complete")
```

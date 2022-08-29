# Setting up logging for data science projects

This repo demonstrates a simple set up to enable logging in your Python or data science projects.

## Project Structure

The entry point for the program is the `src/main.py` file.

```
 .
├──  .env                           <- environment variables
├──  .gitignore
├──  config                         <- configuration files
│  ├──  logging.dev.ini             <- dev environment logging config
│  └──  logging.prod.ini            <- prod environment logging config
├──  logs                           <- logs output location
├──  README.md
├──  requirements.txt
├──  setup.py
└──  src                            <- project source code
   ├──  __init__.py
   ├──  data_processing             <- data preprocessing code
   │  ├──  __init__.py
   │  └──  processor.py
   ├──  model_training              <- model training code
   │  ├──  __init__.py
   │  └──  trainer.py
   └──  main.py                     <- main function
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

The main program is set to send logs to the console and to a file which is stored in the `logs` directory.

The logs sent the file also include addition information about the function calls including their location in the file. This can be helpful for debugging after the run has completed.

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

If you do not want to use a configuration file, here is a short snippet of code to add basic logging without a configuration file.

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

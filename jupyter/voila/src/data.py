"""Data loaders"""

import datetime
import time
from abc import ABC, abstractmethod

import ffn


class DataLoader(ABC):
    """Responsible for loading data"""

    @abstractmethod
    def get_data(
        self,
        tickers: list[str],
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ):
        """Get data from data source"""


class FfnDataLoader(DataLoader):
    """FFN library data loader"""

    def get_data(self, tickers, start_date, end_date):
        """Get data from Yahoo Finance endpoint using ffn"""
        time.sleep(1)  # avoid spamming
        return ffn.get(tickers, start=start_date, end=end_date)

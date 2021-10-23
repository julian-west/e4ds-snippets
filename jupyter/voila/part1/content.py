"""UI Widgets"""
from abc import ABC, abstractmethod

import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class ContentSection(ABC):
    """Defined section of content"""

    def __init__(
        self,
        name: str,
        description: str,
    ):
        self.name = name
        self.description = description
        self.html_description = self._render_html_description()
        self.content = widgets.Output()

    def _render_html_description(self):
        return widgets.HTML(value=(f"<p><strong>{self.description}</strong></p>"))

    @abstractmethod
    def build(self, stock_prices: pd.DataFrame):
        """Build the content section"""

    @abstractmethod
    def refresh_content(self, stock_prices: pd.DataFrame):
        """Refresh the content"""


class RebasedStockGraph(ContentSection):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)

    def build(self, stock_prices: pd.DataFrame) -> widgets.widgets.widget_box.VBox:
        self.refresh_content(stock_prices)
        return widgets.VBox([self.content])

    def refresh_content(self, stock_prices: pd.DataFrame):
        self.content.clear_output()
        with self.content:
            stock_prices.rebase().plot(figsize=(12, 5))
            plt.title("Share price performance (rebased)")
            plt.show()


class StockStatistics(ContentSection):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)

    def build(self, stock_prices: pd.DataFrame) -> widgets.widgets.widget_box.VBox:
        self.refresh_content(stock_prices)
        return widgets.VBox([self.html_description, self.content])

    def refresh_content(self, stock_prices: pd.DataFrame):
        self.content.clear_output()
        with self.content:
            stock_prices.calc_stats().display()


class Correlations(ContentSection):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)

    def build(self, stock_prices: pd.DataFrame) -> widgets.widgets.widget_box.VBox:
        self.refresh_content(stock_prices)
        return widgets.VBox([self.html_description, self.content])

    def refresh_content(self, stock_prices: pd.DataFrame):
        self.content.clear_output()
        with self.content:
            returns = stock_prices.to_log_returns().dropna()
            correlations = returns.corr()
            sns.heatmap(correlations, fmt=".2f", cmap="Blues", annot=True, cbar=False)
            plt.show()


class Drawdown(ContentSection):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)

    def build(self, stock_prices: pd.DataFrame) -> widgets.widgets.widget_box.VBox:
        self.refresh_content(stock_prices)
        return widgets.VBox([self.html_description, self.content])

    def refresh_content(self, stock_prices: pd.DataFrame):
        self.content.clear_output()
        with self.content:
            stock_prices.to_drawdown_series().plot()
            plt.title("Drawdown Plot")
            plt.show()

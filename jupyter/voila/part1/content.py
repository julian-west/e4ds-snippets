"""UI Widgets"""
import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class ContentSection:
    """Defined section of content"""

    def __init__(self, name: str, description: str, stock_prices: pd.DataFrame):
        self.name = name
        self.description = description
        self.stock_prices = stock_prices
        self.html_description = self._render_html_description()
        self.content = self.build()

    def _render_html_description(self):
        return widgets.HTML(value=(f"<p><strong>{self.description}</strong></p>"))

    def build(self):
        """Build the tab"""
        raise NotImplementedError

    def update(self):
        """Action to update the tab"""
        raise NotImplementedError


class RebasedStockGraph(ContentSection):
    def __init__(self, name: str, description: str, stock_prices: pd.DataFrame):
        super().__init__(name, description, stock_prices)

    def build(self) -> widgets.widgets.widget_box.VBox:
        self.output = widgets.Output()
        with self.output:
            self.stock_prices.rebase().plot(figsize=(12, 5))
            plt.title("Share price performance (rebased)")
            plt.show()

        return widgets.VBox([self.output])


class StockStatistics(ContentSection):
    def __init__(self, name: str, description: str, stock_prices: pd.DataFrame):
        super().__init__(name, description, stock_prices)

    def build(self) -> widgets.widgets.widget_box.VBox:
        self.output = widgets.Output()
        with self.output:
            self.stock_prices.calc_stats().display()

        return widgets.VBox([self.html_description, self.output])


class Correlations(ContentSection):
    def __init__(self, name: str, description: str, stock_prices: pd.DataFrame):
        super().__init__(name, description, stock_prices)

    def build(self) -> widgets.widgets.widget_box.VBox:
        self.output = widgets.Output()
        with self.output:
            returns = self.stock_prices.to_log_returns().dropna()
            correlations = returns.corr()
            sns.heatmap(correlations, fmt=".2f", cmap="Blues", annot=True, cbar=False)
            plt.show()

        return widgets.VBox([self.html_description, self.output])


class Drawdown(ContentSection):
    def __init__(self, name: str, description: str, stock_prices: pd.DataFrame):
        super().__init__(name, description, stock_prices)

    def build(self) -> widgets.widgets.widget_box.VBox:
        self.output = widgets.Output()
        with self.output:
            self.stock_prices.to_drawdown_series().plot()
            plt.title("Drawdown Plot")
            plt.show()

        return widgets.VBox([self.html_description, self.output])

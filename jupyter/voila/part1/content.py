"""UI Widgets"""
import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class ContentSection:
    """Defined section of content"""

    def __init__(self, stock_prices_df: pd.DataFrame, name: str, description: str):
        self.stock_prices_df = stock_prices_df
        self.name = name
        self.description = description
        self.html_description = self._render_html_description()
        self.content = self.build()

    def build(self):
        """Build the tab"""
        raise NotImplementedError

    def update(self):
        """Action to update the tab"""
        raise NotImplementedError

    def _render_html_description(self):
        return widgets.HTML(value=(f"<p><strong>{self.description}</strong></p>"))


class RebasedStockGraph(ContentSection):
    def __init__(self, stock_prices_df: pd.DataFrame, name: str, description: str):
        super().__init__(stock_prices_df, name, description)

    def build(self) -> widgets.widgets.widget_box.VBox:
        self.output = widgets.Output()
        with self.output:
            self.stock_prices_df.rebase().plot(figsize=(12, 5))
            plt.title("Share price performance (rebased)")
            plt.show()

        return widgets.VBox([self.output])

    def update(self):
        pass


class StockStatistics(ContentSection):
    def __init__(self, stock_prices_df: pd.DataFrame, name: str, description: str):
        super().__init__(stock_prices_df, name, description)

    def build(self) -> widgets.widgets.widget_box.VBox:
        self.output = widgets.Output()
        with self.output:
            self.stock_prices_df.calc_stats().display()

        return widgets.VBox([self.html_description, self.output])

    def update(self):
        pass


class Correlations(ContentSection):
    def __init__(self, stock_prices_df: pd.DataFrame, name: str, description: str):
        super().__init__(stock_prices_df, name, description)

    def build(self) -> widgets.widgets.widget_box.VBox:
        self.output = widgets.Output()
        with self.output:
            returns = self.stock_prices_df.to_log_returns().dropna()
            correlations = returns.corr()
            sns.heatmap(correlations, fmt=".2f", cmap="Blues", annot=True, cbar=False)
            plt.show()

        return widgets.VBox([self.html_description, self.output])

    def update(self):
        pass


class Drawdown(ContentSection):
    def __init__(self, stock_prices_df: pd.DataFrame, name: str, description: str):
        super().__init__(stock_prices_df, name, description)

    def build(self) -> widgets.widgets.widget_box.VBox:
        self.output = widgets.Output()
        with self.output:
            self.stock_prices_df.to_drawdown_series().plot()
            plt.title("Drawdown Plot")
            plt.show()

        return widgets.VBox([self.html_description, self.output])

    def update(self):
        pass

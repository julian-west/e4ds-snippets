"""Application user interface (GUI)"""

import ipywidgets as widgets
import pandas as pd
from content import ContentSection
from IPython.display import display
from ipywidgets.widgets.widget_button import Button
from user_input import UserInputWidget

WIDTH = "900px"
PADDING = "10px"


class Gui:
    """Responsible for building the entire user interface"""

    def __init__(
        self,
        user_inputs: list[UserInputWidget],
        action_button: Button,
        main: ContentSection,
        tabs: list[ContentSection],
    ):

        self.user_inputs = {
            user_input.name: user_input.widget for user_input in user_inputs
        }
        self.action_button = action_button
        self.main = main
        self.tabs = tabs

    def build_user_input_section(self):
        self.user_input_section = widgets.HBox(
            [
                widgets.VBox(list(self.user_inputs.values())),
                self.action_button,
            ],
            layout=widgets.Layout(border="dashed 2px", padding=PADDING, width=WIDTH),
        )

    def build_tabs(self, stock_prices: pd.DataFrame):
        """Build tabs and give them a title"""
        self.tab_container = widgets.Tab(
            children=[tab.build(stock_prices) for tab in self.tabs],
            layout=widgets.Layout(height="398px", width=WIDTH),
        )

        for i, tab in enumerate(self.tabs):
            self.tab_container.set_title(i, tab.name)

    def build(self, stock_prices: pd.DataFrame):
        """build user interface from components"""
        self.build_user_input_section()
        self.build_tabs(stock_prices)

        display(self.user_input_section)
        display(self.main.build(stock_prices))
        display(self.tab_container)

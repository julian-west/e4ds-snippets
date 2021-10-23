"""Application user interface (GUI)"""

import ipywidgets as widgets
from content import ContentSection
from IPython.display import display
from ipywidgets.widgets.widget_button import Button
from user_input import UserInputWidget


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

    def build(self):
        """build user interface from components"""

        self.tab_container = widgets.Tab(
            children=[tab.content for tab in self.tabs],
            layout=widgets.Layout(height="398px"),
        )

        for i, tab in enumerate(self.tabs):
            self.tab_container.set_title(i, tab.name)

        display(
            widgets.HBox(
                [
                    widgets.VBox([widget for widget in self.user_inputs.values()]),
                    self.action_button,
                ]
            )
        )
        display(self.main.content, self.tab_container)

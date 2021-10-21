"""Application user interface (GUI)"""

import ipywidgets as widgets
from content import ContentSection
from IPython.display import display


class Gui:
    """Responsible for building the entire user interface"""

    def __init__(self, main: ContentSection, tabs: list[ContentSection]):
        self.user_input_area = None
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

        display(self.main.content, self.tab_container)

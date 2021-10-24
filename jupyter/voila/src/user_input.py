"""User Input"""

import ipywidgets as widgets


class UserInputWidget:
    def __init__(self, name: str, widget: widgets.widget):
        self.name = name
        self.widget = widget

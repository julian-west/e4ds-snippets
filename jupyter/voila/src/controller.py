"""Controller to deal with callbacks - might move this to notebook"""
from src.data import DataLoader
from src.gui import Gui


class Controller:
    """Responsible for dealing with callbacks"""

    def __init__(self, gui: Gui, data_loader: DataLoader, stock_lookup: dict[str, str]):
        self.gui = gui
        self.data_loader = data_loader
        self.stock_lookup = stock_lookup
        self._initialize_action_button()
        self._get_data()
        self.gui.build(self.data)

    def _initialize_action_button(self):
        """Sets action for when a user clicks on the action button"""
        self.gui.action_button.on_click(self.update_content)

    def _convert_companies_to_tickers(self) -> list:
        """Convert the company names to list of ticker symbols"""
        return [
            self.stock_lookup[company]
            for company in self.gui.user_inputs["companies"].value
        ]

    def _get_data(self):
        """Get data using DataLoader after converting company names to tickers"""
        tickers = self._convert_companies_to_tickers()
        self.data = self.data_loader.get_data(
            tickers=tickers,
            start_date=self.gui.user_inputs["start_date"].value,
            end_date=self.gui.user_inputs["end_date"].value,
        )

    def update_content(self, value):
        """Trigger data API call and refresh content sections"""
        self._get_data()
        self.gui.main.refresh_content(self.data)

        for tab in self.gui.tabs:
            tab.refresh_content(self.data)

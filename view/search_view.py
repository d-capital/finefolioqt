from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from .exchange_view import ExchangeComparisonWindow   # import your modal


class SearchWidget(QWidget):
    def __init__(self, language="en", parent=None):
        super().__init__(parent)
        self.language = language

        self.currencyPairs = [
            'NZD/JPY','EUR/NZD','GBP/NZD','NZD/CHF','USD/JPY','EUR/USD',
            'GBP/USD','AUD/JPY','USD/CHF','EUR/AUD','GBP/AUD','NZD/CAD',
            'AUD/CHF','CAD/JPY','EUR/CAD','USD/CAD','AUD/NZD','GBP/CAD',
            'CAD/CHF','AUD/CAD','GBP/CHF','CHF/JPY','EUR/CHF','NZD/USD',
            'AUD/USD','GBP/JPY','EUR/JPY','EUR/GBP'
        ]
        self.filteredPairs = list(self.currencyPairs)

        if self.language == "ru":
            self.placeholder = "Искать валютную пару ..."
        else:
            self.placeholder = "Search currency pair..."

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Input field
        self.input = QLineEdit()
        self.input.setPlaceholderText(self.placeholder)
        self.input.textChanged.connect(self.onInputChange)
        self.input.returnPressed.connect(self.onEnter)
        layout.addWidget(self.input)

        # Dropdown (list)
        self.dropdown = QListWidget()
        self.dropdown.itemClicked.connect(self.onSelect)
        layout.addWidget(self.dropdown)

        self.setLayout(layout)
        self.refreshDropdown()

    def refreshDropdown(self):
        self.dropdown.clear()
        for pair in self.filteredPairs:
            item = QListWidgetItem(pair)
            self.dropdown.addItem(item)

    def onInputChange(self, text):
        self.filteredPairs = [p for p in self.currencyPairs if text.lower() in p.lower()]
        self.refreshDropdown()

    def onSelect(self, item: QListWidgetItem):
        pair = item.text()
        self.openComparison(pair)

    def onEnter(self):
        text = self.input.text()
        if text in self.currencyPairs:
            self.openComparison(text)
        elif self.filteredPairs:
            self.openComparison(self.filteredPairs[0])

    def openComparison(self, pair: str):
        ticker = pair.replace("/", ".").lower()
        dlg = ExchangeComparisonWindow(ticker, language=self.language, parent=self)
        dlg.exec()

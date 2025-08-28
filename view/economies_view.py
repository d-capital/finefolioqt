import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, 
    QTableWidgetItem, QLabel, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from models.country import Country, CountriesRequest
from db.session import get_session
from db.session import engine
from sqlmodel import Session
from repositories.macrodata import MacroDataRepository
from view.macro_event_view import MacroEventWindow
from PyQt6.QtWidgets import QMessageBox
from view.search_view import SearchWidget

class EconomiesComparison(QWidget):
    def __init__(self, language="en"):
        super().__init__()

        # Localization
        self.language = language
        if self.language == "ru":
            self.tableTitle = "Экономические показатели стран"
            self.countryLabel = "Страна"
            self.gdpLabel = "Рост ВВП"
            self.interestRateLabel = "Ключевая Ставка"
            self.inflationLabel = "Инфляция"
            self.unemploymentLabel = "Безработица"

            self.countryMap = {
                "usd": "США",
                "gbp": "Великобритания",
                "eur": "ЕС",
                "jpy": "Япония",
                "cad": "Канада",
                "nzd": "Новая Зеландия",
                "chf": "Швейцария",
                "aud": "Австралия",
            }
        else:
            self.tableTitle = "Economic Indicators by country"
            self.countryLabel = "Country"
            self.gdpLabel = "GDP Growth"
            self.interestRateLabel = "Interest Rate"
            self.inflationLabel = "Inflation Rate"
            self.unemploymentLabel = "Unemployment Rate"

            self.countryMap = {
                "usd": "USA",
                "gbp": "United Kingdom",
                "eur": "European Union",
                "jpy": "Japan",
                "cad": "Canada",
                "nzd": "New Zealand",
                "chf": "Switzerland",
                "aud": "Australia",
            }

        # Dummy data (replace with API results)
        session: Session = Session(engine)
        self.countries = MacroDataRepository(session).get_countries_last_events([
            "usd",
            "eur",
            "gbp",
            "cad",
            "jpy",
            "chf",
            "aud",
            "nzd"
            ])

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel(self.tableTitle)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Table
        self.table = QTableWidget(len(self.countries), 5)
        self.table.setHorizontalHeaderLabels([
            self.countryLabel,
            self.gdpLabel,
            self.interestRateLabel,
            self.inflationLabel,
            self.unemploymentLabel
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Populate rows
        for row, country in enumerate(self.countries):
            item = QTableWidgetItem(self.countryMap.get(country.code,country.code))
            self.table.setItem(row,0,item)
            self.addLink(row, 1, str(country.gdp_growth), "gdp", country.code)
            self.addLink(row, 2, str(country.interest_rate), "ir", country.code)
            self.addLink(row, 3, str(country.inflation_rate), "inf", country.code)
            self.addLink(row, 4, str(country.unemployment_rate), "une", country.code)

        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle("Economic Dashboard")

    def addLink(self, row, col, text, event_type, country_code):
        item = QTableWidgetItem(text)
        item.setForeground(Qt.GlobalColor.blue)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.table.setItem(row, col, item)

        def open_window():
            try:
                dlg = MacroEventWindow(event_type, country_code, self.language, parent=self)
                dlg.exec()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

        self.table.itemClicked.connect(
            lambda clicked_item: open_window() if clicked_item == item else None
        )

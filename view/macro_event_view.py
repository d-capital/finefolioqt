import csv
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QFileDialog, QHeaderView
)
from PyQt6.QtCore import Qt
from repositories.macrodata import MacroDataRepository
from db.session import engine
from sqlmodel import Session


class MacroEventWindow(QDialog):
    def __init__(self, event: str, country: str, language="en", parent=None):
        super().__init__(parent)
        self.event = event
        self.country = country
        self.language = language

        # Localization
        if self.language == "ru":
            self.dateLabel = "Дата"
            self.actualLabel = "Факт"
            self.forecastLabel = "Прогноз"
            self.exportLabel = "Скачать CSV"
        else:
            self.dateLabel = "Date"
            self.actualLabel = "Actual"
            self.forecastLabel = "Forecast"
            self.exportLabel = "Export to CSV"

        # Load data from DB
        session = Session(engine)
        repo = MacroDataRepository(session)
        self.events = repo.get_event_by_type_and_country(event, country)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"{self.event} - {self.country.upper()}"))

        # Table
        self.table = QTableWidget(len(self.events), 3)
        self.table.setHorizontalHeaderLabels([self.dateLabel, self.actualLabel, self.forecastLabel])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for row, e in enumerate(self.events):
            # Format date from unix timestamp (assuming e.dateline is int)
            from datetime import datetime
            date_str = datetime.fromtimestamp(e.dateline).strftime("%Y-%m-%d")

            self.table.setItem(row, 0, QTableWidgetItem(date_str))
            self.table.setItem(row, 1, QTableWidgetItem(str(e.actual)))
            self.table.setItem(row, 2, QTableWidgetItem(str(e.forecast)))

        layout.addWidget(self.table)

        # Export button
        export_btn = QPushButton(self.exportLabel)
        export_btn.clicked.connect(self.export_csv)
        layout.addWidget(export_btn)

        self.setLayout(layout)
        self.setWindowTitle(f"{self.event} history for {self.country.upper()}")
        self.resize(600, 400)

    def export_csv(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save CSV", "macro_events.csv", "CSV Files (*.csv)")
        if not filename:
            return
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([self.dateLabel, self.actualLabel, self.forecastLabel])
            for e in self.events:
                from datetime import datetime
                date_str = datetime.fromtimestamp(e.dateline).strftime("%Y-%m-%d")
                writer.writerow([date_str, e.actual, e.forecast])

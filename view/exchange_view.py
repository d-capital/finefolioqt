from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QGridLayout, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from services.exchange_service import get_exchange_rate   # import your function
import logging
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ExchangeComparisonWindow(QDialog):
    def __init__(self, ticker: str, language="en", parent=None):
        super().__init__(parent)
        self.ticker = ticker
        self.language = language

        # Localization
        if self.language == "ru":
            self.header = "Сравнение Валют"
            self.loadingLabel = "Загружаю..."
            self.exchangeRateLabel = "Обменный Курс:"
            self.forecastPppLabel = "Прогноз (PPP):"
            self.forecastRegressionLabel = "Прогноз (Регрессия): "
            self.noteLabel = "Примечание: представленные здесь данные обновляются раз в день!"
            self.fields = [
                ("Процентная ставка (%)", "first_currency_interest_rate", "second_currency_interest_rate"),
                ("Инфляция г/г (%)", "first_currency_inflation_rate", "second_currency_inflation_rate"),
                ("Безработица (%)", "first_currency_unemployment_rate", "second_currency_unemployment_rate"),
                ("Рост ВВП г/г (%)", "first_currency_gdp_growth_rate", "second_currency_gdp_growth_rate"),
            ]
        else:
            self.header = "Currency Comparison"
            self.loadingLabel = "Loading..."
            self.exchangeRateLabel = "Exchange Rate:"
            self.forecastPppLabel = "Forecast (PPP):"
            self.forecastRegressionLabel = "Regression Based Recommendation:"
            self.noteLabel = "Note: data provided here is updated once a day!"
            self.fields = [
                ("Interest Rate (%)", "first_currency_interest_rate", "second_currency_interest_rate"),
                ("Inflation Rate y/y (%)", "first_currency_inflation_rate", "second_currency_inflation_rate"),
                ("Unemployment Rate (%)", "first_currency_unemployment_rate", "second_currency_unemployment_rate"),
                ("GDP Growth Rate y/y (%)", "first_currency_gdp_growth_rate", "second_currency_gdp_growth_rate"),
            ]

        try:
            logging.debug(msg="This was the ticker: "+self.ticker)
            self.exchangeInfo, self.y_test, self.y_pred = get_exchange_rate(self.ticker)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load exchange data: {e}")
            self.exchangeInfo, self.y_test, self.y_pred = None, None, None

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        title = QLabel(self.header)
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        if not self.exchangeInfo:
            layout.addWidget(QLabel(self.loadingLabel))
            self.setLayout(layout)
            return

        grid = QGridLayout()
        grid.addWidget(QLabel(""), 0, 0)
        grid.addWidget(QLabel(self.exchangeInfo.first_currency_short_code.upper()), 0, 1)
        grid.addWidget(QLabel(self.exchangeInfo.second_currency_short_code.upper()), 0, 2)

        # Fields
        for i, (label, first_key, second_key) in enumerate(self.fields, start=1):
            grid.addWidget(QLabel(label), i, 0)
            grid.addWidget(QLabel(str(getattr(self.exchangeInfo, first_key))), i, 1)
            grid.addWidget(QLabel(str(getattr(self.exchangeInfo, second_key))), i, 2)

        layout.addLayout(grid)

        # Extras
        layout.addWidget(QLabel(f"<b>{self.exchangeRateLabel}</b> {self.exchangeInfo.rate}"))
        layout.addWidget(QLabel(f"<b>{self.forecastPppLabel}</b> {self.exchangeInfo.forecast_ppp}"))

        rec_text = f"<b>{self.forecastRegressionLabel}</b>"
        if self.exchangeInfo.recommendation == "sell":
            layout.addWidget(QLabel(f"{rec_text} <span style='color:red;'>Sell 📉</span>"))
        elif self.exchangeInfo.recommendation == "buy":
            layout.addWidget(QLabel(f"{rec_text} <span style='color:green;'>Buy 📈</span>"))

        layout.addWidget(QLabel(self.noteLabel))

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.setWindowTitle(f"Exchange: {self.ticker}")
        self.resize(600, 400)

        # Add regression chart
        if self.y_test is not None and self.y_pred is not None:
            fig = Figure(figsize=(5, 3))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.plot(self.y_test.values, label='Actual')
            ax.plot(self.y_pred, label='Predicted')
            ax.legend()
            ax.set_title('Exchange Rate Prediction')
            layout.addWidget(canvas)

        self.setLayout(layout)
        self.setWindowTitle(f"Exchange: {self.ticker}")
        self.resize(700, 500)

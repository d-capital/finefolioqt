import sys
import logging
import traceback
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from view.economies_view import EconomiesComparison
from view.search_view import SearchWidget
from jobs.macro_update import update
from apscheduler.schedulers.background import BackgroundScheduler

# --- Setup logging ---
logging.basicConfig(
    filename="error_log.txt",   # log file name
    level=logging.DEBUG,        # log level
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# --- Global exception handler ---
def log_uncaught_exceptions(exctype, value, tb):
    error_msg = "".join(traceback.format_exception(exctype, value, tb))
    logging.error("Uncaught exception:\n%s", error_msg)

sys.excepthook = log_uncaught_exceptions

class MainWindow(QWidget):
    def __init__(self, language="en"):
        super().__init__()
        self.language = language
        self.initUI()
        scheduler = BackgroundScheduler()
        scheduler.add_job(update, 'interval', minutes=15)
        scheduler.start()

        

    def initUI(self):
        layout = QVBoxLayout()

        # Add search on top
        self.search = SearchWidget(language=self.language)
        layout.addWidget(self.search)

        # Add economies comparison table below
        self.economies = EconomiesComparison(language=self.language)
        layout.addWidget(self.economies)

        self.setLayout(layout)
        self.setWindowTitle("FineFolio - Economic Dashboard")
        self.resize(1000, 700)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow(language="en")
    window.show()
    sys.exit(app.exec())

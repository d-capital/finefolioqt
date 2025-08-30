import sys
import logging
import traceback
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout,  QPushButton, QMessageBox
from view.economies_view import EconomiesComparison
from view.search_view import SearchWidget
from jobs.macro_update import update
from apscheduler.schedulers.background import BackgroundScheduler
from PyQt6.QtCore import QThread
from jobs.worker import Worker
from jobs.macro_update import update

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

def update_database():
    update()
    return "Update complete ✅"

class MainWindow(QWidget):
    def __init__(self, language="en"):
        super().__init__()
        self.language = language
        self.initUI()
        

    def initUI(self):
        layout = QVBoxLayout()

        self.update_btn = QPushButton("Run Update")
        self.update_btn.clicked.connect(self.start_update)
        layout.addWidget(self.update_btn)

        # Add search on top
        self.search = SearchWidget(language=self.language)
        layout.addWidget(self.search)

        # Add economies comparison table below
        self.economies = EconomiesComparison(language=self.language)
        layout.addWidget(self.economies)

        self.setLayout(layout)
        self.setWindowTitle("FineFolio - Economic Dashboard")
        self.resize(1000, 700)
    def start_update(self):
        # Disable button while running
        self.update_btn.setEnabled(False)

        # Create thread + worker
        self.thread = QThread()
        self.worker = Worker(update_database)   # pass any function here
        self.worker.moveToThread(self.thread)

        # Connect signals
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.finished.connect(lambda _: self.thread.quit())
        self.worker.finished.connect(lambda _: self.worker.deleteLater())
        self.thread.finished.connect(self.thread.deleteLater)

        # Start
        self.thread.start()

    def on_finished(self, result):
        self.update_btn.setEnabled(True)
        QMessageBox.information(self, "Done", f"Update finished!\n\n{result}")

    def on_error(self, message):
        self.update_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Update failed:\n\n{message}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow(language="en")
    window.show()
    sys.exit(app.exec())

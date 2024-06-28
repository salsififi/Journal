"""
JOURNAL
A training journal application
"""

from PySide6.QtWidgets import QApplication

from journal.ui.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow(app)
    window.show()
    app.exec()

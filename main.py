import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from app.config import SHORT_SERVICE_NAME, APP_VERSION


app = QApplication([])

QCoreApplication.setApplicationName(SHORT_SERVICE_NAME)
QCoreApplication.setApplicationVersion(APP_VERSION)


from app.storage import initialize_storage

initialize_storage()


from app.controllers import account_request
from ui.authentication_view import AuthWidget
from ui.panel_view import PanelWidget


if account_request()["success"]:
    widget = PanelWidget()
else:
    widget = AuthWidget()

widget.show()

sys.exit(app.exec())
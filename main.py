import sys
from PySide6 import QtCore, QtWidgets, QtGui

from ui.authentication_view import AuthWidget
from ui.panel_view import PanelWidget
from app.auth import is_authenticated

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    if is_authenticated():
        widget = PanelWidget()
    else:
        widget = AuthWidget()

    widget.setMinimumSize(450,300)

    screen = QtWidgets.QApplication.primaryScreen().availableGeometry()

    widget.move(
        screen.center().x() - widget.width() // 2,
        screen.top() +15
    )

    widget.show()

    sys.exit(app.exec())
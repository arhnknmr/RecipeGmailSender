from PySide6 import (
    QtCore,
    QtWidgets,
)
from PySide6.QtGui import (
    QIcon,
    Qt
)
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

from app.validators import authentication_validation
from pydantic import ValidationError

from app.helper_functions import resource_path
from app.helper_functions import show_validation_errors
from app.controllers import authentication_request
from app.config import SERVICE_NAME

class AuthWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.define_ui()
        self.setup_ui()
        self.setup_connections()

    #Methods :

    def define_ui(self):

        self.setWindowTitle(SERVICE_NAME)
        self.setWindowIcon(QIcon(resource_path("assets/images/app-icon.svg")))

        self.heading_text = QLabel('Use your (Gmail) to Login',alignment=QtCore.Qt.AlignCenter)
        self.helper_link = QLabel('<a href="https://myaccount.google.com/apppasswords">Create an App password for your Gmail account to login</a>',alignment=QtCore.Qt.AlignCenter)
        self.helper_link.setOpenExternalLinks(True)


        self.gmail_field = QtWidgets.QLineEdit()
        self.gmail_field.setPlaceholderText('Enter your Gmail Address')
        self.gmail_field.setFixedHeight(30)

        self.password_field = QtWidgets.QLineEdit()
        self.password_field.setPlaceholderText("Enter your App password")
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_field.setFixedHeight(30)

        self.login_btn = QPushButton('Connect Account')
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setFixedHeight(40)

    def setup_ui(self):
        layout = QVBoxLayout()
        
        layout.addWidget(self.heading_text)
        layout.addWidget(self.helper_link)

        layout.addWidget(self.gmail_field)
        layout.addWidget(self.password_field)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def setup_connections(self):
        self.login_btn.clicked.connect(self.setup_validation)

    def setup_validation(self):
        try:
            data = authentication_validation(
                gmail_address=self.gmail_field.text(),
                app_password=self.password_field.text()
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.setup_request(data)

    def setup_request(self,data):
        request = authentication_request(
            gmail_address=data.gmail_address,
            app_password=data.app_password
        )

        if request["success"]:

            QMessageBox.information(
                self,
                "Success",
                request["message"]
            )
            
            from ui.panel_view import PanelWidget

            self.panel_window = PanelWidget()
            self.panel_window.show()
            self.close()

        else:
            QMessageBox.critical(
                self,
                "Connection Error",
                request["message"]
            )
from PySide6 import (
    QtCore,
    QtWidgets,
)

from PySide6.QtCore import Qt

from PySide6.QtGui import (
    QIcon,
    QAction,
    QFont,
)
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QWidget,
    QFrame,
)

import re

from pathlib import Path

from app.validators import email_content_validation
from app.validators import create_recipes_validation
from app.validators import delete_recipes_validation
from app.validators import email_pushing_validation
from pydantic import ValidationError

from app.helper_functions import resource_path
from app.helper_functions import show_validation_errors
from app.helper_functions import confirmation_alert

from app.config import SERVICE_NAME
from app.controllers import logout_request
from app.workers import EmailWorker


class PanelWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.define_ui()
        self.define_tools()
        self.define_styles()
        self.setup_ui()
        self.setup_connections()

    #Methods :

    def define_styles(self):
        for input in (
            self.subject_field_input,
        ):
            input.setFixedHeight(30)

        for button in (
            self.logout_btn,
            self.check_content_btn,
            self.save_item_btn,
            self.remove_item_btn,
            self.send_emails_btn,
            self.file_attach_btn,
        ):
            button.setCursor(QtCore.Qt.PointingHandCursor)
            button.setFixedHeight(40)

        for label in (
            self.subject_field_label,
            self.content_field_label,
        ):
            label.setFixedHeight(20)

        for box in (
            self.subject_field_box,
            self.content_field_box,
            self.receiver_field_box,
            self.buttons_box,
        ):
            box.setSpacing(1)

        for action in (
            self.bold_action_tool,
            self.italic_action_tool,
            self.underline_action_tool,
        ):
            self.content_field_toolbar.widgetForAction(action).setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

    def define_ui(self):

        self.setWindowTitle(SERVICE_NAME)
        self.setWindowIcon(QIcon(resource_path("assets/images/app-icon.svg")))

        self.heading_text = QLabel('GmailSenderApp',alignment=QtCore.Qt.AlignCenter)
        self.helper_text = QLabel('Fill the Fields with the correct information and send your e-mail',alignment=QtCore.Qt.AlignCenter)
        self.logout_btn = QPushButton('Logout')

        self.info_section = QVBoxLayout()
        self.info_section.addWidget(self.heading_text)
        self.info_section.addWidget(self.helper_text)
        self.info_section.addWidget(self.logout_btn)


        self.subject_field_label = QLabel('Email Subject:')

        self.subject_field_input = QtWidgets.QLineEdit()
        self.subject_field_input.setPlaceholderText('Enter your e-mail subject')

        self.file_attach_btn = QPushButton('Attach File')


        self.subject_field_box = QVBoxLayout()
        self.subject_field_box.addWidget(self.subject_field_label)
        self.subject_field_box.addWidget(self.subject_field_input)
        self.subject_field_box.addWidget(self.file_attach_btn)


        self.content_field_label = QLabel('Email Content:')

        self.content_field_input = QtWidgets.QTextEdit()
        self.content_field_input.setPlaceholderText('Enter your e-mail content')
        self.content_field_input.setFixedHeight(150)

        self.content_field_toolbar = QtWidgets.QToolBar()

        self.content_field_box = QVBoxLayout()
        self.content_field_box.addWidget(self.content_field_label)
        self.content_field_box.addWidget(self.content_field_toolbar)
        self.content_field_box.addWidget(self.content_field_input)


        self.receiver_field_label = QLabel('Email receiver:')
        
        self.receiver_field_input = QtWidgets.QLineEdit()
        self.receiver_field_input.setPlaceholderText('Enter your e-mail receiver')

        self.receiver_field_box = QVBoxLayout()
        self.receiver_field_box.addWidget(self.receiver_field_label)
        self.receiver_field_box.addWidget(self.receiver_field_input)


        self.text_variables_box = QVBoxLayout()

        self.email_recipes_list = QListWidget()
        self.email_recipes_list.setMaximumHeight(75)

        self.check_content_btn = QPushButton('Check Content')
        self.save_item_btn = QPushButton('Save Item')
        self.remove_item_btn = QPushButton('Remove Item')
        self.send_emails_btn = QPushButton('Start Sending Emails')

        self.buttons_box = QVBoxLayout()
        self.buttons_box.addWidget(self.check_content_btn)
        self.buttons_box.addWidget(self.save_item_btn)
        self.buttons_box.addWidget(self.remove_item_btn)
        self.buttons_box.addWidget(self.send_emails_btn)

    def define_tools(self):
        self.bold_action_tool = QAction("B", self)
        self.bold_action_tool.setCheckable(True)
        self.bold_action_tool.setCheckable(True)
        self.bold_action_tool.triggered.connect(
            lambda: self.content_field_input.setFontWeight(
                QFont.Bold
            )
        )

        self.italic_action_tool = QAction("I", self)
        self.italic_action_tool.setCheckable(True)
        self.italic_action_tool.triggered.connect(
            lambda: self.content_field_input.setFontItalic(
                self.italic_action_tool.isChecked()
            )
        )

        self.underline_action_tool = QAction("U", self)
        self.underline_action_tool.setCheckable(True)
        self.underline_action_tool.triggered.connect(
            lambda: self.content_field_input.setFontUnderline(
                self.underline_action_tool.isChecked()
            )
        )


        self.content_field_toolbar.addAction(self.bold_action_tool)
        self.content_field_toolbar.addAction(self.italic_action_tool)
        self.content_field_toolbar.addAction(self.underline_action_tool)

    def file_upload(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self,"Select File","","All Files (*)")

        if not self.file_path:
            return

        self.file_attach_btn.setText(Path(self.file_path).name)

    def auth_logout(self):
        confirmed = confirmation_alert(self,"Confirm to logout","Are you sure about loggin out ?\n(It will not effect your data)")
        
        if not confirmed :
            return

        from ui.authentication_view import AuthWidget

        result = logout_request()

        if not result["success"]:
            QMessageBox.critical(
                self,
                "Loggout failed",
                result["message"]
            )
            return

        QMessageBox.information(
            self,
            "Logout successed",
            result["message"]
        )

        self.auth_window = AuthWidget()
        self.auth_window.show()
        self.close()

    def analyze_vars_validation(self):

        confirmed = confirmation_alert(self,"Confirm structure change","Are you sure about changing the structure ?\n(This will remove previous structure and recipes !)")

        if not confirmed :
            return

        try:
            data = email_content_validation(
                email_content=self.content_field_input.toPlainText()
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return
        
        self.analyze_vars(data.email_content)

    def analyze_vars(self,email_content):
        while self.text_variables_box.count():
            item = self.text_variables_box.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.text_variables = re.findall(r"\{(.*?)\}", email_content)

        for text_variable in self.text_variables :
            temp_field = QtWidgets.QLineEdit()
            temp_field.setPlaceholderText(f"Enter a value for : {text_variable}")
            temp_field.setObjectName(text_variable)
            temp_field.setFixedHeight(30)
            temp_field.setContentsMargins(1,1,1,1)

            self.text_variables_box.addWidget(temp_field)

        self.recipes = {}

    def create_recipes_validation(self) :

        variables_values = {}

        if not hasattr(self, "text_variables"):
            return
        
        for text_variable in self.text_variables:

            variables_values[text_variable] = self.findChild(QtWidgets.QLineEdit,text_variable).text()

                
        try:
            data = create_recipes_validation(
                email_subject=self.subject_field_input.text(),
                email_content=self.content_field_input.toPlainText(),
                email_content_variables_values=variables_values,
                email_receiver=self.receiver_field_input.text(),
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.create_recipes(data)

    def create_recipes(self, data):
        self.recipes[data.email_receiver] = data.email_content_variables_values

        self.receiver_field_input.clear()
        for text_variable in self.text_variables:
            self.findChild(QtWidgets.QLineEdit,text_variable).clear()

        if not self.email_recipes_list.findItems(data.email_receiver,QtCore.Qt.MatchExactly):
            self.email_recipes_list.addItem(data.email_receiver)

    def delete_recipes_validation(self):
        confirmed = confirmation_alert(self,"Confirm recipe remove","Are you sure about removing this recipe ?\n(This will only remove selcted recipe !)")
        
        if not confirmed :
            return

        current_recipe = self.receiver_field_input.text()

        try:
            data = delete_recipes_validation(
                selected_recipe= self.receiver_field_input.text(),
                email_recipes= getattr(self,'recipes', None)
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.delete_recipes(data.selected_recipe)
        
    def delete_recipes(self,item):
        del self.recipes[item]

        removing_item = self.email_recipes_list.findItems(
            item,
            QtCore.Qt.MatchExactly
        )[0]

        self.email_recipes_list.takeItem(
            self.email_recipes_list.row(removing_item)
        )

        self.receiver_field_input.clear()
        for i in range(self.text_variables_box.count()):
            self.text_variables_box.itemAt(i).widget().clear()

    def show_recipe_data(self, item):

        selected_recipe_data = self.recipes[item.text()]

        self.receiver_field_input.setText(item.text())

        for variable, value in selected_recipe_data.items():

            self.findChild(QtWidgets.QLineEdit,variable).setText(value)

    def send_emails_validation(self):
        confirmed = confirmation_alert(self,"Confirm process start","Are you sure about starting to send emails ?\n(The process may take a few minutes !)")
        
        if not confirmed :
            return

        try:
            data = email_pushing_validation(
                email_subject=self.subject_field_input.text(),
                email_content=self.content_field_input.toPlainText(),
                email_html=self.content_field_input.toHtml(),
                email_file=getattr(self, "file_path", None),
                email_recipes=self.recipes,
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.send_emails(data)

    def send_emails(self, data):
        self.receiver_field_input.clear()

        for text_variable in self.text_variables:
            self.findChild(QtWidgets.QLineEdit,text_variable).clear()

        from ui.process_view import ProcessWidget

        self.process_window = ProcessWidget()
        self.process_window.show()

        self.email_thread = QtCore.QThread()
        self.email_worker = EmailWorker(data)

        self.email_worker.moveToThread(self.email_thread)
        self.email_thread.started.connect(self.email_worker.run)

        self.email_worker.final_result.connect(self.handle_email_result)

        self.email_worker.finished.connect(self.email_thread.quit)
        self.email_worker.finished.connect(self.email_worker.deleteLater)
        self.email_thread.finished.connect(self.email_thread.deleteLater)
        self.email_thread.finished.connect(self.process_window.process_finished)

        self.email_thread.start()

    def handle_email_result(self,result):

        if result["type"] == "error":
            QMessageBox.critical( self, "Process Error", result["message"] )
            return

        current_email_receiver = result["email_receiver"]

        self.process_window.add_pushed_recipe(result["success"], current_email_receiver, result["elapsed_time"])

        if result["success"]:

            del self.recipes[current_email_receiver]
            removing_item = self.email_recipes_list.findItems(current_email_receiver, QtCore.Qt.MatchExactly)[0]
            self.email_recipes_list.takeItem(self.email_recipes_list.row(removing_item))

    def setup_connections(self):
        self.logout_btn.clicked.connect(self.auth_logout)
        self.file_attach_btn.clicked.connect(self.file_upload)
        self.check_content_btn.clicked.connect(self.analyze_vars_validation)
        self.save_item_btn.clicked.connect(self.create_recipes_validation)
        self.remove_item_btn.clicked.connect(self.delete_recipes_validation)
        self.send_emails_btn.clicked.connect(self.send_emails_validation)
        self.email_recipes_list.itemClicked.connect(self.show_recipe_data)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        layout.addLayout(self.info_section)
        layout.addLayout(self.subject_field_box)
        layout.addLayout(self.content_field_box)
        layout.addLayout(self.receiver_field_box)
        layout.addLayout(self.text_variables_box)
        layout.addWidget(self.email_recipes_list)
        layout.addLayout(self.buttons_box)

        content = QWidget()
        content.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(scroll)
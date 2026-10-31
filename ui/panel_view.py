from PySide6 import (
    QtCore,
    QtWidgets,
)

from PySide6.QtCore import (Qt,QDateTime)

from PySide6.QtGui import (
    QAction,
    QFont,
    QColor
)
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QWidget,
    QFrame,
)

import re

from pathlib import Path
from pydantic import ValidationError
from datetime import datetime

from app.controllers import get_saved_contents
from app.controllers import get_saved_contacts
from app.controllers import get_saved_files
from app.controllers import get_saved_receivers
from app.controllers import get_saved_drafts
from app.controllers import save_receiver_request
from app.controllers import save_draft_request

from app.validators import email_content_validation
from app.validators import create_recipes_validation
from app.validators import delete_recipes_validation
from app.validators import email_pushing_validation
from app.validators import save_receiver_validation

from app.helper_functions import setup_ui_defaults
from app.helper_functions import show_validation_errors
from app.helper_functions import confirmation_alert
from app.helper_functions import open_file_dir
from app.helper_functions import insertVariable

from app.storage import FILE_FOLDER_PATH

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
            self.schedule_field_input,
            self.receiver_field_input,
            self.receiver_pick_btn
        ):
            input.setFixedHeight(30)

        for button in (
            self.menu_btn,
            self.save_draft_btn,
            self.import_draft_btn,
            self.check_content_btn,
            self.save_item_btn,
            self.remove_item_btn,
            self.send_emails_btn,
            
            self.file_choose_btn,
            self.file_pick_btn,
        ):
            button.setCursor(QtCore.Qt.PointingHandCursor)
            button.setFixedHeight(40)

        for label in (
            self.subject_field_label,
            self.content_field_label,
            self.schedule_field_checkbox,
            self.file_field_checkbox,
        ):
            label.setFixedHeight(20)

        for box in (
            self.schedule_field_box,
            self.draft_manage_box,
            self.subject_field_box,
            self.content_field_box,
            self.receiver_field_box,
            self.buttons_box,
            self.file_field_box,
        ):
            box.setSpacing(1)

        for action in (
            self.bold_action_tool,
            self.italic_action_tool,
            self.underline_action_tool,
            self.pick_action_tool,
            self.var_action_tool,
        ):
            self.content_field_toolbar.widgetForAction(action).setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

    def define_ui(self):
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred
        )

        setup_ui_defaults(self)


        self.helper_text = QLabel('Fill the Fields with the correct information and send your e-mail',alignment=QtCore.Qt.AlignCenter)
        self.menu_btn = QPushButton('Settings (Menu)')

        self.info_section = QVBoxLayout()
        self.info_section.addWidget(self.heading_text)
        self.info_section.addWidget(self.helper_text)
        self.info_section.addWidget(self.menu_btn)


        self.save_draft_btn = QPushButton('Save in drafts')
        self.import_draft_btn = QPushButton('Import from drafts')

        self.draft_manage_box = QVBoxLayout()
        self.draft_manage_box.addWidget(self.save_draft_btn)
        self.draft_manage_box.addWidget(self.import_draft_btn)


        self.subject_field_label = QLabel('Email Subject:')

        self.subject_field_input = QtWidgets.QLineEdit()
        self.subject_field_input.setPlaceholderText('Enter your e-mail subject')

        self.subject_field_box = QVBoxLayout()
        self.subject_field_box.addWidget(self.subject_field_label)
        self.subject_field_box.addWidget(self.subject_field_input)


        self.schedule_field_checkbox = QtWidgets.QCheckBox('Email Schedule:')
        
        self.schedule_field_input = QtWidgets.QDateTimeEdit(QDateTime.currentDateTime())


        self.schedule_field_box = QVBoxLayout()
        self.schedule_field_box.addWidget(self.schedule_field_checkbox)
        self.schedule_field_box.addWidget(self.schedule_field_input)


        self.file_field_checkbox = QtWidgets.QCheckBox("Email File:")
        self.file_pick_btn = QPushButton('~')
        self.file_choose_btn = QPushButton('Attach File')

        self.file_attach_box = QHBoxLayout()
        self.file_attach_box.addWidget(self.file_choose_btn,5)
        self.file_attach_box.addWidget(self.file_pick_btn,1)

        self.file_field_box = QVBoxLayout()
        self.file_field_box.addWidget(self.file_field_checkbox)
        self.file_field_box.addLayout(self.file_attach_box)


        self.content_field_label = QLabel('Email Content:')
        self.content_field_toolbar = QtWidgets.QToolBar()

        self.content_field_input = QtWidgets.QTextEdit()
        self.content_field_input.setPlaceholderText('Enter your e-mail content')
        self.content_field_input.setFixedHeight(150)

        self.content_field_box = QVBoxLayout()
        self.content_field_box.addWidget(self.content_field_label)
        self.content_field_box.addWidget(self.content_field_toolbar)
        self.content_field_box.addWidget(self.content_field_input)


        self.receiver_field_label = QLabel('Email receiver:')
        
        self.receiver_field_input = QtWidgets.QLineEdit()
        self.receiver_field_input.setPlaceholderText('Enter your e-mail receiver')

        self.receiver_pick_btn = QPushButton("~")
        self.receiver_pick_btn.setCursor(QtCore.Qt.PointingHandCursor)

        self.receiver_insert_box = QHBoxLayout()
        self.receiver_insert_box.addWidget(self.receiver_field_input,5)
        self.receiver_insert_box.addWidget(self.receiver_pick_btn,1)

        self.receiver_field_box = QVBoxLayout()
        self.receiver_field_box.addWidget(self.receiver_field_label)
        self.receiver_field_box.addLayout(self.receiver_insert_box)


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


        self.saved_list_popup = QFrame(self,QtCore.Qt.WindowType.Popup)
        self.saved_list_popup.setFixedSize(150, 150)

        self.saved_list_widget = QListWidget()

        self.saved_list_label = QLabel('Choose an item:',alignment=QtCore.Qt.AlignCenter)

        self.saved_list_layout = QVBoxLayout(self.saved_list_popup)
        self.saved_list_layout.setContentsMargins(4,4,4,4)
        self.saved_list_layout.addWidget(self.saved_list_label)
        self.saved_list_layout.addWidget(self.saved_list_widget)

    def define_tools(self):
        self.bold_action_tool = QAction("B", self)
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

        self.pick_action_tool = QAction("~",self)
        self.pick_action_tool.triggered.connect(
            self.pick_saved_data
            )

        self.var_action_tool = QAction("{}",self)
        self.var_action_tool.triggered.connect(
            lambda: insertVariable(self.content_field_input)
        )


        self.content_field_toolbar.addAction(self.bold_action_tool)
        self.content_field_toolbar.addAction(self.italic_action_tool)
        self.content_field_toolbar.addAction(self.underline_action_tool)

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred
        )

        self.content_field_toolbar.addWidget(spacer)

        self.content_field_toolbar.addAction(self.pick_action_tool)
        self.content_field_toolbar.addAction(self.var_action_tool)

    def file_upload(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self,"Select File","","All Files (*)")

        if not self.file_path:
            return

        self.file_choose_btn.setText(Path(self.file_path).name)

    def file_show(self):
        if not self.file_path:
            return

        open_file_dir(self.file_path)

    def menu_view(self):
        from ui.menu_view import MenuWidget

        self.menu_window = MenuWidget()
        self.menu_window.exec()

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

        if not self.email_recipes_list.findItems(
            data.email_receiver,
            QtCore.Qt.MatchExactly
        ):
            item = QtWidgets.QListWidgetItem(data.email_receiver)

            in_receivers = data.email_receiver in get_saved_receivers()
            in_contacts = data.email_receiver in get_saved_contacts().values()

            if in_receivers and in_contacts:
                item.setForeground(QColor("green"))
            elif in_contacts:
                item.setForeground(QColor("yellow"))
            elif in_receivers:
                item.setForeground(QColor("blue"))

            self.email_recipes_list.addItem(item)

    def delete_recipes_validation(self):
        confirmed = confirmation_alert(self,"Confirm recipe remove","Are you sure about removing this recipe ?\n(This will only remove selcted recipe !)")
        
        if not confirmed :
            return

        current_recipe = self.contact_field_input.text()

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

    def pick_saved_data(self):

        match self.sender():
            case self.file_pick_btn:
                self.saved_list_active = 'file'
                self.saved_datas = get_saved_files()

            case self.pick_action_tool:
                self.saved_list_active = 'content'
                self.saved_datas = get_saved_contents()

            case self.receiver_pick_btn:
                self.saved_list_active = 'contact'
                self.saved_datas = get_saved_contacts()

            case self.import_draft_btn:
                self.saved_list_active = 'draft'
                self.saved_datas = get_saved_drafts()

            case _:
                return

        self.saved_list_widget.clear()
        self.saved_list_widget.addItems(self.saved_datas.keys())

        self.saved_list_type = "file"

        self.saved_list_popup.move(
            self.mapToGlobal(
                self.rect().center() - self.saved_list_popup.rect().center()
            )
        )

        self.saved_list_popup.show()

    def insert_saved_data(self,item):
        match self.saved_list_active:
            case 'file':
                current_data = self.saved_datas.get(item.text())

                self.file_choose_btn.setText(current_data)
                self.file_path = FILE_FOLDER_PATH / current_data

            case 'content':
                current_data = self.saved_datas.get(item.text())

                self.content_field_input.setHtml(current_data)

            case 'contact':
                current_data = self.saved_datas.get(item.text())

                self.receiver_field_input.setText(current_data)

            case 'draft':
                current_data = self.saved_datas.get(item.text())

                self.subject_field_input.setText(item.text())
                self.content_field_input.setHtml(current_data["email_html"])

                self.analyze_vars(current_data["email_content"])

                if current_data["email_file"]:
                    self.file_path = current_data["email_file"]
                    self.file_choose_btn.setText(Path(self.file_path).name)

                if current_data["email_schedule"] :
                    self.schedule_field_checkbox.setChecked(True)
                    self.schedule_field_input.setDateTime(
                    QDateTime(datetime.fromisoformat(
                        current_data["email_schedule"]
                    ))
                )

                self.recipes = current_data["email_recipes"]

                for receiver in self.recipes:
                    item = QtWidgets.QListWidgetItem(receiver)
        
                    in_receivers = receiver in get_saved_receivers()
                    in_contacts = receiver in get_saved_contacts().values()
        
                    if in_receivers and in_contacts:
                        item.setForeground(QColor("green"))
                    elif in_contacts:
                        item.setForeground(QColor("yellow"))
                    elif in_receivers:
                        item.setForeground(QColor("blue"))
        
                    self.email_recipes_list.addItem(item)

            case _:
                return

    def save_draft(self):
        confirmed = confirmation_alert(self,"Confirm draft storage","Are you sure about saving recipe as a draft ?\n(This will save this recipe in drafts and clear the fields)")
        
        if not confirmed :
            return

        try:
            data = email_pushing_validation(
                email_subject=self.subject_field_input.text(),
                email_schedule=(
                    self.schedule_field_input.dateTime().toPython()
                    if self.schedule_field_checkbox.isChecked()
                    else None
                ),
                email_content=self.content_field_input.toPlainText(),
                email_html=self.content_field_input.toHtml(),
                email_file=getattr(self, "file_path", None),
                email_recipes=self.recipes,
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        save_draft_request(data.model_dump(mode="json"))

    def send_emails_validation(self):
        confirmed = confirmation_alert(self,"Confirm process start","Are you sure about starting to send emails ?\n(The process may take a few minutes !)")
        
        if not confirmed :
            return

        try:
            data = email_pushing_validation(
                email_subject=self.subject_field_input.text(),
                email_schedule=(
                    self.schedule_field_input.dateTime().toPython()
                    if self.schedule_field_checkbox.isChecked()
                    else None
                ),
                email_content=self.content_field_input.toPlainText(),
                email_html=self.content_field_input.toHtml(),
                email_file=(
                    getattr(self, "file_path", None)
                    if self.file_field_checkbox.isChecked()
                    else None
                ),
                email_recipes=self.recipes,
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.send_emails(data)

    def send_emails(self, data):
        self.sent_email_receivers = []

        self.receiver_field_input.clear()

        if hasattr(self, "text_variables"):
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
            try:
                data = save_receiver_validation(
                    email_receiver=current_email_receiver
                )
    
            except ValidationError as error:
                show_validation_errors(self,error)
                return

            save_receiver_request(current_email_receiver)

            del self.recipes[current_email_receiver]
            removing_item = self.email_recipes_list.findItems(current_email_receiver, QtCore.Qt.MatchExactly)[0]
            self.email_recipes_list.takeItem(self.email_recipes_list.row(removing_item))

    def setup_connections(self):
        self.menu_btn.clicked.connect(self.menu_view)
        self.save_draft_btn.clicked.connect(self.save_draft)
        self.check_content_btn.clicked.connect(self.analyze_vars_validation)
        self.save_item_btn.clicked.connect(self.create_recipes_validation)
        self.remove_item_btn.clicked.connect(self.delete_recipes_validation)
        self.send_emails_btn.clicked.connect(self.send_emails_validation)
        self.email_recipes_list.itemClicked.connect(self.show_recipe_data)
        
        self.file_choose_btn.clicked.connect(self.file_upload)
        self.file_choose_btn.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.file_choose_btn.customContextMenuRequested.connect(
            self.file_show
        )

        for btn in (
            self.file_pick_btn,
            self.receiver_pick_btn,
            self.import_draft_btn
        ):
            btn.clicked.connect(self.pick_saved_data)
        
        self.saved_list_widget.itemClicked.connect(self.insert_saved_data)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        layout.addLayout(self.info_section)
        layout.addLayout(self.draft_manage_box)
        layout.addLayout(self.subject_field_box)
        layout.addLayout(self.file_field_box)
        layout.addLayout(self.schedule_field_box)
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
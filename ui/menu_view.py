from PySide6 import (
    QtCore,
    QtWidgets,
    
)

from PySide6.QtCore import Qt

from PySide6.QtGui import (
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
    QStackedWidget,
)

import ctypes

from pathlib import Path

from app.validators import save_content_validation
from app.validators import remove_content_validation

from app.validators import save_contact_validation
from app.validators import remove_contact_validation

from app.validators import save_file_validation
from app.validators import remove_file_validation

from app.validators import remove_receiver_validation
from app.validators import remove_draft_validation

from pydantic import ValidationError

from app.helper_functions import setup_ui_defaults
from app.helper_functions import show_validation_errors
from app.helper_functions import confirmation_alert
from app.helper_functions import insertVariable
from app.helper_functions import open_file_dir

from app.storage import FILE_FOLDER_PATH

from app.controllers import logout_request
from app.controllers import get_saved_contents
from app.controllers import get_saved_contacts
from app.controllers import get_saved_files
from app.controllers import get_saved_receivers
from app.controllers import get_saved_drafts

from app.controllers import save_content_request
from app.controllers import delete_content_request

from app.controllers import save_contact_request
from app.controllers import delete_contact_request

from app.controllers import save_file_request
from app.controllers import delete_file_request

from app.controllers import delete_receiver_request
from app.controllers import delete_draft_request


class MenuWidget(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()

        self.define_tabs()
        self.define_tabs_tools()
        self.define_ui()
        self.define_styles()
        self.setup_ui()
        self.setup_connections()

    #Methods :

    def define_styles(self):
        for input in (
            self.content_name_input,
            self.contact_name_input,
            self.file_name_input,
            self.receiver_field_input,
            self.draft_field_input,
        ):
            input.setFixedHeight(30)

        for button in (
            self.exit_btn,
            self.auth_logout_btn,
            self.email_contents_management,
            self.email_contacts_management,
            self.email_files_management,
            self.email_receivers_management,
            self.email_drafts_management,
            self.content_field_btn,
            self.contact_field_btn,
            self.file_field_btn,
            self.receiver_field_btn,
            self.draft_field_btn,
            self.saved_contact_remove,
            self.saved_content_remove,
            self.saved_file_remove,
            self.saved_receiver_remove,
            self.saved_draft_remove,
        ):
            button.setCursor(QtCore.Qt.PointingHandCursor)
            button.setFixedHeight(40)

        for label in (
            self.menu_label,
            self.content_field_label,
            self.contact_field_label,
            self.file_field_label,
            self.receiver_field_label,
            self.draft_field_label,
            self.contact_name_label,
            self.content_name_label,
            self.file_name_label,
        ):
            label.setFixedHeight(20)

        for box in (
            self.menu_box,
        ):
            box.setSpacing(1)

        for container in (
            self.email_contents_container,
            self.email_contacts_container,
            self.email_files_container,
            self.email_receivers_container,
            self.email_drafts_container,
        ):
            container.setContentsMargins(0,0,0,0)
            container.setSpacing(1)

        for list in (
            self.saved_contents_list,
            self.saved_contacts_list,
            self.saved_files_list,
            self.saved_receivers_list,
            self.saved_drafts_list,
        ):
            list.setFixedHeight(75)

        for action in (
            self.bold_action_tool,
            self.italic_action_tool,
            self.underline_action_tool,
            self.var_action_tool,
        ):
            self.content_field_toolbar.widgetForAction(action).setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            
    def define_ui(self):

        setup_ui_defaults(self)


        self.helper_text = QLabel('Choose a Menu Option',alignment=QtCore.Qt.AlignCenter)
        self.exit_btn = QPushButton('Close Menu')

        self.info_section = QVBoxLayout()
        self.info_section.addWidget(self.heading_text)
        self.info_section.addWidget(self.helper_text)
        self.info_section.addWidget(self.exit_btn)

        self.menu_label = QLabel('Menu Options :')
        self.auth_logout_btn = QPushButton('Logout')
        self.email_contents_management = QPushButton('Manage Email Contents')
        self.email_contacts_management = QPushButton('Manage Email contacts')
        self.email_files_management = QPushButton('Manage Email Files')
        self.email_receivers_management = QPushButton('Manage Email Receivers')
        self.email_drafts_management = QPushButton('Manage Email Drafts')

        self.menu_box = QVBoxLayout()
        self.menu_box.addWidget(self.menu_label)
        self.menu_box.addWidget(self.auth_logout_btn)
        self.menu_box.addWidget(self.email_contents_management)
        self.menu_box.addWidget(self.email_contacts_management)
        self.menu_box.addWidget(self.email_files_management)
        self.menu_box.addWidget(self.email_receivers_management)
        self.menu_box.addWidget(self.email_drafts_management)

        
        self.empty_tab = QLabel('Select a Menu Option To Continue !',alignment=QtCore.Qt.AlignCenter)

        self.option_box = QStackedWidget()
        self.option_box.addWidget(self.empty_tab)
        self.option_box.addWidget(self.email_contents_tab)
        self.option_box.addWidget(self.email_contacts_tab)
        self.option_box.addWidget(self.email_files_tab)
        self.option_box.addWidget(self.email_receivers_tab)
        self.option_box.addWidget(self.email_drafts_tab)

        self.option_box.setCurrentWidget(self.empty_tab)

    def define_tabs(self):

        # email_contents

        self.content_name_label = QLabel("Content Name:")

        self.content_name_input = QtWidgets.QLineEdit()
        self.content_name_input.setPlaceholderText('Enter a name for this content')

        self.content_field_label = QLabel("Email Content:")

        self.content_field_toolbar = QtWidgets.QToolBar()

        self.content_field_input = QtWidgets.QTextEdit()
        self.content_field_input.setPlaceholderText("Enter your e-mail content")
        self.content_field_input.setFixedHeight(150)

        self.content_field_btn = QPushButton('Save Content')

        self.saved_contents_list = QListWidget()

        self.all_saved_contents = get_saved_contents()
        for content_key, content_text in self.all_saved_contents.items():
            self.saved_contents_list.addItem(content_key)

        self.saved_content_remove = QPushButton('Remove Content')


        self.email_contents_container = QVBoxLayout()
        self.email_contents_container.addWidget(self.content_name_label)
        self.email_contents_container.addWidget(self.content_name_input)
        self.email_contents_container.addWidget(self.content_field_label)
        self.email_contents_container.addWidget(self.content_field_toolbar)
        self.email_contents_container.addWidget(self.content_field_input)
        self.email_contents_container.addWidget(self.content_field_btn)
        self.email_contents_container.addWidget(self.saved_contents_list)
        self.email_contents_container.addWidget(self.saved_content_remove)

        self.email_contents_tab = QWidget()
        self.email_contents_tab.setLayout(self.email_contents_container)


        # email_contacts

        self.contact_name_label = QLabel("contact Name:")
        
        self.contact_name_input = QtWidgets.QLineEdit()
        self.contact_name_input.setPlaceholderText('Enter a name for this contact')

        self.contact_field_label = QLabel("Email contact:")
        
        self.contact_field_input = QtWidgets.QLineEdit()
        self.contact_field_input.setPlaceholderText("Enter your e-mail contact")
        self.contact_field_input.setFixedHeight(30)

        self.contact_field_btn = QPushButton('Save contact')


        self.saved_contacts_list = QListWidget()

        self.all_saved_contacts = get_saved_contacts()
        for contact_key, contact_text in self.all_saved_contacts.items():
            self.saved_contacts_list.addItem(contact_key)

        self.saved_contact_remove = QPushButton('Remove contact')


        self.email_contacts_container = QVBoxLayout()
        self.email_contacts_container.addWidget(self.contact_name_label)
        self.email_contacts_container.addWidget(self.contact_name_input)
        self.email_contacts_container.addWidget(self.contact_field_label)
        self.email_contacts_container.addWidget(self.contact_field_input)
        self.email_contacts_container.addWidget(self.contact_field_btn)
        self.email_contacts_container.addWidget(self.saved_contacts_list)
        self.email_contacts_container.addWidget(self.saved_contact_remove)

        self.email_contacts_tab = QWidget()
        self.email_contacts_tab.setLayout(self.email_contacts_container)
        
        # email_files

        self.file_name_label = QLabel("File Name:")
        
        self.file_name_input = QtWidgets.QLineEdit()
        self.file_name_input.setPlaceholderText('Enter a name for this file')

        self.file_field_label = QLabel("Email file:")
        
        self.file_field_input = QPushButton("Upload your e-mail file")
        self.file_field_input.setFixedHeight(40)

        self.file_field_btn = QPushButton('Save File')


        self.saved_files_list = QListWidget()

        self.all_saved_files = get_saved_files()
        for file_key, file_text in self.all_saved_files.items():
            self.saved_files_list.addItem(file_key)

        self.saved_file_remove = QPushButton('Remove file')


        self.email_files_container = QVBoxLayout()
        self.email_files_container.addWidget(self.file_name_label)
        self.email_files_container.addWidget(self.file_name_input)
        self.email_files_container.addWidget(self.file_field_label)
        self.email_files_container.addWidget(self.file_field_input)
        self.email_files_container.addWidget(self.file_field_btn)
        self.email_files_container.addWidget(self.saved_files_list)
        self.email_files_container.addWidget(self.saved_file_remove)

        self.email_files_tab = QWidget()
        self.email_files_tab.setLayout(self.email_files_container)
        
        # email_receivers

        self.receiver_field_label = QLabel("Email receiver:")
        
        self.receiver_field_input = QtWidgets.QLineEdit()
        self.receiver_field_input.setReadOnly(True)

        self.receiver_field_btn = QPushButton('Clear receivers')


        self.saved_receivers_list = QListWidget()

        self.all_saved_receivers = get_saved_receivers()
        for receiver in self.all_saved_receivers:
            self.saved_receivers_list.addItem(receiver)

        self.saved_receiver_remove = QPushButton('Remove receiver')


        self.email_receivers_container = QVBoxLayout()
        self.email_receivers_container.addWidget(self.receiver_field_label)
        self.email_receivers_container.addWidget(self.receiver_field_input)
        self.email_receivers_container.addWidget(self.receiver_field_btn)
        self.email_receivers_container.addWidget(self.saved_receivers_list)
        self.email_receivers_container.addWidget(self.saved_receiver_remove)

        self.email_receivers_tab = QWidget()
        self.email_receivers_tab.setLayout(self.email_receivers_container)

        # email_drafts

        self.draft_field_label = QLabel("Email draft:")
        
        self.draft_field_input = QtWidgets.QLineEdit()
        self.draft_field_input.setReadOnly(True)

        self.draft_field_btn = QPushButton('Clear drafts')


        self.saved_drafts_list = QListWidget()

        self.all_saved_drafts = get_saved_drafts()
        for draft in self.all_saved_drafts:
            self.saved_drafts_list.addItem(draft)

        self.saved_draft_remove = QPushButton('Remove draft')


        self.email_drafts_container = QVBoxLayout()
        self.email_drafts_container.addWidget(self.draft_field_label)
        self.email_drafts_container.addWidget(self.draft_field_input)
        self.email_drafts_container.addWidget(self.draft_field_btn)
        self.email_drafts_container.addWidget(self.saved_drafts_list)
        self.email_drafts_container.addWidget(self.saved_draft_remove)

        self.email_drafts_tab = QWidget()
        self.email_drafts_tab.setLayout(self.email_drafts_container)

    def define_tabs_tools(self):
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

        self.content_field_toolbar.addAction(self.var_action_tool)

    def close_window(self):
        self.close()

    def open_file(self):
        self.opened_file_path, _ = QFileDialog.getOpenFileName(self,"Select File","","All Files (*)")

        if not self.opened_file_path:
            return

        self.file_field_input.setText(Path(self.opened_file_path).name)
    
    def show_file(self):
        if not self.opened_file_path:
            return

        open_file_dir(self.opened_file_path)


    def auth_logout(self):
        confirmed = confirmation_alert(self,"Confirm to logout","Are you sure about logging out ?\n(It will not effect your data)")
        
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


    def store_content_validation(self):
        try:
            data = save_content_validation(
                content_name= self.content_name_input.text(),
                email_content= self.content_field_input.toHtml()
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.store_content(data)

    def store_content(self, data):

        is_new_content = data.content_name not in self.all_saved_contents

        confirmed = confirmation_alert(
            self,
            "Confirm content storage",
            "Are you sure about storing this content?\n(If a saved content with the same name exists, it will be updated!)"
        )

        if not confirmed:
            return

        save_content_request(data.content_name,data.email_content)

        self.all_saved_contents[data.content_name] = data.email_content

        if is_new_content:
            self.saved_contents_list.addItem(data.content_name)
        
    def select_saved_content(self,item):
        selected_content_data = self.all_saved_contents[item.text()]

        self.content_name_input.setText(item.text())

        self.content_field_input.setHtml(selected_content_data)

    def delete_content_validation(self):

        try:
            data = remove_content_validation(
                content_name= self.content_name_input.text(),
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.delete_content(data)

    def delete_content(self,data):

        confirmed = confirmation_alert(
            self,
            "Confirm content deletion",
            "Are you sure about deleting this content?\n(It will delete the selected content!)"
        )

        if not confirmed:
            return

        delete_content_request(data.content_name)

        del self.all_saved_contents[data.content_name]

        self.saved_contents_list.takeItem(
            self.saved_contents_list.row(self.saved_contents_list.currentItem())
        )

        
    def store_contact_validation(self):
        try:
            data = save_contact_validation(
                contact_name= self.contact_name_input.text(),
                email_contact= self.contact_field_input.text()
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.store_contact(data)

    def store_contact(self, data):

        is_new_contact = data.contact_name not in self.all_saved_contacts

        confirmed = confirmation_alert(
            self,
            "Confirm contact storage",
            "Are you sure about storing this contact?\n(If a saved contact with the same name exists, it will be updated!)"
        )

        if not confirmed:
            return

        save_contact_request(data.contact_name,data.email_contact)

        self.all_saved_contacts[data.contact_name] = data.email_contact

        if is_new_contact:
            self.saved_contacts_list.addItem(data.contact_name)
        
    def select_saved_contact(self,item):
        selected_contact_data = self.all_saved_contacts[item.text()]

        self.contact_name_input.setText(item.text())

        self.contact_field_input.setText(selected_contact_data)

    def delete_contact_validation(self):

        try:
            data = remove_contact_validation(
                contact_name= self.contact_name_input.text(),
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.delete_contact(data)

    def delete_contact(self,data):

        confirmed = confirmation_alert(
            self,
            "Confirm contact deletion",
            "Are you sure about deleting this contact?\n(It will delete the selected contact!)"
        )

        if not confirmed:
            return

        delete_contact_request(data.contact_name)

        del self.all_saved_contacts[data.contact_name]

        self.saved_contacts_list.takeItem(
            self.saved_contacts_list.row(self.saved_contacts_list.currentItem())
        )
        
        
    def store_file_validation(self):
        try:
            data = save_file_validation(
                file_name= self.file_name_input.text(),
                email_file= self.opened_file_path
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.store_file(data)

    def store_file(self, data):

        is_new_file = data.file_name not in self.all_saved_files

        confirmed = confirmation_alert(
            self,
            "Confirm file storage",
            "Are you sure about storing this file?\n(If a saved file with the same name exists, it will be updated!)"
        )

        if not confirmed:
            return

        save_file_request(data.file_name,data.email_file)

        self.all_saved_files[data.file_name] = data.email_file.name

        if is_new_file:
            self.saved_files_list.addItem(data.file_name)
        
    def select_saved_file(self,item):
        selected_file_data = self.all_saved_files[item.text()]

        self.opened_file_path = FILE_FOLDER_PATH / selected_file_data

        self.file_name_input.setText(item.text())

        self.file_field_input.setText(selected_file_data)

    def delete_file_validation(self):

        try:
            data = remove_file_validation(
                file_name= self.file_name_input.text(),
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.delete_file(data)

    def delete_file(self,data):

        confirmed = confirmation_alert(
            self,
            "Confirm file deletion",
            "Are you sure about deleting this file?\n(It will delete the selected file!)"
        )

        if not confirmed:
            return

        delete_file_request(data.file_name)

        del self.all_saved_files[data.file_name]

        self.saved_files_list.takeItem(
            self.saved_files_list.row(self.saved_files_list.currentItem())
        )


    def clear_receivers_validation(self):
        confirmed = confirmation_alert(
            self,
            "Confirm receivers deletion",
            "Are you sure about deleting all receivers?\n(It will delete all saved receivers!)"
        )

        if not confirmed:
            return

        try:
            data = remove_receiver_validation(
                email_receiver= "*"
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.clear_receivers(data)

    def clear_receivers(self, data):
        delete_receiver_request(data.email_receiver)

        self.all_saved_receivers.clear()
        self.saved_receivers_list.clear()
        
    def select_saved_receiver(self,val):
        self.receiver_field_input.setText(val.text())

    def delete_receiver_validation(self):

        try:
            data = remove_receiver_validation(
                email_receiver= self.receiver_field_input.text(),
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.delete_receiver(data)

    def delete_receiver(self,data):

        confirmed = confirmation_alert(
            self,
            "Confirm receiver deletion",
            "Are you sure about deleting this receiver?\n(It will delete the selected receiver!)"
        )

        if not confirmed:
            return

        delete_receiver_request(data.email_receiver)

        self.all_saved_receivers.remove(data.email_receiver)

        self.saved_receivers_list.takeItem(
            self.saved_receivers_list.row(self.saved_receivers_list.currentItem())
        )


    def clear_drafts_validation(self):
        confirmed = confirmation_alert(
            self,
            "Confirm drafts deletion",
            "Are you sure about deleting all drafts?\n(It will delete all saved drafts!)"
        )

        if not confirmed:
            return

        try:
            data = remove_draft_validation(
                email_subject= "*"
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.clear_drafts(data)

    def clear_drafts(self, data):
        delete_draft_request(data.email_subject)

        self.all_saved_drafts.clear()
        self.saved_drafts_list.clear()
        
    def select_saved_draft(self,val):
        self.draft_field_input.setText(val.text())

    def delete_draft_validation(self):

        try:
            data = remove_draft_validation(
                email_subject= self.draft_field_input.text(),
            )

        except ValidationError as error:
            show_validation_errors(self,error)
            return

        self.delete_draft(data)

    def delete_draft(self,data):

        confirmed = confirmation_alert(
            self,
            "Confirm draft deletion",
            "Are you sure about deleting this draft?\n(It will delete the selected draft!)"
        )

        if not confirmed:
            return

        delete_draft_request(data.email_subject)

        del self.all_saved_drafts[data.email_subject]

        self.saved_drafts_list.takeItem(
            self.saved_drafts_list.row(self.saved_drafts_list.currentItem())
        )


    def email_contents_manager(self):
        self.option_box.setCurrentWidget(
            self.email_contents_tab
        ) 
        
    def email_contacts_manager(self):
        self.option_box.setCurrentWidget(
            self.email_contacts_tab
        )
        
    def email_files_manager(self):
        self.option_box.setCurrentWidget(
            self.email_files_tab
        )

    def email_receivers_manager(self):
        self.option_box.setCurrentWidget(
            self.email_receivers_tab
        )

    def email_drafts_manager(self):
        self.option_box.setCurrentWidget(
            self.email_drafts_tab
        )


    def setup_connections(self):
        self.exit_btn.clicked.connect(self.close_window)
        self.auth_logout_btn.clicked.connect(self.auth_logout)
        self.file_field_input.clicked.connect(self.open_file)
        self.file_field_input.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.file_field_input.customContextMenuRequested.connect(
            self.show_file
        )

        self.email_contents_management.clicked.connect(self.email_contents_manager)
        self.email_contacts_management.clicked.connect(self.email_contacts_manager)
        self.email_files_management.clicked.connect(self.email_files_manager)
        self.email_receivers_management.clicked.connect(self.email_receivers_manager)
        self.email_drafts_management.clicked.connect(self.email_drafts_manager)

        self.content_field_btn.clicked.connect(self.store_content_validation)
        self.saved_contents_list.itemClicked.connect(self.select_saved_content)
        self.saved_content_remove.clicked.connect(self.delete_content_validation)

        self.contact_field_btn.clicked.connect(self.store_contact_validation)
        self.saved_contacts_list.itemClicked.connect(self.select_saved_contact)
        self.saved_contact_remove.clicked.connect(self.delete_contact_validation)

        self.file_field_btn.clicked.connect(self.store_file_validation)
        self.saved_files_list.itemClicked.connect(self.select_saved_file)
        self.saved_file_remove.clicked.connect(self.delete_file_validation)


        self.receiver_field_btn.clicked.connect(self.clear_receivers_validation)
        self.saved_receivers_list.itemClicked.connect(self.select_saved_receiver)
        self.saved_receiver_remove.clicked.connect(self.delete_receiver_validation)


        self.draft_field_btn.clicked.connect(self.clear_drafts_validation)
        self.saved_drafts_list.itemClicked.connect(self.select_saved_draft)
        self.saved_draft_remove.clicked.connect(self.delete_draft_validation)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        layout.addLayout(self.info_section)
        layout.addLayout(self.menu_box)
        layout.addWidget(self.option_box)

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
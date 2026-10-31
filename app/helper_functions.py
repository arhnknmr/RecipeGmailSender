import sys
import json

import os
import ctypes

from html import escape
from pathlib import Path

from PySide6.QtWidgets import (QLabel,QMessageBox,QApplication)

from PySide6.QtGui import QTextCursor,QIcon

from PySide6.QtCore import Qt

from app.storage import DATA_FILE_PATH

from app.config import (SHORT_SERVICE_NAME,FULL_SERVICE_NAME,APP_VERSION)


def setup_ui_defaults(self):

    self.setWindowTitle(SHORT_SERVICE_NAME)
    self.setWindowIcon(QIcon(resource_path("assets/images/app-icon.svg")))
    self.heading_text = QLabel(FULL_SERVICE_NAME+' : '+APP_VERSION,alignment=Qt.AlignCenter)


def insertVariable(input_field):
    cursor = input_field.textCursor()

    if cursor.hasSelection():
        selected_text = cursor.selectedText()
        cursor.insertText(f"{{{selected_text}}}")
    else:
        cursor.insertText("{}")
        cursor.movePosition(QTextCursor.MoveOperation.Left)

    input_field.setTextCursor(cursor)
    input_field.setFocus()


def resource_path(relative_path:str)->str :
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent

    return str(base_path / relative_path)


def show_validation_errors(self, error):

    field_names = {
        "gmail_address": "Gmail Address",
        "app_password": "App Password",
    }

    messages = []

    for err in error.errors():
        field = err["loc"][0]
        field_name = field_names.get(field, field)

        messages.append(
            f"{field_name}:\n{err['msg']}"
        )

    QMessageBox.critical(
        self,
        "Validation Error",
        "\n\n".join(messages)
    )


def confirmation_alert(parent,title,message):

    reply = QMessageBox.question(
        parent,
        title,
        message,
        QMessageBox.StandardButton.Yes |
        QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )

    return reply == QMessageBox.StandardButton.Yes


def load_data_file():
    default_data = {
        "contents": {},
        "contacts": {},
        "files": {},
        "receivers": [],
        "drafts": {},
    }

    if not DATA_FILE_PATH.exists():
        DATA_FILE_PATH.parent.mkdir(parents=True,exist_ok=True)

        with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(
                default_data,
                file,
                ensure_ascii=False,
                indent=4
            )

        return default_data

    with open(DATA_FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    for key, default_value in default_data.items():
        data.setdefault(key, default_value)

    return data


def open_file_dir(file_path):

    file_path = os.path.abspath(os.fspath(file_path))

    ctypes.windll.shell32.ShellExecuteW(
        None,
        "open",
        "explorer.exe",
        f'/select,"{file_path}"',
        None,
        1
    )


def replace_recipe_variables(content, recipe, html=False):

    for variable, value in recipe.items():

        value = str(value)

        if html:
            value = escape(value)

        content = content.replace(
            f"{{{variable}}}",
            value
        )

    return content


def setup_window_size(window, required_width):
    screen = QApplication.primaryScreen()
    screen_width = screen.availableGeometry().width()

    if screen_width < required_width:
        window.showFullScreen()
    else:
        window.resize(required_width, 500)
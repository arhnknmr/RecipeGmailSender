import sys
import re

from html import escape
from pathlib import Path

from PySide6.QtWidgets import QMessageBox


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
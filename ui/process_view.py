from PySide6 import (
    QtCore,
    QtWidgets,
)
from PySide6.QtGui import (
    QColor
)
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QListWidgetItem,
)

from app.helper_functions import setup_ui_defaults


class ProcessWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.define_ui()
        self.define_styles()
        self.setup_ui()

    #Methods :

    def define_styles(self):
       for box in (
            self.info_section,
            self.process_box,
        ):
            box.setSpacing(1)

    def define_ui(self):

        setup_ui_defaults(self)


        self.helper_text = QLabel('App is in process keep it open !',alignment=QtCore.Qt.AlignCenter)

        self.info_section = QVBoxLayout()
        self.info_section.addWidget(self.heading_text)
        self.info_section.addWidget(self.helper_text)

        self.process_box = QtWidgets.QListWidget()
        self.process_box.setFixedHeight(300)

    def add_pushed_recipe(self,success,email_receiver,elapsed_time):
        new_item = QListWidgetItem(f"{email_receiver} in {elapsed_time:.2f}s")
        
        if success:
            new_item.setForeground(QColor("green"))
        else:
            new_item.setForeground(QColor("red"))

        self.process_box.addItem(new_item)

    def process_finished(self):
        self.helper_text.setText('Process is done !\n(You can close this window)')

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        layout.addLayout(self.info_section)
        layout.addWidget(self.process_box)

        self.setLayout(layout)
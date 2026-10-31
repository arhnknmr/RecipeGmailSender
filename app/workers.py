from PySide6 import QtCore

from app.controllers import email_pushing_request


class EmailWorker(QtCore.QObject):

    final_result = QtCore.Signal(dict)
    finished = QtCore.Signal()

    def __init__(self, data):
        super().__init__()
        self.data = data

    @QtCore.Slot()
    def run(self):

        try:
            for result in email_pushing_request(
                self.data.email_schedule,
                self.data.email_subject,
                self.data.email_content,
                self.data.email_html,
                self.data.email_file,
                self.data.email_recipes
            ):
                self.final_result.emit(result)

        finally:
            self.finished.emit()
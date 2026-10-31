from pathlib import Path

from PySide6.QtCore import QStandardPaths


APP_DATA_DIR = None
DATA_FILE_PATH = None
SESSION_FILE_PATH = None
FILE_FOLDER_PATH = None
CREDENTIALS_FILE_PATH = None


def initialize_storage():
    global APP_DATA_DIR
    global DATA_FILE_PATH
    global SESSION_FILE_PATH
    global FILE_FOLDER_PATH

    APP_DATA_DIR = Path(
        QStandardPaths.writableLocation(
            QStandardPaths.AppDataLocation
        )
    )

    DATA_FILE_PATH = APP_DATA_DIR / "data.json"
    SESSION_FILE_PATH = APP_DATA_DIR / "settings.json"
    FILE_FOLDER_PATH = APP_DATA_DIR / "files"

    APP_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    FILE_FOLDER_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    if not DATA_FILE_PATH.exists():
        DATA_FILE_PATH.write_text(
            '{"contents": {}, "contacts": {}, "files": {}, "receivers": [], "drafts": {}}',
            encoding="utf-8"
        )

    if not SESSION_FILE_PATH.exists():
        SESSION_FILE_PATH.write_text(
            '{}',
            encoding="utf-8"
        )
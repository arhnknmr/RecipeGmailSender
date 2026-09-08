import keyring
import json

from app.config import (SERVICE_NAME,SETTINGS_FILE_PATH)


def is_authenticated():

    if not SETTINGS_FILE_PATH.exists():
        return False

    with open(SETTINGS_FILE_PATH, "r", encoding="utf-8") as f:
        gmail_address = json.load(f).get("gmail_address")

    if not gmail_address:
        return False

    app_password = keyring.get_password(
        SERVICE_NAME,
        gmail_address
    )

    if app_password is None:
        return False

    return {
        'gmail_address' : gmail_address,
        'app_password' : app_password
    }
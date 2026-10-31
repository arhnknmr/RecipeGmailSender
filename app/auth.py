import keyring

from app.config import SHORT_SERVICE_NAME


def save_app_password(gmail_address, app_password):
    keyring.set_password(
        SHORT_SERVICE_NAME,
        gmail_address,
        app_password
    )


def get_app_password(gmail_address):
    return keyring.get_password(
        SHORT_SERVICE_NAME,
        gmail_address
    )


def delete_app_password(gmail_address):
    keyring.delete_password(
        SHORT_SERVICE_NAME,
        gmail_address
    )
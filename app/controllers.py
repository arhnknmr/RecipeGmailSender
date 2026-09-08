import smtplib
import keyring
import json
import re
import time
import mimetypes
from email.message import EmailMessage
from pathlib import Path

from app.config import (
    SERVICE_NAME,
    APP_DIR,
    SETTINGS_FILE_PATH,
    SMTP_HOST,
    SMTP_PORT
)

from app.auth import is_authenticated
from app.helper_functions import replace_recipe_variables


def authentication_request(gmail_address, app_password):
    try:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)

        server.login(
            gmail_address,
            app_password
        )

        server.quit()

    except smtplib.SMTPAuthenticationError:
        return {
            "success": False,
            "message": "Gmail address or App Password is incorrect."
        }

    except smtplib.SMTPException as error:
        return {
            "success": False,
            "message": str(error)
        }

    APP_DIR.mkdir(exist_ok=True)

    settings = {
        "authenticated": True,
        "gmail_address": gmail_address
    }

    with open(SETTINGS_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)

    keyring.set_password(
        SERVICE_NAME,
        gmail_address,
        app_password
    )

    
    return {
        "success": True,
        "message": "Account connected successfully."
    }


def logout_request():
    if not SETTINGS_FILE_PATH.exists():
        return {
            "success": False,
            "message": "No authenticated account found."
        }

    try:
        with open(
            SETTINGS_FILE_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            settings = json.load(file)

        gmail_address = settings.get("gmail_address")

        if gmail_address:
            keyring.delete_password(
                SERVICE_NAME,
                gmail_address
            )

        SETTINGS_FILE_PATH.unlink()

        return {
            "success": True,
            "message": "Logged out successfully."
        }

    except keyring.errors.PasswordDeleteError:
        return {
            "success": False,
            "message": "Failed to remove account credentials."
        }

    except (OSError, json.JSONDecodeError) as error:
        return {
            "success": False,
            "message": str(error)
        }


def email_pushing_request(subject, content, html, file, recipes):

    data = is_authenticated()

    if not data:
        yield {
            "type": "error",
            "success": False,
            "message": "Auth checking failed."
        }
        return

    server = None

    try:
        server = smtplib.SMTP_SSL(
            SMTP_HOST,
            SMTP_PORT
        )

        server.login(
            data["gmail_address"],
            data["app_password"]
        )

        if file:
            file_path = Path(file)

            with open(file_path, "rb") as uploaded_file:
                file_data = uploaded_file.read()

            file_name = file_path.name

            mime_type, _ = mimetypes.guess_type(file_path)

            if mime_type:
                maintype, subtype = mime_type.split("/", 1)
            else:
                maintype = "application"
                subtype = "octet-stream"

        for email_receiver, recipe in recipes.items():

            email_message = EmailMessage()

            email_message["From"] = data["gmail_address"]
            email_message["To"] = email_receiver
            email_message["Subject"] = subject

            email_content = replace_recipe_variables(
                content,
                recipe
            )

            html_content = replace_recipe_variables(
                html,
                recipe,
                True
            )

            email_message.set_content(email_content)

            email_message.add_alternative(
                html_content,
                subtype="html"
            )

            if file:
                email_message.add_attachment(
                    file_data,
                    maintype=maintype,
                    subtype=subtype,
                    filename=file_name
                )

            start_time = time.perf_counter()

            try:
                server.send_message(email_message)
                success = True
                message = "Email sent successfully."

            except smtplib.SMTPException as error:
                success = False
                message = str(error)

            elapsed_time = time.perf_counter() - start_time

            yield {
                "type": "email",
                "success": success,
                "message": message,
                "email_receiver": email_receiver,
                "elapsed_time": elapsed_time
            }

    except smtplib.SMTPAuthenticationError:
        yield {
            "type": "error",
            "success": False,
            "message": "Gmail address or App Password is incorrect."
        }

    except smtplib.SMTPException as error:
        yield {
            "type": "error",
            "success": False,
            "message": str(error)
        }

    finally:
        if server:
            server.quit()
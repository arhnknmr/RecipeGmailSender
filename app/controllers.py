import smtplib
import keyring
import json
import re
import time
import mimetypes
import shutil
from email.message import EmailMessage
from pathlib import Path

from app.config import (
    SMTP_HOST,
    SMTP_PORT
)

from app.auth import (save_app_password,delete_app_password,get_app_password)
from app.storage import (DATA_FILE_PATH,SESSION_FILE_PATH,FILE_FOLDER_PATH)

from app.helper_functions import replace_recipe_variables
from app.helper_functions import load_data_file


def account_request(gmail_address=None,app_password=None):
    if gmail_address is None and app_password is None:
        try:
            with open(SESSION_FILE_PATH,"r",encoding="utf-8") as file:
                settings = json.load(file)

            gmail_address = settings.get("gmail_address")

            if not gmail_address:
                return {
                    "success": False,
                    "message": "No authenticated account found."
                }

            app_password = get_app_password(gmail_address)

            if not app_password:
                return {
                    "success": False,
                    "message": "Account credentials not found."
                }

            return {
                "success": True,
                "gmail_address": gmail_address,
                "app_password": app_password
            }

        except (OSError, json.JSONDecodeError) as error:
            return {
                "success": False,
                "message": str(error)
            }

    try:
        server = smtplib.SMTP_SSL(
            SMTP_HOST,
            SMTP_PORT
        )

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

    with open(SESSION_FILE_PATH,"r",encoding="utf-8") as file:
        settings = json.load(file)

    settings["gmail_address"] = gmail_address

    with open(
        SESSION_FILE_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            settings,
            file,
            ensure_ascii=False,
            indent=4
        )

    # ذخیره App Password
    save_app_password(
        gmail_address,
        app_password
    )

    return {
        "success": True,
        "message": "Account connected successfully."
    }


def logout_request():
    try:
        with open(SESSION_FILE_PATH, "r", encoding="utf-8") as file:
            settings = json.load(file)

        gmail_address = settings.get("gmail_address")

        if gmail_address:
            delete_app_password(gmail_address)

        del settings["gmail_address"]

        with open(SESSION_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(
                settings,
                file,
                ensure_ascii=False,
                indent=4
            )

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


def get_saved_contents():

    data = load_data_file()

    return data.get("contents")


def get_saved_contacts():
    
    data = load_data_file()

    return data.get("contacts")


def get_saved_files():
    
    data = load_data_file()

    return data.get("files")


def get_saved_receivers():
    
    data = load_data_file()

    return data.get("receivers")


def get_saved_drafts():

    data = load_data_file()

    return data.get("drafts")


def save_content_request(content_name, email_content):

    saved_data =load_data_file()

    saved_data.setdefault("contents", {})

    saved_data["contents"][content_name] = email_content

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            saved_data,
            file,
            ensure_ascii=False,
            indent=4
        )


def delete_content_request(content_name):

    saved_data = load_data_file()

    contents = saved_data.setdefault("contents", {})

    del contents[content_name]

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            saved_data,
            file,
            ensure_ascii=False,
            indent=4
        )


def save_contact_request(contact_name, email_contact):

    saved_data = load_data_file()

    saved_data.setdefault("contacts", {})

    saved_data["contacts"][contact_name] = email_contact

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            saved_data,
            file,
            ensure_ascii=False,
            indent=4
        )


def delete_contact_request(contact_name):

    saved_data = load_data_file()

    contacts = saved_data.setdefault("contacts", {})

    del contacts[contact_name]

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            saved_data,
            file,
            ensure_ascii=False,
            indent=4
        )

        
def save_file_request(file_name, email_file):

    saved_data = load_data_file()

    saved_data.setdefault("files", {})

    email_file = Path(email_file)

    FILE_FOLDER_PATH.mkdir(parents=True, exist_ok=True)

    destination = FILE_FOLDER_PATH / email_file.name

    shutil.copy2(email_file, destination)

    saved_data["files"][file_name] = str(email_file.name)

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            saved_data,
            file,
            ensure_ascii=False,
            indent=4
        )


def delete_file_request(file_name):

    saved_data = load_data_file()

    files = saved_data.setdefault("files", {})
   
    Path(FILE_FOLDER_PATH/files.get(file_name)).unlink()

    del files[file_name]

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            saved_data,
            file,
            ensure_ascii=False,
            indent=4
        )


def save_receiver_request(email_receiver):

    saved_data = load_data_file()

    receivers = saved_data.setdefault("receivers", [])

    if email_receiver not in receivers:
        receivers.append(email_receiver)

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            saved_data,
            file,
            ensure_ascii=False,
            indent=4
        )


def delete_receiver_request(email_receiver):

    saved_data = load_data_file()

    receivers = saved_data.setdefault("receivers", [])

    if email_receiver == "*":
        receivers.clear()
    else:
        receivers.remove(email_receiver)

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            saved_data,
            file,
            ensure_ascii=False,
            indent=4
        )


def save_draft_request(data):
    saved_data = load_data_file()
    
    saved_data.setdefault("drafts", {})

    saved_data["drafts"][data.pop("email_subject")] = data

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            saved_data,
            file,
            ensure_ascii=False,
            indent=4
        )


def delete_draft_request(email_subject):
    saved_data = load_data_file()
    
    drafts = saved_data.setdefault("drafts", {})

    if email_subject == "*":
            drafts.clear()
    else:
        del drafts[email_subject]

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            saved_data,
            file,
            ensure_ascii=False,
            indent=4
        )


def email_pushing_request(schedule, subject, content, html, file, recipes):

    try:
        with open(SESSION_FILE_PATH,"r",encoding="utf-8") as session_file:
            settings = json.load(session_file)

        gmail_address = settings.get("gmail_address")

        if not gmail_address:
            yield {
                "type": "error",
                "success": False,
                "message": "No Gmail account is authenticated."
            }
            return

        app_password = get_app_password(gmail_address)

        if not app_password:
            yield {
                "type": "error",
                "success": False,
                "message": "Failed to get account credentials."
            }
            return

    except (OSError, json.JSONDecodeError) as error:
        yield {
            "type": "error",
            "success": False,
            "message": str(error)
        }
        return

    server = None

    try:
        server = smtplib.SMTP_SSL(
            SMTP_HOST,
            SMTP_PORT
        )

        server.login(
            gmail_address,
            app_password
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

            email_message["From"] = gmail_address
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

            except Exception as error:
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

    except Exception as error:
        yield {
            "type": "error",
            "success": False,
            "message": str(error)
        }

    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass
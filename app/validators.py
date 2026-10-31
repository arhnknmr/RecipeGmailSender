from pydantic import (
    BaseModel,
    ValidationInfo,
    field_validator,
    EmailStr,
    Field,
    StringConstraints
)

from PySide6.QtGui import QTextDocument

from datetime import datetime, timedelta
from typing import Annotated
from pathlib import Path
import re

from app.helper_functions import load_data_file


class save_content_validation(BaseModel):
    content_name:str = Field(min_length=5,max_length=255)
    email_content: str

    @field_validator("email_content")
    @classmethod
    def validate_email_content(cls, value):
        document = QTextDocument()
        document.setHtml(value)

        plain_text = document.toPlainText()

        variables = re.findall(
            r"\{([^{}]+)\}",
            plain_text
        )

        if not variables:
            raise ValueError(
                "Email content must contain at least one variable."
            )

        return value


class remove_content_validation(BaseModel):
    content_name:str

    @field_validator("content_name")
    @classmethod
    def validate_content_name(cls, value):
        if not value in load_data_file()["contents"]:
            raise ValueError(
                "This content name doesn't exist"
            )

        return value
    

class save_contact_validation(BaseModel):
    contact_name:str = Field(min_length=5,max_length=255)
    email_contact: EmailStr


class remove_contact_validation(BaseModel):
    contact_name:str

    @field_validator("contact_name")
    @classmethod
    def validate_content_name(cls, value):
        if not value in load_data_file()["contacts"]:
            raise ValueError(
                "This contact name doesn't exist"
            )

        return value


class save_file_validation(BaseModel):

    file_name:str = Field(min_length=5,max_length=255)
    email_file: Path

    @field_validator("email_file")
    @classmethod
    def validate_file(cls, value):

        if not value.exists():
            raise ValueError("File does not exist.")

        if not value.is_file():
            raise ValueError("The provided path is not a file.")

        if value.stat().st_size > 10 * 1024 * 1024:
            raise ValueError("File size must not exceed 10 MB.")

        return value


class remove_file_validation(BaseModel):
    file_name:str

    @field_validator("file_name")
    @classmethod
    def validate_content_name(cls, value):
        if not value in load_data_file()["files"]:
            raise ValueError(
                "This file name doesn't exist"
            )

        return value


class save_receiver_validation(BaseModel):
    email_receiver: EmailStr


class remove_receiver_validation(BaseModel):
    email_receiver: str

    @field_validator("email_receiver")
    @classmethod
    def validate_email_receiver(cls, value):
        saved_receivers = load_data_file()["receivers"]

        if not saved_receivers:
            raise ValueError(
                "Saved receivers list is empty"
            )

        if value == "*":
            return value

        if value not in saved_receivers:
            raise ValueError(
                "This receiver doesn't exist"
            )

        return value


class remove_draft_validation(BaseModel):
    email_subject: str

    @field_validator("email_subject")
    @classmethod
    def validate_email_subject(cls, value):
        saved_drafts = load_data_file()["drafts"]

        if not saved_drafts:
            raise ValueError(
                "Saved drafts list is empty"
            )

        if value == "*":
            return value

        if value not in saved_drafts:
            raise ValueError(
                "This draft doesn't exist"
            )

        return value


class authentication_validation(BaseModel):
    gmail_address: EmailStr
    app_password: str = Field(min_length=16, max_length=16)

    @field_validator("gmail_address")
    @classmethod
    def validate_gmail_address(cls, value):
        if not value.endswith("@gmail.com"):
            raise ValueError("ایمیل باید از نوع Gmail باشد")

        return value

    @field_validator("app_password", mode="before")
    @classmethod
    def correct_app_password(cls, value):
        return value.replace(" ", "")


class email_content_validation(BaseModel):
    email_content: str

    @field_validator("email_content")
    @classmethod
    def validate_email_content(cls, value):
        variables = re.findall(r"\{([^{}]+)\}", value)

        if not variables:
            raise ValueError(
                "Email content must contain at least one variable."
            )

        return value


class create_recipes_validation(BaseModel):
    email_receiver:EmailStr
    email_subject: str = Field(min_length=5, max_length=255)
    email_content_variables_values:dict[str,str]
    email_content: str

    @field_validator("email_content_variables_values")
    @classmethod
    def validate_variables_values(cls, value):

        for key, val in value.items():

            if not key.strip():
                raise ValueError(
                    "Variable name cannot be empty."
                )

            if not 1 <= len(key) <= 50:
                raise ValueError(
                    "Variable name must be between 1 and 50 characters."
                )

            if re.search(r"\s", key):
                raise ValueError(
                    "Variable must not contain spaces "
                    "(use underscore instead)."
                )

            if not 1 <= len(val.strip()) <= 255:
                raise ValueError(
                    "Variable value must be between 1 and 255 characters."
                )

        return value


    @field_validator("email_content")
    @classmethod
    def validate_email_content(cls, value):
        variables = re.findall(r"\{([^{}]+)\}", value)

        if not variables:
            raise ValueError(
                "Email content must contain at least one variable."
            )

        return value


class delete_recipes_validation(BaseModel):
    selected_recipe: EmailStr
    email_recipes: dict[
        EmailStr,
        dict[
            Annotated[
                str,
                StringConstraints(
                    min_length=1,
                    max_length=50
                )
            ],
            Annotated[
                str,
                StringConstraints(
                    min_length=1,
                    max_length=255
                )
            ]
        ]
    ]

    @field_validator('email_recipes')
    @classmethod
    def validate_variables(cls, value, info: ValidationInfo):
        selected_recipe = info.data.get("selected_recipe")

        if selected_recipe not in value:
            raise ValueError(
                "Selected recipe does not exist."
            )

        return value
    

class email_pushing_validation(BaseModel):

    email_subject: str = Field(min_length=5,max_length=255)
    email_schedule: datetime | None = None
    email_content: str
    email_html: str
    email_file: Path | None = None
    email_recipes: dict[
        EmailStr,
        dict[
            Annotated[
                str,
                StringConstraints(
                    min_length=1,
                    max_length=50
                )
            ],
            Annotated[
                str,
                StringConstraints(
                    min_length=1,
                    max_length=255
                )
            ]
        ]
    ]


    @field_validator("email_schedule")
    @classmethod
    def validate_email_schedule(cls, value):
        if value is None:
            return None

        if value < datetime.now() + timedelta(hours=1):
            raise ValueError(
                "Email schedule must be at least one hour from now."
            )

        return value

    @field_validator("email_content")
    @classmethod
    def validate_email_content(cls, value):

        variables = re.findall(r"\{([^{}]+)\}",value)

        if not variables:
            raise ValueError(
                "Email content must contain at least one variable."
            )
        return value

    @field_validator("email_file")
    @classmethod
    def validate_file(cls, value):

        if value is None:
            return None

        if not value.exists():
            raise ValueError("File does not exist.")

        if not value.is_file():
            raise ValueError("The provided path is not a file.")

        if value.stat().st_size > 10 * 1024 * 1024:
            raise ValueError("File size must not exceed 10 MB.")

        return value

    @field_validator('email_recipes')
    @classmethod
    def validate_variables(cls, value, info: ValidationInfo):

        variables = re.findall(r"\{([^{}]+)\}",info.data.get("email_content"))

        for email , recipe in value.items():
            for variable in variables :
                if variable not in recipe:
                    raise ValueError(
                        f"Variable '{variable}' is missing for {email}"
                    )

        return value
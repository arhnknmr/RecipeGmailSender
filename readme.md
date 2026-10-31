# Recipe Gmail Sender

First of all, thank you for taking the time to visit and explore this
project. ❤️

If you find this project useful or interesting, I would really
appreciate it if you could give the repository a ⭐ star on GitHub. It
helps support the project and encourages us to keep improving it and
adding new features.

------------------------------------------------------------------------

## 📌 About The Project

**Recipe Gmail Sender** is a desktop email application built with Python
that helps users send personalized emails through their Gmail account.

The application makes sending personalized messages easier by allowing
users to define email templates with custom variables and provide
different values for each recipient.

For example, you can create a template such as:

``` text
Hello {name},

We are happy to contact you regarding {subject}.
```

Then provide different values for each recipient.

The application handles email processing in the background, helping keep
the user interface responsive while emails are being processed.

------------------------------------------------------------------------

## ✨ Features

### Email Composition and Sending

-   Send emails through Gmail
-   Personalized email templates with custom variables
-   Custom values for each recipient
-   Support for HTML email content
-   Support for email attachments
-   Background email processing
-   Validation of email data before sending

### Contacts and Recipients

-   Save email addresses as contacts
-   Manage saved contacts
-   Import saved contacts for use when composing emails
-   Save all email recipients
-   Keep a history of recipients

### Reusable Content and Attachments

-   Save email text for later reuse
-   Manage saved email text and import it when composing a message
-   Store email attachments in the application's storage
-   Manage saved attachments and import them for reuse

### Drafts

-   Save email compositions as drafts
-   Manage saved drafts
-   Import a draft to continue editing or reuse its content

### Recipient List Color Indicators

Recipient entries are color-coded to indicate whether an address exists
in the current recipient list, the saved contacts, or both:

-   **Green:** The address exists in both the recipient list and saved
    contacts.
-   **Yellow:** The address exists in saved contacts only.
-   **Blue:** The address exists in the recipient list only.

------------------------------------------------------------------------

## 🛠️ Technologies

This project is built with **Python 3** and uses the following libraries
and modules:

-   **PySide6** --- Desktop graphical user interface
-   **Pydantic** --- Data validation
-   **Keyring** --- Secure credential storage
-   **SMTP (Gmail)** --- Email delivery through Gmail's SMTP server
-   **JSON** --- Local storage for application data

For the complete list of project dependencies and their versions, please
see the `requirements.txt` file.

------------------------------------------------------------------------

## 📦 Installation

Clone the repository:

``` bash
git clone <repository-url>
```

Navigate to the project directory:

``` bash
cd ResumeSenderApp
```

Install the required dependencies:

``` bash
pip install -r requirements.txt
```

Then run the application:

``` bash
python main.py
```

------------------------------------------------------------------------

## 🔐 Gmail Authentication

The application currently supports Gmail authentication using a Gmail
App Password. Google OAuth integration is being developed and tested.

Your Gmail password or App Password should never be stored directly in
the source code. Keep credentials and token files private, and do not
commit them to a public repository.

------------------------------------------------------------------------

## 🤝 Open Source

This project is publicly available so that developers and users can
explore the source code, learn from it, modify it, and contribute to its
development.

The project will continue to evolve, and new features and improvements
will be added in future versions.

If you have an idea, find a bug, or would like to contribute, feel free
to open an issue or submit a pull request.

------------------------------------------------------------------------

## 📄 License

Recipe Gmail Sender is open-source software licensed under the **MIT
License**.

You are free to use, modify, distribute, and publish this project or
modified versions of it, provided that the original copyright notice and
license are included.

The initial version of this project was developed by **AmirHossein
(arhnknmr)**.

GitHub: https://github.com/arhnknmr

Please see the `LICENSE` file for the complete license terms.

------------------------------------------------------------------------

## ⭐ Support The Project

If you find **Recipe Gmail Sender** useful, consider giving the
repository a ⭐ star on GitHub.

Your support helps the project grow and motivates us to continue
developing new features.

Thank you for checking out the project! ❤️

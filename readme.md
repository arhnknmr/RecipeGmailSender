# Gmail Sender App

First of all, thank you for taking the time to visit and explore this project. ❤️

If you find this project useful or interesting, I would really appreciate it if you could give the repository a ⭐ star on GitHub. It helps support the project and encourages us to keep improving it and adding new features.

---

## 📌 About The Project

**Gmail Sender App** is a simple desktop application built with Python that allows users to send emails through their Gmail account using Gmail SMTP.

The application is designed to make sending personalized emails easier by allowing users to define email templates with custom variables and provide different values for each recipient.

For example, you can create a template such as:

```text
Hello {name},

We are happy to contact you regarding {subject}.
```

Then provide different values for each recipient.

The application handles the email sending process in the background, allowing the user interface to remain responsive while emails are being sent.

---

## ✨ Features

* Send emails using Gmail SMTP
* Personalized email templates
* Custom variables for each recipient
* Support for HTML email content
* Support for email attachments
* Background email processing
* Validation of email data before sending
* Secure storage of Gmail credentials using the operating system's credential storage
* Simple and lightweight desktop interface

---

## 🛠️ Technologies

This project is built with **Python 3** and the following libraries:

* **PySide6** — Desktop graphical user interface
* **Pydantic** — Data validation
* **Keyring** — Secure credential storage
* **smtplib** — Sending emails through SMTP
* **email** — Creating and formatting email messages

For the complete list of project dependencies and their versions, please see the `requirements.txt` file.

---

## 📦 Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd GmailSenderApp
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Then run the application:

```bash
python main.py
```

---

## 🔐 Gmail Authentication

The application uses Gmail SMTP authentication with a Gmail App Password.

Your Gmail password should never be stored directly in the source code.

The application uses the system credential manager to securely store authentication credentials.

---

## 🤝 Open Source

This project is publicly available so that developers and users can explore the source code, learn from it, modify it, and contribute to its development.

The project will continue to evolve, and new features and improvements will be added in future versions.

If you have an idea, find a bug, or would like to contribute, feel free to open an issue or submit a pull request.

---

## 📄 License

Gmail Sender App is open-source software licensed under the **MIT License**.

You are free to use, modify, distribute, and publish this project or modified versions of it, provided that the original copyright notice and license are included.

The initial version of this project was developed by **AmirHossein (arhnknmr)**.

GitHub: https://github.com/arhnknmr

Please see the `LICENSE` file for the complete license terms.

---

## ⭐ Support The Project

If you find **Gmail Sender App** useful, consider giving the repository a ⭐ star on GitHub.

Your support helps the project grow and motivates us to continue developing new features.

Thank you for checking out the project! ❤️
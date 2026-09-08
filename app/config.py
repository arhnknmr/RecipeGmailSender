from pathlib import Path

SERVICE_NAME = 'RecipeGmailSender'

APP_DIR = Path.home() / ".gmail_sender"

SETTINGS_FILE_PATH = APP_DIR / "settings.json"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
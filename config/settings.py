import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Application Settings
LOG_FILE = 'logs/email_automation.log'
TEMPLATES_DIR = 'templates'
DATA_DIR = 'data'
CONTACTS_FILE = 'data/contacts.csv'
SENT_EMAILS_FILE = 'data/sent_emails.json'

# Email Templates
DEFAULT_TEMPLATES = {
    'welcome': 'welcome_email.html',
    'newsletter': 'newsletter.html',
    'reminder': 'reminder.html'
}


# config/settings.py

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

DATA_DIR = "data"
LOG_FILE = "logs/email_automation.log"
SENT_EMAILS_FILE = f"{DATA_DIR}/sent_emails.json"
CONTACTS_FILE = f"{DATA_DIR}/contacts.csv"

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
import json
from config.settings import *

class EmailSender:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.email_address = EMAIL_ADDRESS
        self.email_password = EMAIL_PASSWORD
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def send_email(self, to_email, subject, body, is_html=False, attachments=None):
        """Send email to recipient"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body to email
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments if any
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            # Connect to server and send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_address, to_email, text)
            server.quit()
            
            # Log successful send
            self.logger.info(f"Email sent successfully to {to_email}")
            self.log_sent_email(to_email, subject)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_bulk_emails(self, recipients, subject, body, is_html=False):
        """Send emails to multiple recipients"""
        results = []
        for recipient in recipients:
            result = self.send_email(recipient, subject, body, is_html)
            results.append({'email': recipient, 'success': result})
        return results
    
    def log_sent_email(self, to_email, subject):
        """Log sent email to JSON file"""
        log_entry = {
            'to': to_email,
            'subject': subject,
            'timestamp': datetime.now().isoformat(),
            'from': self.email_address
        }
        
        os.makedirs(DATA_DIR, exist_ok=True)
        
        try:
            with open(SENT_EMAILS_FILE, 'r') as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
        
        logs.append(log_entry)
        
        with open(SENT_EMAILS_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
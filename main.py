import tkinter as tk
from src.gui import EmailAutomationGUI
import os

def main():
    # Create necessary directories
    os.makedirs('config', exist_ok=True)
    os.makedirs('src', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("""# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# For Gmail, use App Password instead of regular password
# Go to Google Account Settings > Security > App passwords
""")
        print("Created .env file. Please configure your email settings.")
    
    # Create GUI
    root = tk.Tk()
    app = EmailAutomationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
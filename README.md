

---

```markdown
# 📧 Email Automation Tool

A desktop application built with Python for automating email sending, scheduling, template management, and contact handling. Designed for marketers, small businesses, and developers who want to streamline their email workflows.

---

## 🚀 Features

- **Send HTML Emails** instantly using customizable templates
- **Schedule Emails** daily, weekly, or at a custom time
- **Contact Management** with CSV import/export and editing
- **Template Management** with live editing and saving
- **Built-in Logging** and email history tracking
- **Easy-to-use GUI** powered by `tkinter`

---

## 🖼️ User Interface Preview



---![email automation screenshot 1](https://github.com/user-attachments/assets/eec7d6e9-9bd5-46b2-bf84-48197accd306)

![email automation screenshot 2](https://github.com/user-attachments/assets/e67b72f0-8dda-437a-869e-e3ef0a784e00)



![email automation screenshot 3](https://github.com/user-attachments/assets/f0c71776-fd73-46e9-968d-b07d4e2b47ba)



![email automation screenshot 4](https://github.com/user-attachments/assets/b92de30d-c23b-4e2d-b090-eacd146c8c55)

## 📁 Project Structure

```

email\_automation\_tool/
├── main.py                     # Entry point to launch the app
├── requirements.txt            # Python dependencies
├── .env                        # Email credentials (not committed)
├── config/
│   └── settings.py             # Configuration constants
├── src/
│   ├── gui.py                  # Main GUI code
│   ├── email\_sender.py         # Handles sending and logging emails
│   ├── template\_manager.py     # Loads and renders templates
│   └── scheduler.py            # Handles scheduling of emails
├── templates/                  # HTML email templates
├── data/
│   ├── contacts.csv            # Contact list (name, email)
│   └── sent\_emails.json        # Log of sent emails
├── logs/
│   └── email\_automation.log    # System logs

````

---

## ⚙️ Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/email_automation_tool.git
cd email_automation_tool
````

2. **Create a Virtual Environment**

```bash
python -m venv venv
```

3. **Activate the Environment**

* **Windows**:

  ```bash
  venv\Scripts\activate
  ```
* **Mac/Linux**:

  ```bash
  source venv/bin/activate
  ```

4. **Install Dependencies**

```bash
pip install -r requirements.txt
```

5. **Configure Email Settings**

* Run the app once:

  ```bash
  python main.py
  ```
* This creates a `.env` file. Open it and fill in your email credentials:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

🛡️ **Note:** Use an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if using Gmail.

---

## 🧪 Running the App

After setting up `.env`, just run:

```bash
python main.py
```

---

## 📬 Email Templates

Place your `.html` templates inside the `templates/` directory. Use variables like:

```html
<h1>Welcome {{ name }}</h1>
<p>Thanks for joining {{ company_name }}.</p>
```

Pass template variables in JSON format via the GUI.

---

## 📖 Contact Format (`data/contacts.csv`)

```csv
name,email
John Doe,john@example.com
Jane Smith,jane@example.com
```

---

## ✅ Dependencies

* `tkinter`
* `smtplib`
* `schedule==1.2.0`
* `jinja2==3.1.2`
* `pandas==2.0.3`
* `python-dotenv==1.0.0`

---

## 📝 License

MIT License. Feel free to use and modify.

---



---

## 👤 Author

**Ihejirika Tochukwu Daniel**
[[LinkedIn](https://[linkedin.com/in/yourprofile](https://www.linkedin.com/in/tochukwu-ihejirika-daniel-902a51203/))] • [GitHub](https://[github.com/yourusername](https://github.com/Ihejirikatochukwudaniel))

---

## 📌 Disclaimer

This tool sends real emails. Use responsibly and comply with email sending policies and regulations (e.g., CAN-SPAM, GDPR).

```

---



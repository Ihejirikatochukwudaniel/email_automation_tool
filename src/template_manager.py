import os
import json
from jinja2 import Template, FileSystemLoader, Environment
from config.settings import TEMPLATES_DIR, DEFAULT_TEMPLATES

class TemplateManager:
    def __init__(self):
        self.templates_dir = TEMPLATES_DIR
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        self.create_default_templates()
    
    def create_default_templates(self):
        """Create default email templates if they don't exist"""
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Welcome Email Template
        welcome_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; }
                .footer { background-color: #f1f1f1; padding: 10px; text-align: center; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Welcome {{ name }}!</h1>
            </div>
            <div class="content">
                <p>Thank you for joining us. We're excited to have you on board!</p>
                <p>Your account has been created successfully.</p>
                <p>If you have any questions, feel free to reach out to us.</p>
            </div>
            <div class="footer">
                <p>Best regards,<br>{{ company_name }}</p>
            </div>
        </body>
        </html>
        """
        
        # Newsletter Template
        newsletter_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background-color: #2196F3; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; }
                .article { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px; }
                .footer { background-color: #f1f1f1; padding: 10px; text-align: center; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{{ newsletter_title }}</h1>
                <p>{{ date }}</p>
            </div>
            <div class="content">
                <h2>Hi {{ name }},</h2>
                {% for article in articles %}
                <div class="article">
                    <h3>{{ article.title }}</h3>
                    <p>{{ article.content }}</p>
                </div>
                {% endfor %}
            </div>
            <div class="footer">
                <p>{{ company_name }}<br>
                <a href="{{ unsubscribe_link }}">Unsubscribe</a></p>
            </div>
        </body>
        </html>
        """
        
        # Reminder Template
        reminder_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background-color: #FF9800; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; }
                .reminder-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .footer { background-color: #f1f1f1; padding: 10px; text-align: center; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Reminder: {{ reminder_title }}</h1>
            </div>
            <div class="content">
                <p>Hi {{ name }},</p>
                <div class="reminder-box">
                    <h3>{{ reminder_title }}</h3>
                    <p>{{ reminder_message }}</p>
                    <p><strong>Due Date:</strong> {{ due_date }}</p>
                </div>
                <p>Please take action on this reminder.</p>
            </div>
            <div class="footer">
                <p>{{ company_name }}</p>
            </div>
        </body>
        </html>
        """
        
        templates = {
            'welcome_email.html': welcome_template,
            'newsletter.html': newsletter_template,
            'reminder.html': reminder_template
        }
        
        for filename, content in templates.items():
            filepath = os.path.join(self.templates_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    f.write(content)
    
    def get_template(self, template_name):
        """Get template by name"""
        try:
            return self.env.get_template(template_name)
        except Exception as e:
            raise Exception(f"Template {template_name} not found: {str(e)}")
    
    def render_template(self, template_name, **kwargs):
        """Render template with given variables"""
        template = self.get_template(template_name)
        return template.render(**kwargs)
    
    def list_templates(self):
        """List all available templates"""
        templates = []
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.html'):
                templates.append(filename)
        return templates
    
    def create_custom_template(self, name, content):
        """Create a custom template"""
        filepath = os.path.join(self.templates_dir, name)
        with open(filepath, 'w') as f:
            f.write(content)
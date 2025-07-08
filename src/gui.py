import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime
from src.email_sender import EmailSender
from src.template_manager import TemplateManager
from src.scheduler import EmailScheduler
from config.settings import CONTACTS_FILE

class EmailAutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Automation Tool")
        self.root.geometry("800x600")
        
        self.email_sender = EmailSender()
        self.template_manager = TemplateManager()
        self.scheduler = EmailScheduler()
        
        self.create_widgets()
        self.load_contacts()
        
        # Start scheduler
        self.scheduler.start_scheduler()
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Send Email Tab
        self.create_send_email_tab(notebook)
        
        # Schedule Email Tab
        self.create_schedule_email_tab(notebook)
        
        # Templates Tab
        self.create_templates_tab(notebook)
        
        # Contacts Tab
        self.create_contacts_tab(notebook)
    
    def create_send_email_tab(self, notebook):
        """Create send email tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Send Email")
        
        # Recipients
        ttk.Label(frame, text="Recipients:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.recipients_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.recipients_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse Contacts", command=self.browse_contacts).grid(row=0, column=2, padx=5, pady=5)
        
        # Subject
        ttk.Label(frame, text="Subject:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.subject_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.subject_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        
        # Template
        ttk.Label(frame, text="Template:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.template_var = tk.StringVar()
        template_combo = ttk.Combobox(frame, textvariable=self.template_var, width=47)
        template_combo.grid(row=2, column=1, padx=5, pady=5)
        template_combo['values'] = self.template_manager.list_templates()
        
        # Template Variables
        ttk.Label(frame, text="Template Variables (JSON):").grid(row=3, column=0, sticky='nw', padx=5, pady=5)
        self.template_vars_text = tk.Text(frame, width=50, height=10)
        self.template_vars_text.grid(row=3, column=1, padx=5, pady=5)
        
        # Default template vars
        default_vars = '''{
    "name": "John Doe",
    "company_name": "Your Company"
}'''
        self.template_vars_text.insert('1.0', default_vars)
        
        # Send Button
        ttk.Button(frame, text="Send Email", command=self.send_email).grid(row=4, column=1, padx=5, pady=10)
    
    def create_schedule_email_tab(self, notebook):
        """Create schedule email tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Schedule Email")
        
        # Recipients
        ttk.Label(frame, text="Recipients:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.sched_recipients_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.sched_recipients_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        
        # Subject
        ttk.Label(frame, text="Subject:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.sched_subject_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.sched_subject_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        
        # Template
        ttk.Label(frame, text="Template:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.sched_template_var = tk.StringVar()
        sched_template_combo = ttk.Combobox(frame, textvariable=self.sched_template_var, width=47)
        sched_template_combo.grid(row=2, column=1, padx=5, pady=5)
        sched_template_combo['values'] = self.template_manager.list_templates()
        
        # Schedule Time
        ttk.Label(frame, text="Schedule Time (HH:MM):").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.sched_time_var = tk.StringVar(value="09:00")
        ttk.Entry(frame, textvariable=self.sched_time_var, width=20).grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        # Repeat
        ttk.Label(frame, text="Repeat:").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.sched_repeat_var = tk.StringVar(value="once")
        repeat_combo = ttk.Combobox(frame, textvariable=self.sched_repeat_var, width=20)
        repeat_combo.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        repeat_combo['values'] = ['once', 'daily', 'weekly', 'monthly']
        
        # Template Variables
        ttk.Label(frame, text="Template Variables (JSON):").grid(row=5, column=0, sticky='nw', padx=5, pady=5)
        self.sched_template_vars_text = tk.Text(frame, width=50, height=8)
        self.sched_template_vars_text.grid(row=5, column=1, padx=5, pady=5)
        
        # Schedule Button
        ttk.Button(frame, text="Schedule Email", command=self.schedule_email).grid(row=6, column=1, padx=5, pady=10)
        
        # Scheduled Jobs List
        ttk.Label(frame, text="Scheduled Jobs:").grid(row=7, column=0, sticky='nw', padx=5, pady=5)
        self.jobs_listbox = tk.Listbox(frame, width=70, height=6)
        self.jobs_listbox.grid(row=7, column=1, padx=5, pady=5)
        
        # Refresh and Cancel buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=8, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Refresh Jobs", command=self.refresh_jobs).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel Selected", command=self.cancel_job).pack(side='left', padx=5)
    
    def create_templates_tab(self, notebook):
        """Create templates tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Templates")
        
        # Template List
        ttk.Label(frame, text="Available Templates:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.templates_listbox = tk.Listbox(frame, width=30, height=10)
        self.templates_listbox.grid(row=0, column=1, padx=5, pady=5)
        self.templates_listbox.bind('<<ListboxSelect>>', self.on_template_select)
        
        # Template Content
        ttk.Label(frame, text="Template Content:").grid(row=0, column=2, sticky='nw', padx=5, pady=5)
        self.template_content_text = tk.Text(frame, width=50, height=20)
        self.template_content_text.grid(row=0, column=3, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=1, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Refresh Templates", command=self.refresh_templates).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save Template", command=self.save_template).pack(side='left', padx=5)
        ttk.Button(button_frame, text="New Template", command=self.new_template).pack(side='left', padx=5)
        
        self.refresh_templates()
    
    def create_contacts_tab(self, notebook):
        """Create contacts tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Contacts")
        
        # Contacts List
        ttk.Label(frame, text="Contacts:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        # Treeview for contacts
        self.contacts_tree = ttk.Treeview(frame, columns=('Name', 'Email'), show='headings', height=15)
        self.contacts_tree.heading('Name', text='Name')
        self.contacts_tree.heading('Email', text='Email')
        self.contacts_tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Contact", command=self.add_contact).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Edit Contact", command=self.edit_contact).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete Contact", command=self.delete_contact).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Import CSV", command=self.import_contacts).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Export CSV", command=self.export_contacts).pack(side='left', padx=5)
    
    def send_email(self):
        """Send email"""
        try:
            recipients = [email.strip() for email in self.recipients_var.get().split(',')]
            subject = self.subject_var.get()
            template_name = self.template_var.get()
            template_vars = eval(self.template_vars_text.get('1.0', 'end-1c'))
            
            # Render template
            body = self.template_manager.render_template(template_name, **template_vars)
            
            # Send emails
            results = self.email_sender.send_bulk_emails(recipients, subject, body, is_html=True)
            
            # Show results
            success_count = sum(1 for r in results if r['success'])
            messagebox.showinfo("Email Sent", f"Successfully sent {success_count} out of {len(results)} emails")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")
    
    def schedule_email(self):
        """Schedule email"""
        try:
            recipients = [email.strip() for email in self.sched_recipients_var.get().split(',')]
            subject = self.sched_subject_var.get()
            template_name = self.sched_template_var.get()
            template_vars = eval(self.sched_template_vars_text.get('1.0', 'end-1c'))
            schedule_time = self.sched_time_var.get()
            repeat = self.sched_repeat_var.get()
            
            job_id = self.scheduler.schedule_email(
                recipients, subject, template_name, template_vars, schedule_time, repeat
            )
            
            messagebox.showinfo("Email Scheduled", f"Email scheduled successfully. Job ID: {job_id}")
            self.refresh_jobs()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule email: {str(e)}")
    
    def refresh_jobs(self):
        """Refresh scheduled jobs list"""
        self.jobs_listbox.delete(0, tk.END)
        for job in self.scheduler.get_scheduled_jobs():
            job_text = f"{job['id']} - {job['subject']} - {job['status']}"
            self.jobs_listbox.insert(tk.END, job_text)
    
    def cancel_job(self):
        """Cancel selected job"""
        selection = self.jobs_listbox.curselection()
        if selection:
            job_text = self.jobs_listbox.get(selection[0])
            job_id = job_text.split(' - ')[0]
            if self.scheduler.cancel_job(job_id):
                messagebox.showinfo("Job Cancelled", "Job cancelled successfully")
                self.refresh_jobs()
            else:
                messagebox.showerror("Error", "Failed to cancel job")
    
    def browse_contacts(self):
        """Browse and select contacts"""
        # Simple contact selection dialog
        contact_window = tk.Toplevel(self.root)
        contact_window.title("Select Contacts")
        contact_window.geometry("400x300")
        
        # Contact listbox
        contacts_listbox = tk.Listbox(contact_window, selectmode='multiple', width=50, height=15)
        contacts_listbox.pack(padx=10, pady=10)
        
        # Load contacts
        try:
            df = pd.read_csv(CONTACTS_FILE)
            for _, row in df.iterrows():
                contacts_listbox.insert(tk.END, f"{row['name']} - {row['email']}")
        except FileNotFoundError:
            pass
        
        def select_contacts():
            selected_indices = contacts_listbox.curselection()
            selected_emails = []
            for i in selected_indices:
                contact_info = contacts_listbox.get(i)
                email = contact_info.split(' - ')[1]
                selected_emails.append(email)
            self.recipients_var.set(', '.join(selected_emails))
            contact_window.destroy()
        
        ttk.Button(contact_window, text="Select", command=select_contacts).pack(pady=10)
    
    def refresh_templates(self):
        """Refresh templates list"""
        self.templates_listbox.delete(0, tk.END)
        for template in self.template_manager.list_templates():
            self.templates_listbox.insert(tk.END, template)
    
    def on_template_select(self, event):
        """Handle template selection"""
        selection = self.templates_listbox.curselection()
        if selection:
            template_name = self.templates_listbox.get(selection[0])
            try:
                template_path = os.path.join(self.template_manager.templates_dir, template_name)
                with open(template_path, 'r') as f:
                    content = f.read()
                self.template_content_text.delete('1.0', tk.END)
                self.template_content_text.insert('1.0', content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load template: {str(e)}")
    
    def save_template(self):
        """Save current template"""
        selection = self.templates_listbox.curselection()
        if selection:
            template_name = self.templates_listbox.get(selection[0])
            content = self.template_content_text.get('1.0', 'end-1c')
            try:
                template_path = os.path.join(self.template_manager.templates_dir, template_name)
                with open(template_path, 'w') as f:
                    f.write(content)
                messagebox.showinfo("Success", "Template saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save template: {str(e)}")
    
    def new_template(self):
        """Create new template"""
        template_name = tk.simpledialog.askstring("New Template", "Enter template name (with .html extension):")
        if template_name:
            self.template_manager.create_custom_template(template_name, "<!-- New Template -->")
            self.refresh_templates()
            messagebox.showinfo("Success", "New template created")
    
    def load_contacts(self):
        """Load contacts from CSV"""
        try:
            df = pd.read_csv(CONTACTS_FILE)
            for _, row in df.iterrows():
                self.contacts_tree.insert('', 'end', values=(row['name'], row['email']))
        except FileNotFoundError:
            # Create default contacts file
            default_contacts = pd.DataFrame({
                'name': ['John Doe', 'Jane Smith'],
                'email': ['john@example.com', 'jane@example.com']
            })
            os.makedirs(os.path.dirname(CONTACTS_FILE), exist_ok=True)
            default_contacts.to_csv(CONTACTS_FILE, index=False)
            self.load_contacts()
    
    def add_contact(self):
        """Add new contact"""
        contact_window = tk.Toplevel(self.root)
        contact_window.title("Add Contact")
        contact_window.geometry("300x150")
        
        ttk.Label(contact_window, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        name_var = tk.StringVar()
        ttk.Entry(contact_window, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(contact_window, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        email_var = tk.StringVar()
        ttk.Entry(contact_window, textvariable=email_var).grid(row=1, column=1, padx=10, pady=10)
        
        def save_contact():
            try:
                df = pd.read_csv(CONTACTS_FILE)
                new_contact = pd.DataFrame({
                    'name': [name_var.get()],
                    'email': [email_var.get()]
                })
                df = pd.concat([df, new_contact], ignore_index=True)
                df.to_csv(CONTACTS_FILE, index=False)
                
                # Refresh contacts tree
                self.contacts_tree.delete(*self.contacts_tree.get_children())
                self.load_contacts()
                
                contact_window.destroy()
                messagebox.showinfo("Success", "Contact added successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add contact: {str(e)}")
        
        ttk.Button(contact_window, text="Save", command=save_contact).grid(row=2, column=1, padx=10, pady=10)
    
    def edit_contact(self):
        """Edit selected contact"""
        selection = self.contacts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact to edit")
            return
        
        item = self.contacts_tree.item(selection[0])
        values = item['values']
        
        contact_window = tk.Toplevel(self.root)
        contact_window.title("Edit Contact")
        contact_window.geometry("300x150")
        
        ttk.Label(contact_window, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        name_var = tk.StringVar(value=values[0])
        ttk.Entry(contact_window, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(contact_window, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        email_var = tk.StringVar(value=values[1])
        ttk.Entry(contact_window, textvariable=email_var).grid(row=1, column=1, padx=10, pady=10)
        
        def update_contact():
            try:
                df = pd.read_csv(CONTACTS_FILE)
                mask = (df['name'] == values[0]) & (df['email'] == values[1])
                df.loc[mask, 'name'] = name_var.get()
                df.loc[mask, 'email'] = email_var.get()
                df.to_csv(CONTACTS_FILE, index=False)
                
                # Refresh contacts tree
                self.contacts_tree.delete(*self.contacts_tree.get_children())
                self.load_contacts()
                
                contact_window.destroy()
                messagebox.showinfo("Success", "Contact updated successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update contact: {str(e)}")
        
        ttk.Button(contact_window, text="Update", command=update_contact).grid(row=2, column=1, padx=10, pady=10)
    
    def delete_contact(self):
        """Delete selected contact"""
        selection = self.contacts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact to delete")
            return
        
        item = self.contacts_tree.item(selection[0])
        values = item['values']
        
        if messagebox.askyesno("Confirm", f"Delete contact {values[0]}?"):
            try:
                df = pd.read_csv(CONTACTS_FILE)
                mask = (df['name'] == values[0]) & (df['email'] == values[1])
                df = df[~mask]
                df.to_csv(CONTACTS_FILE, index=False)
                
                # Refresh contacts tree
                self.contacts_tree.delete(*self.contacts_tree.get_children())
                self.load_contacts()
                
                messagebox.showinfo("Success", "Contact deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete contact: {str(e)}")
    
    def import_contacts(self):
        """Import contacts from CSV"""
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                new_df = pd.read_csv(file_path)
                existing_df = pd.read_csv(CONTACTS_FILE)
                
                # Merge dataframes
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                combined_df.drop_duplicates(subset=['email'], keep='first', inplace=True)
                combined_df.to_csv(CONTACTS_FILE, index=False)
                
                # Refresh contacts tree
                self.contacts_tree.delete(*self.contacts_tree.get_children())
                self.load_contacts()
                
                messagebox.showinfo("Success", "Contacts imported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import contacts: {str(e)}")
    
    def export_contacts(self):
        """Export contacts to CSV"""
        file_path = filedialog.asksaveasfilename(
            title="Save contacts as",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                df = pd.read_csv(CONTACTS_FILE)
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Contacts exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export contacts: {str(e)}")

# Add missing import
import tkinter.simpledialog
import os
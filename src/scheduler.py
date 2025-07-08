import schedule
import time
import threading
from datetime import datetime, timedelta
import json
import os
from src.email_sender import EmailSender
from src.template_manager import TemplateManager
from config.settings import DATA_DIR

class EmailScheduler:
    def __init__(self):
        self.email_sender = EmailSender()
        self.template_manager = TemplateManager()
        self.scheduled_jobs = []
        self.running = False
        self.scheduler_thread = None
        self.load_scheduled_jobs()
    
    def schedule_email(self, recipients, subject, template_name, template_vars, schedule_time, repeat='once'):
        """Schedule an email to be sent"""
        job_id = f"job_{datetime.now().timestamp()}"
        
        job_data = {
            'id': job_id,
            'recipients': recipients,
            'subject': subject,
            'template_name': template_name,
            'template_vars': template_vars,
            'schedule_time': schedule_time,
            'repeat': repeat,
            'created_at': datetime.now().isoformat(),
            'status': 'scheduled'
        }
        
        self.scheduled_jobs.append(job_data)
        self.save_scheduled_jobs()
        
        # Schedule the job
        if repeat == 'daily':
            schedule.every().day.at(schedule_time).do(self.send_scheduled_email, job_id)
        elif repeat == 'weekly':
            schedule.every().week.at(schedule_time).do(self.send_scheduled_email, job_id)
        elif repeat == 'monthly':
            schedule.every().month.at(schedule_time).do(self.send_scheduled_email, job_id)
        else:  # once
            schedule.every().day.at(schedule_time).do(self.send_scheduled_email, job_id).tag(job_id)
        
        return job_id
    
    def send_scheduled_email(self, job_id):
        """Send a scheduled email"""
        job = next((j for j in self.scheduled_jobs if j['id'] == job_id), None)
        if not job:
            return
        
        try:
            # Render template
            body = self.template_manager.render_template(
                job['template_name'], 
                **job['template_vars']
            )
            
            # Send emails
            results = self.email_sender.send_bulk_emails(
                job['recipients'], 
                job['subject'], 
                body, 
                is_html=True
            )
            
            # Update job status
            job['status'] = 'sent'
            job['sent_at'] = datetime.now().isoformat()
            job['results'] = results
            
            # If it's a one-time job, remove it from schedule
            if job['repeat'] == 'once':
                schedule.clear(job_id)
                self.scheduled_jobs.remove(job)
            
            self.save_scheduled_jobs()
            
        except Exception as e:
            job['status'] = 'failed'
            job['error'] = str(e)
            self.save_scheduled_jobs()
    
    def start_scheduler(self):
        """Start the email scheduler"""
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
    
    def stop_scheduler(self):
        """Stop the email scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
    
    def _run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def get_scheduled_jobs(self):
        """Get all scheduled jobs"""
        return self.scheduled_jobs
    
    def cancel_job(self, job_id):
        """Cancel a scheduled job"""
        job = next((j for j in self.scheduled_jobs if j['id'] == job_id), None)
        if job:
            schedule.clear(job_id)
            self.scheduled_jobs.remove(job)
            self.save_scheduled_jobs()
            return True
        return False
    
    def save_scheduled_jobs(self):
        """Save scheduled jobs to file"""
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(os.path.join(DATA_DIR, 'scheduled_jobs.json'), 'w') as f:
            json.dump(self.scheduled_jobs, f, indent=2)
    
    def load_scheduled_jobs(self):
        """Load scheduled jobs from file"""
        try:
            with open(os.path.join(DATA_DIR, 'scheduled_jobs.json'), 'r') as f:
                self.scheduled_jobs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.scheduled_jobs = []
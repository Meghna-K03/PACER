import os
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
from scraper import search_jobs, match_jobs_to_student
from whatsapp_alerts import send_job_alert
from database import supabase

load_dotenv()

scheduler = BlockingScheduler()

def get_all_students():
    """Get all students from database"""
    try:
        result = supabase.table("students").select("*").execute()
        return result.data
    except Exception as e:
        print(f"Error fetching students: {e}")
        return []

def morning_job_alert():
    """Runs every day at 8am automatically"""
    print("Running morning job alert...")
    
    students = get_all_students()
    print(f"Found {len(students)} students")
    
    jobs = search_jobs("software engineer", "india")
    print(f"Found {len(jobs)} jobs")
    
    for student in students:
        if not student.get("phone"):
            continue
            
        matching = match_jobs_to_student(jobs, student)
        
        if matching:
            phone = f"whatsapp:+91{student['phone']}"
            send_job_alert(student["name"], phone, matching)
            print(f"Alert sent to {student['name']}")

@scheduler.scheduled_job('cron', hour=8, minute=0)
def scheduled_alert():
    morning_job_alert()

if __name__ == "__main__":
    print("PACER Agent starting...")
    print("Will send job alerts every day at 8:00 AM")
    print("Press Ctrl+C to stop")
    
    morning_job_alert()
    scheduler.start()
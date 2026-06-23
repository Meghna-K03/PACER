import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def send_whatsapp(to_number, message):
    """Send a WhatsApp message to a student"""
    try:
        msg = client.messages.create(
            from_=os.getenv("TWILIO_WHATSAPP_FROM"),
            to=to_number,
            body=message
        )
        print(f"Message sent: {msg.sid}")
        return True
    except Exception as e:
        print(f"WhatsApp error: {e}")
        return False

def send_job_alert(student_name, phone_number, jobs):
    """Send job match alert to a student"""
    message = f"Namaste {student_name}! 🎯\n\n"
    message += f"PACER ne aapke liye {len(jobs)} naye opportunities dhundhe hain:\n\n"
    
    for job in jobs[:3]:
        message += f"🏢 {job['title']} at {job['company']}\n"
        message += f"📌 Source: {job['source']}\n\n"
    
    message += "Kisi bhi company ke liye interview prep karne ke liye:\n"
    message += "👉 http://localhost:8000\n\n"
    message += "All the best! 💪"
    
    return send_whatsapp(phone_number, message)

def send_test_message(phone_number):
    """Send a test message to verify setup"""
    message = """Namaste! 🎯

PACER yahan hai — aapka AI placement prep agent!

Main har roz subah 8 baje aapke liye naye job opportunities dhundhunga aur aapko alert karunga.

Taiyaar ho jaao! 💪"""
    
    return send_whatsapp(phone_number, message)
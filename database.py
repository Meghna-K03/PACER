import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def save_student(name, email, branch, cgpa, skills):
    try:
        result = supabase.table("students").insert({
            "name": name,
            "email": email,
            "branch": branch,
            "cgpa": cgpa,
            "skills": skills
        }).execute()
        return result.data[0]
    except Exception as e:
        print(f"Error saving student: {e}")
        return None

def save_session(student_id, company, questions):
    try:
        result = supabase.table("sessions").insert({
            "student_id": student_id,
            "company": company,
            "questions": questions
        }).execute()
        return result.data[0]
    except Exception as e:
        print(f"Error saving session: {e}")
        return None

def get_student_by_email(email):
    try:
        result = supabase.table("students")\
            .select("*")\
            .eq("email", email)\
            .execute()
        if result.data:
            return result.data[0]
        return None
    except Exception as e:
        print(f"Error fetching student: {e}")
        return None

def get_student_sessions(student_id):
    try:
        result = supabase.table("sessions")\
            .select("*")\
            .eq("student_id", student_id)\
            .order("created_at", desc=True)\
            .execute()
        return result.data
    except Exception as e:
        print(f"Error fetching sessions: {e}")
        return []
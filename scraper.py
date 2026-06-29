import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
API_KEY = os.getenv("ADZUNA_API_KEY")

def search_jobs(keyword="software engineer", location="india", results=10):
    """Search for jobs using Adzuna API"""
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    
    params = {
        "app_id": APP_ID,
        "app_key": API_KEY,
        "results_per_page": results,
        "what": keyword,
        "where": location,
        "content-type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        jobs = []
        for job in data.get("results", []):
            jobs.append({
                "title": job.get("title", ""),
                "company": job.get("company", {}).get("display_name", ""),
                "location": job.get("location", {}).get("display_name", ""),
                "description": job.get("description", "")[:200],
                "url": job.get("redirect_url", ""),
                "salary_min": job.get("salary_min", ""),
                "salary_max": job.get("salary_max", ""),
                "source": "Adzuna"
            })
        
        return jobs
    
    except Exception as e:
        print(f"Adzuna API error: {e}")
        return []

def match_jobs_to_student(jobs, student):
    """Check if any jobs match this student's profile"""
    skills = student.get("skills", "").lower()
    branch = student.get("branch", "").lower()
    
    keywords = skills.split(",") + [branch]
    keywords = [k.strip() for k in keywords if k.strip()]
    
    matching = []
    for job in jobs:
        job_title = job["title"].lower()
        job_desc = job["description"].lower()
        
        for keyword in keywords:
            if keyword and (keyword in job_title or keyword in job_desc):
                matching.append(job)
                break
    
    return matching

if __name__ == "__main__":
    print("Testing Adzuna API...")
    jobs = search_jobs("software engineer", "india")
    print(f"Found {len(jobs)} jobs")
    for job in jobs[:5]:
        print(f"- {job['title']} at {job['company']} ({job['location']})")
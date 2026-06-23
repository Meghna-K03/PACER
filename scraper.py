import requests
from bs4 import BeautifulSoup

def scrape_internshala(keyword="software engineer"):
    """Scrape Internshala for recent job listings"""
    url = f"https://internshala.com/jobs/{keyword.replace(' ', '-')}-jobs"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        jobs = []
        job_cards = soup.find_all("div", class_="individual_internship")
        
        for card in job_cards[:10]:
            title_el = card.find("h3")
            company_el = card.find("h4")
            
            if title_el and company_el:
                jobs.append({
                    "title": title_el.text.strip(),
                    "company": company_el.text.strip(),
                    "source": "Internshala",
                    "url": url
                })
        
        return jobs
    
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

def match_jobs_to_student(jobs, student):
    """Check if any jobs match this student's profile"""
    skills = student.get("skills", "").lower()
    branch = student.get("branch", "").lower()
    matching = []
    
    keywords = skills.split(",") + [branch]
    keywords = [k.strip() for k in keywords]
    
    for job in jobs:
        job_title = job["title"].lower()
        for keyword in keywords:
            if keyword and keyword in job_title:
                matching.append(job)
                break
    
    return matching

if __name__ == "__main__":
    print("Testing scraper...")
    jobs = scrape_internshala("software engineer")
    print(f"Found {len(jobs)} jobs")
    for job in jobs[:3]:
        print(f"- {job['title']} at {job['company']}")
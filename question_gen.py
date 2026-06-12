from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_questions(branch, company, cgpa, skills):
    prompt = f"""
    Tu ek expert placement coach hai Indian engineering students ke liye.
    
    Student ki profile:
    - Branch: {branch}
    - Target Company: {company}
    - CGPA: {cgpa}
    - Skills: {skills}
    
    {company} ke liye 10 interview questions generate kar jo is student se puche jayenge.
    
    Mix kuch is tarah karo:
    - 3 technical concept questions (OS, DBMS, CN ya relevant topics)
    - 3 coding/DSA questions (jo {company} actually puchti hai)
    - 2 HR questions
    - 2 aptitude questions
    
    Har question ke saath ye bhi bata:
    - {company} ye question kyun puchti hai
    - Ek achhe answer mein kya hona chahiye
    
    Hinglish mein likh — jaise ek senior apne junior ko gyaan de raha ho.
    Friendly aur honest tone rakho.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=2000
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    print("PACER - Placement Prep Agent")
    print("=" * 40)

    result = generate_questions(
        branch="Computer Science",
        company="TCS",
        cgpa="7.8",
        skills="Python, Java, SQL"
    )

    print(result)
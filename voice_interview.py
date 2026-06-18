import whisper
import os
import tempfile
from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load whisper model once — takes 30 seconds first time
print("Loading Whisper model...")
whisper_model = whisper.load_model("base")
print("Whisper ready!")

def transcribe_audio(audio_file_path):
    """Convert student's spoken answer to text"""
    result = whisper_model.transcribe(
        audio_file_path,
        language="hi"
    )
    return result["text"]

def score_answer(question, student_answer, company):
    """Ask Groq to score the answer honestly"""
    prompt = f"""
    Tu ek strict lekin supportive placement coach hai.
    
    Company: {company}
    Question: {question}
    Student ka answer: {student_answer}
    
    Is answer ko 5 cheeson pe score kar (har ek 10 mein se):
    1. Technical accuracy — kya answer sahi hai?
    2. Communication clarity — kya tu samajh sakta tha?
    3. Structure — kya answer ka beginning, middle, end tha?
    4. Confidence — kya student confident laga?
    5. Example — kya student ne example diya?
    
    Total score 50 mein se bata.
    
    Phir 3 specific cheezein bata jo galat thi aur kaise fix karein.
    Honest reh — sirf achha bolne ke liye achha mat bol.
    Hinglish mein likh — jaise ek senior junior ko feedback de raha ho.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    return response.choices[0].message.content

def text_to_speech(text, filename="output.mp3"):
    """Convert feedback text to speech"""
    tts = gTTS(text=text, lang='hi', slow=False)
    tts.save(filename)
    return filename
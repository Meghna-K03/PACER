
import shutil
import os
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from question_generator import generate_questions
from database import save_student, save_session, get_student_by_email, get_student_sessions

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    branch: str = Form(...),
    company: str = Form(...),
    cgpa: str = Form(...),
    skills: str = Form(...)
):
    # Check if student already exists
    student = get_student_by_email(email)
    
    # If new student, save them
    if not student:
        student = save_student(name, email, branch, cgpa, skills)
    
    # Generate questions
    questions = generate_questions(branch, company, cgpa, skills)
    
    # Save this session
    if student:
        save_session(student["id"], company, questions)
    
    # Get all past sessions for this student
    past_sessions = []
    if student:
        past_sessions = get_student_sessions(student["id"])
    
    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "questions": questions,
            "company": company,
            "name": name,
            "past_sessions": past_sessions,
            "session_count": len(past_sessions)
        }
    )


@app.get("/interview", response_class=HTMLResponse)
async def interview_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="interview.html"
    )

@app.post("/score-answer")
async def score_answer_route(
    request: Request,
    audio: UploadFile = File(...),
    question: str = Form(...),
    company: str = Form(...)
):
    from voice_interview import transcribe_audio, score_answer

    # Save uploaded audio temporarily
    temp_path = f"temp_audio_{audio.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    # Transcribe
    transcript = transcribe_audio(temp_path)

    # Score
    feedback = score_answer(question, transcript, company)

    # Clean up temp file
    os.remove(temp_path)

    return JSONResponse({
        "transcript": transcript,
        "feedback": feedback
    })
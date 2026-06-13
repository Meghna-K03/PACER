from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from question_generator import generate_questions

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
    branch: str = Form(...),
    company: str = Form(...),
    cgpa: str = Form(...),
    skills: str = Form(...)
):
    questions = generate_questions(branch, company, cgpa, skills)
    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "questions": questions,
            "company": company,
            "name": name
        }
    )
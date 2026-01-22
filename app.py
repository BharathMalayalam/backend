from fastapi import FastAPI, UploadFile
import PyPDF2

app = FastAPI()

@app.post("/analyze")
async def analyze_resume(file: UploadFile, job_desc: str):
    reader = PyPDF2.PdfReader(file.file)
    text = " ".join([p.extract_text() for p in reader.pages])

    resume_skills = set(text.lower().split())
    job_skills = set(job_desc.lower().split())

    matched = resume_skills & job_skills
    score = int((len(matched) / len(job_skills)) * 100) if job_skills else 0

    return {
        "match_percentage": score,
        "matched_skills": list(matched),
        "missing_skills": list(job_skills - matched)
    }

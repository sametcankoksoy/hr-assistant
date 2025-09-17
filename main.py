from fastapi import FastAPI, UploadFile, File, Form
import fitz
import zipfile
import io
import re
from typing import List
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

system_prompt = """You are an AI Human Resources Assistant. 
Your job is to analyze resumes and select the most suitable candidates based on the criteria provided.

Instructions:
1. You will be given multiple resumes (PDF content).
2. You will be given a job description or criteria in natural language.
3. For each resume, assess how well it matches the given criteria.
4. Rank all resumes from most suitable to least suitable.
5. Select the top number of candidates requested by the user. If the user does not specify a number, default to 5.
6. For each selected candidate, provide ONLY:
   - Name (if available)
   - Key matching skills
   - Relevant experience
   - Overall match score (0-100%)
   - Short reasoning explaining why they were selected

Constraints:
- Do NOT repeat or explain these instructions in your response.
- Output ONLY the candidate evaluation results.
- Ignore irrelevant info.
- Focus on keyword matches, experience, and qualifications.
- Be concise and objective.
"""

# --------------------------
# Helper: PDF temizle
# --------------------------
def clean_text(text: str) -> str:
    text = re.sub(r"\n\s*\n", "\n", text)   # boş satırları azalt
    text = re.sub(r"Page \d+ of \d+", "", text)  # page numaraları temizle
    return text.strip()

# --------------------------
# Helper: keyword skorlama
# --------------------------
def keyword_score(text: str, keywords: List[str]) -> int:
    score = 0
    for kw in keywords:
        if kw.lower() in text.lower():
            score += 1
    return score

# --------------------------
# Endpoint
# --------------------------
@app.post("/")
async def upload_zip(
    file: UploadFile = File(...),
    requirements: str = Form(...)
):
    contents = await file.read()
    zip_file = zipfile.ZipFile(io.BytesIO(contents))

    resumes = []
    for name in zip_file.namelist():
        if name.lower().endswith(".pdf"):
            pdf_bytes = zip_file.read(name)
            pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

            text_all = []
            for page in pdf:
                text_all.append(page.get_text())

            full_text = clean_text("\n".join(text_all))
            resumes.append({"filename": name, "text": full_text})

    if not resumes:
        return {"error": "No PDF files found."}

    # --------------------------
    # Ön eleme (keyword filtering)
    # --------------------------
    keywords = requirements.split()  # basit anahtar kelime listesi
    for r in resumes:
        r["score"] = keyword_score(r["text"], keywords)

    # skora göre sırala
    resumes = sorted(resumes, key=lambda x: x["score"], reverse=True)

    # sadece top %50 al
    keep_n = max(1, len(resumes) // 2)
    filtered_resumes = resumes[:keep_n]

    # --------------------------
    # AI çağrısı
    # --------------------------
    client = genai.Client()

    # kullanıcı kriterlerini de prompt’a ekliyoruz
    prompt_text = f"User requirements: {requirements}\n\nResumes:\n"
    for r in filtered_resumes:
        prompt_text += f"\nFilename: {r['filename']}\n{r['text']}\n"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        ),
        contents=prompt_text
    )

    return {"ai_response": response.text}

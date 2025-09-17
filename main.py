from fastapi import FastAPI, UploadFile, File
import fitz  
import zipfile
import io
from google import genai
from google.genai import types

app = FastAPI()

system_prompt = """You are an AI Human Resources Assistant. Your job is to analyze resumes and select the most suitable candidates based on the criteria provided.

Instructions:
1. You will be given multiple resumes (PDF content).
2. You will be given a list of desired skills, experience, qualifications, and other criteria.
3. For each resume, assess how well it matches the given criteria.
4. Rank all resumes from most suitable to least suitable.
5. Select the top number of candidates requested by the user. 
   - If the user does not specify a number, default to 5 candidates.
6. For each selected candidate, provide:
   - Name (if available)
   - Key matching skills
   - Relevant experience
   - Overall match score (0-100%)
   - Short reasoning explaining why they were selected

Constraints:
- Always adapt the number of candidates to the user’s request.
- If the user does not clearly state a number, assume 5.
- Ignore information not relevant to the role.
- Focus on keyword matches, experience, and qualifications.
- Be objective and concise in explanations."""

@app.post("/")
async def upload_zip(file: UploadFile = File(...)):
    contents = await file.read()
    zip_file = zipfile.ZipFile(io.BytesIO(contents))

    results = []

    for name in zip_file.namelist():
        if name.lower().endswith(".pdf"):
            pdf_bytes = zip_file.read(name)
            pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

            text_all = []
            for page in pdf:
                text_all.append(page.get_text())

            full_text = "\n".join(text_all).strip()

            results.append(f"Filename: {name}\n{text_all if full_text else 'Text Not Found'}")

    if not results:
        return {"error": "No PDF files found in the zip."}

    client = genai.Client()
    prompt_text = "\n\n".join(results)

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        ),
        contents=prompt_text
    )

    return {"ai_response": response.text}

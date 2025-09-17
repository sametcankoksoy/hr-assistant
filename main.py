from fastapi import FastAPI, UploadFile, File
import fitz  
import zipfile
import io
from google import genai

app = FastAPI()

@app.post("/upload-zip/")
async def upload_zip(file: UploadFile = File(...)):
    results = []

    contents = await file.read()
    zip_file = zipfile.ZipFile(io.BytesIO(contents))

    for name in zip_file.namelist():
        if name.lower().endswith(".pdf"):
            pdf_bytes = zip_file.read(name)
            pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

            text_all = []
            for page in pdf:
                text_all.append(page.get_text())

            full_text = "\n".join(text_all).strip()

            results.append({
                "filename": name,
                "text": full_text if full_text else "Text Not Found"
            })

            

    return {"pdf_texts": results}

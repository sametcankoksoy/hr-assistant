import streamlit as st
import requests

st.set_page_config(
    page_title="HR Resume Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("📄 HR Resume Assistant")

requirements = st.text_input(
    "Enter what you're looking for in candidates (e.g., Python developer with 3+ years experience, SQL, FastAPI, Agile, Cloud)"
)

uploaded_zip = st.file_uploader(
    "Upload a zip containing multiple PDF resumes", type=["zip"]
)

if st.button("Analyze Resumes"):
    if not uploaded_zip or not requirements.strip():
        st.warning("Please enter requirements and upload a zip file.")
    else:
        st.info("Processing resumes... This may take a few seconds.")

        files = {"file": (uploaded_zip.name, uploaded_zip, "application/zip")}
        data = {"requirements": requirements}  # single text input sent to backend

        try:
            backend_url = "http://localhost:8000/"
            response = requests.post(backend_url, files=files, data=data)

            if response.status_code == 200:
                ai_response = response.json().get("ai_response", "")
                st.success("✅ Analysis complete! Top 5 candidates:")
                st.text(ai_response)
            else:
                st.error(f"Backend returned an error: {response.status_code}")
        except Exception as e:
            st.error(f"Error contacting backend: {e}")

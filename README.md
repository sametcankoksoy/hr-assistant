# 📋 AI-Powered HR Resume Assistant

This project is an AI-powered HR assistant designed to accelerate the recruitment process. The application batch-analyzes multiple resumes (in PDF format), compares them against specific job requirements, and presents a ranked list of the most suitable candidates.

## 🚀 Key Features

* **Bulk Resume Upload:** Upload a single `.zip` file containing multiple candidate resumes.
* **Natural Language Requirements:** Specify the desired candidate traits in plain language (e.g., "Python developer with 5+ years of experience, SQL, and cloud knowledge").
* **Two-Stage Filtering:**
    * **Pre-screening:** The FastAPI backend performs a quick pre-screening based on keyword matching to select the most relevant resumes.
    * **In-depth Analysis:** The pre-screened resumes are then sent to the Google Gemini AI model for a detailed analysis and ranking.
* **Intelligent Candidate Ranking:** Gemini AI evaluates each candidate's skills, experience, and overall fit, ranking the top candidates and providing a brief rationale for their selection.
* **Interactive Interface:** Offers a simple and user-friendly web interface built with Streamlit.

## ⚙️ Architecture and How It Works

The application consists of a Streamlit frontend and a FastAPI backend.

1.  **Data Input:** The HR specialist enters the search criteria and uploads a `.zip` file containing candidate resumes using the Streamlit interface.
2.  **API Request:** Upon clicking the "Analyze Resumes" button, the Streamlit frontend sends the file and criteria as a `POST` request to the `/` endpoint on the FastAPI backend.
3.  **Backend Processing (`main.py`):**
    * The backend opens the uploaded `.zip` file in memory and extracts all contained PDF files.
    * It reads and cleans the text content of each PDF using the `PyMuPDF (fitz)` library.
    * It performs a simple **pre-screening** by splitting the user's requirements into keywords and scoring each resume against them.
    * It selects the top-scoring resumes (the top 50%) for the next stage.
4.  **AI Invocation:**
    * The text from the filtered resumes, along with the user's job description, is sent to the Google Gemini API with a system prompt.
    * This prompt instructs the AI to act as an HR assistant, rank the candidates, and provide a short justification for each selection.
5.  **Displaying Results:** The response from Gemini is sent back from FastAPI to the Streamlit interface, and the list of top candidates is displayed to the user.

## 🛠️ Technology Stack

* **Backend:**
    * Python 3.11+
    * FastAPI: For the API server.
    * Uvicorn: ASGI server.
    * Google Generative AI (`google-generativeai`): For Gemini API integration.
    * PyMuPDF (`fitz`): For reading PDF files.
    * Python-dotenv: For managing environment variables.
* **Frontend:**
    * Streamlit: For building fast, interactive web apps.
    * Requests: For communicating with the backend.

## 📦 Installation and Setup

### Prerequisites

* Python 3.10+
* An API Key from Google AI Studio

### 1. Clone and Install

```bash
git clone https://github.com/sametcankoksoy/hr-assistant
cd hr-assistant

# Install the required Python packages
pip install -r requirements.txt
```

*(Note: If a `requirements.txt` file is not available, install packages with: `pip install fastapi uvicorn streamlit requests google-generativeai pymupdf python-dotenv`)*

### 2\. Set Up Environment Variables

1.  Create a file named `.env` in the project's root directory.The `.gitignore` file is already configured to ignore this file[cite: 2].
2.  Add your Google AI Studio API key to this file:
    ```   
    # .env file
    GEMINI_API_KEY="PASTE_YOUR_API_KEY_HERE"
    ```

### 3\. Run the Application

You will need two separate terminal windows to run the application.

1.  **Terminal 1: Start the Backend Server**

    ```bash
    uvicorn main:app --reload
    ```

    The server will start at `http://localhost:8000`.

2.  **Terminal 2: Start the Frontend App**

    ```bash
    streamlit run app.py
    ```

    The Streamlit interface will automatically open in your browser (usually at `http://localhost:8501`).

    You are now ready to use the application\!

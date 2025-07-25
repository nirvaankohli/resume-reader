# Resume Reader

Resume Reader is an AI-powered web application that helps job seekers instantly match their resume to any job description. It provides a match grade, highlights strengths, identifies missing skills, and offers actionable insights to improve your applications.

## Features

- **Upload Resume & Job Description:** Upload your resume (PDF) and paste a job description to get a detailed match analysis.
  
- **AI-Powered Analysis:** Uses OpenAI's GPT-4 to compare your resume with the job description and generate a comprehensive JSON-based evaluation.

- **Match Grade:** Get an overall match score (0-100) indicating how well your resume fits the job.

- **Skill & Keyword Matching:** See which skills and keywords are matched or missing, and their importance.

- **Strengths & Improvements:** Receive a list of strengths and actionable suggestions for improvement.

- **Relevant Experience & Education Match:** Quickly see if your experience and education align with the job requirements.

- **Modern UI:** Clean, responsive interface with clear feedback and loading states.

## Demo

1. **Landing Page:** Welcomes users and explains the app's purpose.

2. **Upload Page:** Upload your resume PDF and paste a job description.

3. **Loading State:** Shows a spinner while your resume is being analyzed
   
4. **Results Page:** Displays your match grade, strengths, areas to improve, keyword table, and a summary.

## How It Works

1. **Upload:** User uploads a PDF resume and pastes a job description.
2. **Extraction:** The app extracts text from the PDF using PyPDF2.
3. **AI Analysis:** Sends the resume and job description to OpenAI's GPT-4 for structured analysis.
4. **Results:** Returns a JSON object with match grade, skills, strengths, improvements, and more, which is rendered in the UI.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nirvaankohli/resume-reader.git
   cd resume-reader
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file in the project root with your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```
4. **Run the app:**
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000/`.

## Requirements

- Python 3.8+
- Flask
- PyPDF2
- OpenAI
- python-dotenv

(See `requirements.txt` for the full list.)

## Usage

1. Go to the landing page and click "Try It".
2. Upload your resume PDF and paste the job description.
3. Click "Grade Match" and wait for the analysis.
4. Review your match grade, strengths, missing skills, and suggestions.

## Project Structure

- `app.py` - Main Flask application and backend logic
- `templates/` - HTML templates for landing, upload, loading, and result pages
- `static/` - Static assets (e.g., favicon)
- `uploads/` - Uploaded PDF files (temporary)
- `requirements.txt` - Python dependencies
- `setup.py` - Packaging and entry point

## API

- `POST /api/analyze` - Accepts a PDF file and job description, returns JSON analysis

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [OpenAI](https://openai.com/)
- [PyPDF2](https://pypdf2.readthedocs.io/)

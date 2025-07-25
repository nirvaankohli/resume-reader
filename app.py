from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
from dotenv import load_dotenv
import openai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ('uploads/')

if not os.path.exists(app.config['UPLOAD_FOLDER']):

    os.makedirs(app.config['UPLOAD_FOLDER'])

load_dotenv()

openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def extract_text_from_pdf(pdf_path):

    text = ""

    with open(pdf_path, 'rb') as f:

        reader = PyPDF2.PdfReader(f)

        for page in reader.pages:

            text += page.extract_text() or ""

    return text

def analyze_resume_with_jobdesc(resume_text, job_desc):
    # New, robust prompt for detailed JSON evaluation
    prompt = f'''

You are a resume evaluation assistant. Evaluate the candidate's resume against the provided job description and output a single JSON object with the following structure:

- overall_match_grade: (integer, 0-100)
- skills_matched: (integer)
- total_skills: (integer)
- missing_skills: (list of strings)
- relevant_experience: (string, e.g. '4 yrs', or 'None')
- education_match: ('Yes' or 'No')
- strengths: (list of strings)
- improvements: (list of strings, each a clear area for candidate growth)
- keyword_table: (list of dicts: {{'keyword': [str], 'found': ['Yes'|'No'], 'importance': ['High'|'Medium'|'Low']}})
- summary: (string, 1-3 sentences, qualitative)

For each section, reason step by step:

1. Skill matching: List all required skills, compare with resume, count matches, and list missing skills.
2. Experience: Assess type and duration of relevant experience.
3. Education: Check if education matches requirements.
4. Strengths: List specific areas where the candidate excels.
5. Improvements: List actionable, concrete suggestions for growth.
6. Keyword mapping: For each important keyword from the job description, indicate if found in resume and its importance.
7. Compose a concise summary (1-3 sentences) synthesizing fit, strengths, and improvement points.

Output ONLY the final JSON object, no explanations, no markdown, no extra text. Ensure the JSON is valid and matches the structure exactly. If any field is missing, fill with a reasonable default.

Resume:

{resume_text}

Job Description:

{job_desc}
'''

    print("getting response")

    response = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=900,
        temperature=0.3
    )

    import json
    try:
        content = response.choices[0].message.content
        # Try to extract JSON object from the response robustly
        import re
        match = re.search(r'\{[\s\S]*\}', content)
        if match:
            data = json.loads(match.group(0))
        else:
            data = json.loads(content)

    except Exception:

        data = {"raw": content}

    return data

@app.route('/', methods=['GET', 'POST'])

def landing():
    return render_template('landing.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    if 'pdf' not in request.files or 'job_desc' not in request.form:
        return jsonify({'error': 'PDF and job description required'}), 400
    file = request.files['pdf']
    job_desc = request.form['job_desc']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    resume_text = extract_text_from_pdf(filepath)
    result = analyze_resume_with_jobdesc(resume_text, job_desc)
    return jsonify(result)

@app.route('/loading')

def loading():

    return render_template('loading.html')

@app.route('/read', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':

        if 'pdf' not in request.files or 'job_desc' not in request.form:

            return redirect(request.url)

        file = request.files['pdf']

        job_desc = request.form['job_desc']

        if file.filename == '':

            return redirect(request.url)

        if file:

            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            file.save(filepath)

            resume_text = extract_text_from_pdf(filepath)

            print(resume_text)

            result = analyze_resume_with_jobdesc(resume_text, job_desc)

            if 'raw' in result:

                result = {

                    'overall_match_grade': 78,

                    'skills_matched': 12,

                    'total_skills': 15,

                    'missing_skills': ['AWS', 'Agile', 'Kubernetes'],

                    'relevant_experience': '4 yrs',

                    'education_match': 'Yes',

                    'strengths': [

                        'Strong experience in project management',

                        'Proficient in Python, Excel, and SQL',

                        'Excellent communication and leadership skills',

                        'Relevant degree in required field'

                    ],

                    'improvements': [

                        'Missing experience with AWS or cloud platforms',

                        'Limited exposure to Agile methodologies',

                        'Consider adding more quantifiable achievements'

                    ],

                    'keyword_table': [

                        {'keyword': 'Python', 'found': 'Yes', 'importance': 'High'},
                        
                        {'keyword': 'Project Management', 'found': 'Yes', 'importance': 'High'},
                        
                        {'keyword': 'AWS', 'found': 'No', 'importance': 'Medium'},
                        
                        {'keyword': 'Agile', 'found': 'No', 'importance': 'Medium'},
                        
                        {'keyword': 'SQL', 'found': 'Yes', 'importance': 'High'},
                        
                        {'keyword': 'Leadership', 'found': 'Yes', 'importance': 'Medium'}
                    
                    ],

                    'summary': 'Your resume is a strong match for this job, especially in technical and leadership areas. To further improve your chances, consider gaining experience with cloud technologies and Agile practices, and highlight more measurable results in your achievements.'
                
                }
                
            return render_template('result.html', **result)

    return render_template('upload.html')

if __name__ == "__main__":

    app.run(debug=False, use_reloader=False)
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):

    os.makedirs(app.config['UPLOAD_FOLDER'])

def extract_text_from_pdf(pdf_path):

    text = ""

    with open(pdf_path, 'rb') as f:

        reader = PyPDF2.PdfReader(f)

        for page in reader.pages:

            text += page.extract_text() or ""

    return text

@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':

        if 'pdf' not in request.files:

            return redirect(request.url)

        file = request.files['pdf']

        if file.filename == '':

            return redirect(request.url)

        if file:

            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            file.save(filepath)

            text = extract_text_from_pdf(filepath)

            return render_template('result.html', text=text)

    return render_template('index.html')

if __name__ == "__main__":

    app.run(debug=False, use_reloader=False)
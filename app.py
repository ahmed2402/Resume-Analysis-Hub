    # app.py
from flask import Flask, render_template, request
import joblib
import PyPDF2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load models
rf = joblib.load("rf_model.pkl")
tf_idf = joblib.load("tfidf_vectorizer.pkl")
le = joblib.load("label_encoder.pkl")

def preprocess_text(text):
    return text  # Add your preprocessing logic here

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    resume_text = ""

    if 'resume_text' in request.form and request.form['resume_text'].strip():
        resume_text = request.form['resume_text']
    elif 'resume_file' in request.files:
        file = request.files['resume_file']
        if file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            resume_text = extract_text_from_pdf(file_path)
            os.remove(file_path)

    resume_text = preprocess_text(resume_text)
    vectorized = tf_idf.transform([resume_text])
    prediction = rf.predict(vectorized)
    predicted_category = le.inverse_transform([prediction[0]])[0]

    return render_template('result.html', category=predicted_category, text=resume_text)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)

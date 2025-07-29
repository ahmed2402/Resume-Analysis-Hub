import re
from flask import Flask, render_template, request, jsonify, send_file
import joblib
import PyPDF2
import os
from werkzeug.utils import secure_filename
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import numpy as np

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load models
rf = joblib.load("models/rf.pkl")
tf_idf = joblib.load("models/tf_idf.pkl")
le = joblib.load("models/le.pkl")




def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    text = re.sub('http\\S+\\s*', ' ', text)
    text = re.sub('RT|cc', ' ', text)
    text = re.sub('#\\S+', '', text)
    text = re.sub('@\\S+', ' ', text)
    text = re.sub('[^a-zA-Z0-9]+', ' ', text)
    text = re.sub(' +', ' ', text)
    
    tokens = word_tokenize(text)
    
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text


def validate_input(text):
    if len(text) < 100:
        return False, "Resume is too short. Please provide a more detailed resume."
    
    if re.search(r'(.)\1{4,}', text):
        return False, "Please provide meaningful Resume instead of repetitive characters."
    
    random_patterns = [
        r'[a-z]{15,}',  # Very long sequences of random letters (increased threshold)
        r'[0-9]{8,}',   # Long sequences of numbers
        r'[!@#$%^&*()]{5,}',  # Long sequences of special characters
    ]
    
    for pattern in random_patterns:
        if re.search(pattern, text.lower()):
            return False, "Please provide meaningful Resume instead of random characters."
    
    return True, ""  # Return True if all validations pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    resume_text = ""

    if 'resume_text' in request.form and request.form['resume_text'].strip():
        resume_text = request.form['resume_text']
        is_valid, error_message = validate_input(resume_text)
        if not is_valid:
            return render_template('index.html', error=error_message) 
    elif 'resume_file' in request.files:
        file = request.files['resume_file']
        if file and file.filename:
            if file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                resume_text = extract_text_from_pdf(file_path)
                os.remove(file_path)
            else:
                return render_template('index.html', error="Please upload a PDF file.")
        else:
            return render_template('index.html', error="Please provide resume text or upload a PDF file.")
    
    # Check if we have valid resume text after processing
    if not resume_text or len(resume_text.strip()) < 100:
        return render_template('index.html', error="Please provide a valid resume with sufficient content.")

    resume_text = preprocess_text(resume_text)
    vectorized = tf_idf.transform([resume_text])
    
    prediction_proba = rf.predict_proba(vectorized)[0]
    
    # Get top 3 predictions with their probabilities
    top_3_indices = np.argsort(prediction_proba)[-3:][::-1]
    top_3_predictions = []
    
    for idx in top_3_indices:
        category = le.inverse_transform([idx])[0]
        confidence = prediction_proba[idx] * 100
        top_3_predictions.append({
            'category': category,
            'confidence': round(confidence, 2)
        })

    return render_template('result.html', 
                         predictions=top_3_predictions, 
                         text=resume_text)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)

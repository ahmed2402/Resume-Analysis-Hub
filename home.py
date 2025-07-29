from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file
import joblib
import PyPDF2
import os
from werkzeug.utils import secure_filename
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

rf = joblib.load("models/rf.pkl")
tf_idf = joblib.load("models/tf_idf.pkl")
le = joblib.load("models/le.pkl")

# For JD analysis, we'll create a fresh TF-IDF vectorizer each time
# since we only have 2 documents (resume and JD)

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

def calculate_similarity(resume_text, jd_text):
    # Preprocess both texts
    resume_processed = preprocess_text(resume_text)
    jd_processed = preprocess_text(jd_text)
    
    # Check if processed texts are empty or too short
    if len(resume_processed.strip()) < 10 or len(jd_processed.strip()) < 10:
        return 0.0
    
    # Create a fresh TF-IDF vectorizer for this comparison
    jd_tfidf = TfidfVectorizer(max_features=5000, stop_words='english', min_df=1, max_df=1.0)
    
    try:
        # Create TF-IDF vectors
        texts = [resume_processed, jd_processed]
        vectors = jd_tfidf.fit_transform(texts)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return round(similarity * 100, 2)
    except ValueError as e:
        # Handle empty vocabulary error
        if "empty vocabulary" in str(e):
            return 0.0
        else:
            raise e




# Home page route
@app.route('/')
def home():
    return render_template('home/home.html')

# Resume category prediction routes
@app.route('/resume-category')
def resume_category():
    return render_template('resume_classifier/index.html')

@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    resume_text = ""

    if 'resume_text' in request.form and request.form['resume_text'].strip():
        resume_text = request.form['resume_text']
        is_valid, error_message = validate_input(resume_text)
        if not is_valid:
            return render_template('resume_classifier/index.html', error=error_message) 
    elif 'resume_file' in request.files:
        file = request.files['resume_file']
        if file and file.filename:
            if file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                resume_text = extract_text_from_pdf(file_path)
                os.remove(file_path)  # Clean up
            else:
                return render_template('resume_classifier/index.html', error="Please upload a PDF file")
        else:
            return render_template('resume_classifier/index.html', error="Please provide resume text or upload a file")
    else:
        return render_template('resume_classifier/index.html', error="Please provide resume text or upload a file")

    if not resume_text:
        return render_template('resume_classifier/index.html', error="Please provide resume text or upload a file")

    processed_text = preprocess_text(resume_text)
    vectorized = tf_idf.transform([processed_text])
    
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

    
    return render_template('resume_classifier/result.html', 
                         predictions=top_3_predictions,
                         text=processed_text)

# JD score calculation routes
@app.route('/jd-score')
def jd_score():
    return render_template('job_desc/jd_analysis.html')

@app.route('/analyze-jd', methods=['POST'])
def analyze_jd():
    resume_text = ""
    jd_text = ""
    
        # Get resume text
    if 'resume_text' in request.form and request.form['resume_text'].strip():
        resume_text = request.form['resume_text']
        # is_valid, error_message = validate_input(resume_text)
        # if not is_valid:
        #     return render_template('job_desc/jd_analysis.html', error=error_message)     
    elif 'resume_file' in request.files:
        file = request.files['resume_file']
        if file and file.filename:
            if file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                resume_text = extract_text_from_pdf(file_path)
                os.remove(file_path)  # Clean up
            else:
                return render_template('job_desc/jd_analysis.html', error="Please upload a PDF file for resume")
    
    # Get job description text
    if 'jd_text' in request.form and request.form['jd_text'].strip():
        jd_text = request.form['jd_text']
        # is_valid, error_message = validate_input(jd_text)
        # if not is_valid:
        #     return render_template('job_desc/jd_analysis.html', error=error_message)     
    elif 'jd_file' in request.files:
        file = request.files['jd_file']
        if file and file.filename:
            if file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                jd_text = extract_text_from_pdf(file_path)
                os.remove(file_path)  # Clean up
            else:
                return render_template('job_desc/jd_analysis.html', error="Please upload a PDF file for job description")
    
    # Check both inputs after processing
    # if not resume_text:
    #     return render_template('job_desc/jd_analysis.html', error="Please provide resume text or upload a resume file")
        
    # if not jd_text:
    #     return render_template('job_desc/jd_analysis.html', error="Please provide job description text or upload a job description file")
    
    # Calculate similarity score
    score = calculate_similarity(resume_text, jd_text)
    
    # Determine match level
    if score >= 80:
        match_level = "Excellent Match"
        match_color = "#28a745"
    elif score >= 60:
        match_level = "Good Match"
        match_color = "#17a2b8"
    elif score >= 40:
        match_level = "Fair Match"
        match_color = "#ffc107"
    else:
        match_level = "Poor Match"
        match_color = "#dc3545"
    
    return render_template('job_desc/jd_analysis.html', 
                         score=round(score, 2), 
                         match_level=match_level, 
                         match_color=match_color)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Flask, render_template, request
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
import google.generativeai as genai
import json
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'



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
    
    result = ' '.join(tokens)
    return result

def extract_text_from_pdf(file_path):
    try:
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        if not text:
            return "[No text extracted. PDF may be scanned or encrypted.]"
        return text.strip()
    except Exception as e:
        return f"[Error extracting text: {str(e)}]"


def validate_input(text):
    if len(text) < 100:
        return False, "Resume is too short. Please provide a more detailed resume."
    
    if re.search(r'(.)\1{4,}', text):
        return False, "Please provide meaningful Resume instead of repetitive characters."
    
    random_patterns = [
        r'[a-z]{15,}',
        r'[0-9]{8,}',
        r'[!@#$%^&*()]{5,}',
    ]
    
    for pattern in random_patterns:
        if re.search(pattern, text.lower()):
            return False, "Please provide meaningful Resume instead of random characters."
    
    return True, "" 

def calculate_similarity(resume_text, jd_text):
    resume_processed = preprocess_text(resume_text)
    jd_processed = preprocess_text(jd_text)
    
    if len(resume_processed.strip()) < 10 or len(jd_processed.strip()) < 10:
        return 0.0
    
    jd_tfidf = TfidfVectorizer(max_features=5000, stop_words='english', min_df=1, max_df=1.0)
    
    try:
        texts = [resume_processed, jd_processed]
        vectors = jd_tfidf.fit_transform(texts)
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return round(similarity * 100, 2)
    except ValueError as e:
        if "empty vocabulary" in str(e):
            return 0.0
        else:
            raise e

def generate_match_analysis(resume_text, jd_text, score):
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Analyze the match between a resume and job description with a similarity score of {score}%.

        Resume Text:
        {resume_text[:2000]}...

        Job Description:
        {jd_text[:2000]}...

        Return the analysis in this exact format (no extra dashes or blank lines):

        [Section] Key Insights
        - Insight 1
        - Insight 2

        [Section] Strengths
        - Strength 1
        - Strength 2

        [Section] Areas for Improvement
        - Area 1
        - Area 2

        [Section] Missing Skills
        - Skill 1
        - Skill 2

        [Section] Recommendations
        - Recommendation 1
        - Recommendation 2

        [Section] Overall Assessment
        - Assessment 1
        - Assessment 2

        """
        response = model.generate_content(prompt)
        
        return response.text


@app.route('/')
def home():
    return render_template('home/home.html')

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
                os.remove(file_path)  
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

@app.route('/jd-score')
def jd_score():
    return render_template('job_desc/jd_analysis.html')

@app.route('/analyze-jd', methods=['POST'])
def analyze_jd():
    jd_resume_text = ""
    jd_text = ""
    
    # Handle resume input (text or file)
    if 'jd_resume_text' in request.form and request.form['jd_resume_text'].strip():
        jd_resume_text = request.form['jd_resume_text'].strip()
    elif 'jd_resume_file' in request.files:
        file = request.files['jd_resume_file']
        if file and file.filename:
            if file.filename.endswith('.pdf'):
                try:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    jd_resume_text = extract_text_from_pdf(file_path)
                    os.remove(file_path)
                except Exception as e:
                    return render_template('job_desc/jd_analysis.html', error=f"Error processing resume file: {str(e)}")
            else:
                return render_template('job_desc/jd_analysis.html', error="Please upload a PDF file for resume")
        else:
            return render_template('job_desc/jd_analysis.html', error="Please provide resume text or upload a file")
    else:
        return render_template('job_desc/jd_analysis.html', error="Please provide resume text or upload a file")
    
    # Handle job description input (text or file)
    if 'jd_text' in request.form and request.form['jd_text'].strip():
        jd_text = request.form['jd_text'].strip()
    elif 'jd_file' in request.files:
        file = request.files['jd_file']
        if file and file.filename:
            if file.filename.endswith('.pdf'):
                try:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    jd_text = extract_text_from_pdf(file_path)
                    os.remove(file_path)
                except Exception as e:
                    return render_template('job_desc/jd_analysis.html', error=f"Error processing job description file: {str(e)}")
            else:
                return render_template('job_desc/jd_analysis.html', error="Please upload a PDF file for job description")
        else:
            return render_template('job_desc/jd_analysis.html', error="Please provide job description text or upload a file")
    else:
        return render_template('job_desc/jd_analysis.html', error="Please provide job description text or upload a file")
    
    # Validate that we have both inputs
    if not jd_resume_text or not jd_text:
        return render_template('job_desc/jd_analysis.html', error="Both resume and job description are required")
    
    # Check if extracted text is meaningful
    if jd_resume_text.startswith("[No text extracted") or jd_resume_text.startswith("[Error extracting"):
        return render_template('job_desc/jd_analysis.html', error="Could not extract text from resume PDF. Please try a different file or paste text directly.")
    
    if jd_text.startswith("[No text extracted") or jd_text.startswith("[Error extracting"):
        return render_template('job_desc/jd_analysis.html', error="Could not extract text from job description PDF. Please try a different file or paste text directly.")
    
    score = calculate_similarity(jd_resume_text, jd_text)
    
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
    
    analysis = generate_match_analysis(jd_resume_text, jd_text, score)

    return render_template('job_desc/jd_result.html', 
                         score=round(score, 2), 
                         match_level=match_level, 
                         match_color=match_color,
                         analysis=analysis)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

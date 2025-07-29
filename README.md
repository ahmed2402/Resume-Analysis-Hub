# Resume Category Classifier

A sophisticated AI-powered web application that automatically categorizes resumes into different job categories using machine learning. The application provides an intuitive interface for uploading PDF resumes or pasting resume text, then uses a trained Random Forest model to predict the most suitable job categories with confidence scores.

## 🚀 Features

- **PDF Resume Upload**: Drag-and-drop interface for uploading PDF resumes
- **Text Input**: Direct text input option for resume content
- **AI-Powered Classification**: Uses trained machine learning models for accurate categorization
- **Multi-Category Prediction**: Shows top 3 predicted job categories with confidence scores
- **Real-time Processing**: Instant analysis with beautiful loading animations
- **Responsive Design**: Modern, professional UI that works on all devices
- **Input Validation**: Comprehensive validation to ensure quality input
- **Text Preprocessing**: Advanced NLP preprocessing for better accuracy

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Machine Learning**: Scikit-learn, NLTK
- **PDF Processing**: PyPDF2
- **Data Processing**: Pandas, NumPy
- **Model Persistence**: Joblib
- **Styling**: Custom CSS with animations and responsive design

## 📁 Project Structure

```
Resume-Classifier/
├── app.py                          # Main Flask application
├── synthetic.py                    # Synthetic data generation script
├── eda.ipynb                      # Exploratory Data Analysis notebook
├── README.md                      # Project documentation
├── .gitignore                     # Git ignore file
├── static/
│   └── style.css                  # Custom CSS styles
├── templates/
│   ├── index.html                 # Main upload interface
│   └── result.html                # Results display page
├── models/                        # Trained ML models (gitignored)
│   ├── rf.pkl                     # Random Forest model
│   ├── tf_idf.pkl                 # TF-IDF vectorizer
│   ├── le.pkl                     # Label encoder
│   └── catboost_model.pkl         # CatBoost model (alternative)
├── datasets/                      # Training datasets (gitignored)
│   ├── UpdatedResumeDataSet.csv   # Main dataset
│   ├── cleaned_resume.csv         # Cleaned dataset
│   ├── synthetic_resume_dataset.csv
│   └── synthetic_resume_dataset2.csv
└── catboost_info/                 # CatBoost training logs (gitignored)
```

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Resume-Classifier
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install required dependencies**
   ```bash
   pip install flask
   pip install scikit-learn
   pip install nltk
   pip install PyPDF2
   pip install pandas
   pip install numpy
   pip install joblib
   pip install google-generativeai
   pip install python-dotenv
   ```

4. **Download NLTK data**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   nltk.download('punkt_tab')
   ```

5. **Set up models and datasets**
   - Place your trained models in the `models/` directory
   - Ensure you have the required dataset files in `datasets/` directory
   - Models should include: `rf.pkl`, `tf_idf.pkl`, and `le.pkl`

## 🎯 Usage

### Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`

### Using the Application

1. **Upload a PDF Resume**
   - Drag and drop a PDF file onto the upload area
   - Or click "Choose File" to select a PDF from your computer

2. **Or Paste Resume Text**
   - Type or paste your resume text directly into the text area

3. **Analyze**
   - Click "Analyze Resume" to process your input
   - Wait for the AI to categorize your resume

4. **View Results**
   - See the top 3 predicted job categories
   - View confidence scores for each prediction
   - Optionally view the processed text

## 📊 Machine Learning Pipeline

### Data Preprocessing
1. **Text Cleaning**: Remove URLs, special characters, and normalize text
2. **Tokenization**: Split text into individual words
3. **Stop Word Removal**: Remove common English stop words
4. **Lemmatization**: Convert words to their base form

### Feature Extraction
- **TF-IDF Vectorization**: Convert text to numerical features
- **Dimensionality**: Optimized feature space for classification

### Model Training
- **Algorithm**: Random Forest Classifier
- **Cross-validation**: Ensures model robustness
- **Hyperparameter Tuning**: Optimized for accuracy

## 🎨 UI/UX Features

### Design Highlights
- **Modern Gradient Background**: Animated blue gradient with floating particles
- **Glass Morphism**: Translucent cards with backdrop blur effects
- **Smooth Animations**: CSS transitions and keyframe animations
- **Interactive Elements**: Hover effects, ripple animations, and micro-interactions
- **Responsive Layout**: Mobile-first design approach

### User Experience
- **Drag & Drop**: Intuitive file upload interface
- **Real-time Validation**: Immediate feedback on input quality
- **Loading States**: Beautiful spinner animations during processing
- **Error Handling**: Clear error messages with helpful guidance
- **Accessibility**: Keyboard navigation and screen reader support

## 📈 Performance

### Model Performance
- **Accuracy**: High classification accuracy across multiple job categories
- **Speed**: Fast inference times for real-time processing
- **Scalability**: Handles various resume formats and lengths

### Application Performance
- **Response Time**: Sub-second processing for most resumes
- **Memory Usage**: Optimized for efficient resource utilization
- **Concurrent Users**: Supports multiple simultaneous users

## 🔍 Data Sources

### Training Data
- **Primary Dataset**: UpdatedResumeDataSet.csv with diverse job categories
- **Synthetic Data**: AI-generated resumes for data augmentation
- **Data Cleaning**: Removed duplicates and standardized formats

### Categories Supported
The model can classify resumes into various job categories including:
- Web Developer
- Software Engineer
- Data Scientist
- Business Analyst
- And many more...

## 🛡️ Security & Privacy

### Data Protection
- **Local Processing**: All analysis happens on the server
- **Temporary Storage**: Uploaded files are deleted after processing
- **No Data Retention**: User data is not stored permanently
- **Input Validation**: Comprehensive validation prevents malicious input

### File Handling
- **PDF Validation**: Only accepts valid PDF files
- **Size Limits**: Reasonable file size restrictions
- **Content Validation**: Checks for meaningful content

## 🧪 Testing

### Input Validation Tests
- Resume length validation
- Content quality checks
- File format verification
- Special character handling

### Model Performance Tests
- Accuracy metrics
- Processing speed tests
- Memory usage optimization
- Cross-validation results


## 👥 Authors

- **Ahmed Raza**  - [Github](https://github.com/ahmed2402), [Linkedln](https://www.linkedin.com/in/ahmvd/)



## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact: ahmedraza312682@gmail.com

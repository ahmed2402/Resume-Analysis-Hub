# Resume Analysis Hub

A comprehensive AI-powered web application that provides two main functionalities: **Resume Category Classification** and **Job Description Matching Analysis**. Built with Flask and powered by machine learning models, this application helps users understand their professional profile and assess job compatibility with AI-driven insights.

## 🚀 Features

### Resume Category Predictor
- **PDF Resume Upload**: Drag-and-drop interface for uploading PDF resumes
- **Text Input**: Direct text input option for resume content
- **AI-Powered Classification**: Uses trained Random Forest model for accurate categorization
- **Multi-Category Prediction**: Shows top 3 predicted job categories with confidence scores
- **Real-time Processing**: Instant analysis with beautiful loading animations

### Job Description Score Analysis
- **Dual Input Support**: Upload or paste both resume and job description
- **Similarity Scoring**: Calculate compatibility scores using TF-IDF and cosine similarity
- **AI-Powered Insights**: Gemini API integration for personalized analysis and recommendations
- **Comprehensive Analysis**: Get detailed insights including strengths, areas for improvement, and recommendations
- **Match Level Assessment**: Visual indicators for Excellent, Good, Fair, or Poor matches

### General Features
- **Responsive Design**: Modern, professional UI that works on all devices
- **Input Validation**: Comprehensive validation to ensure quality input
- **Text Preprocessing**: Advanced NLP preprocessing for better accuracy
- **Security**: Local processing with temporary file storage
- **Error Handling**: Clear error messages with helpful guidance

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Machine Learning**: Scikit-learn, NLTK
- **PDF Processing**: PyPDF2
- **Data Processing**: Pandas, NumPy
- **Model Persistence**: Joblib
- **AI Analysis**: Google Gemini API
- **Styling**: Custom CSS with animations and responsive design

## 📁 Project Structure

```
Resume-Classifier/
├── home.py                         # Main Flask application
├── Procfile                       # Railway deployment configuration
├── requirements.txt               # Python dependencies
├── runtime.txt                   # Python version specification
├── README.md                     # Project documentation
├── RAILWAY_DEPLOYMENT_GUIDE.md   # Railway deployment guide
├── uploads/                      # Temporary file upload directory
├── static/
│   ├── shared.css                # Shared CSS styles
│   ├── home/
│   │   └── home.css             # Home page styles
│   ├── resume_classifier/
│   │   └── resume.css           # Resume classifier styles
│   ├── job_desc/
│   │   ├── jd_analysis.css      # Job description analysis styles
│   │   └── jd_result.css        # Job description result styles
│   └── js/
│       ├── home.js              # Home page JavaScript
│       ├── resume_classifier.js # Resume classifier JavaScript
│       ├── resume_result.js     # Resume result JavaScript
│       ├── jd_analysis.js       # Job description analysis JavaScript
│       └── jd_result.js         # Job description result JavaScript
├── templates/
│   ├── home/
│   │   └── home.html            # Main landing page
│   ├── resume_classifier/
│   │   ├── index.html           # Resume upload interface
│   │   └── result.html          # Classification results
│   └── job_desc/
│       ├── jd_analysis.html     # Job description analysis interface
│       └── jd_result.html       # Analysis results
├── models/                       # Trained ML models
│   ├── rf.pkl                   # Random Forest model
│   ├── tf_idf.pkl               # TF-IDF vectorizer
│   ├── le.pkl                   # Label encoder
│   └── catboost_model.pkl       # CatBoost model (alternative)
├── datasets/                     # Training datasets
│   ├── UpdatedResumeDataSet.csv # Main dataset
│   ├── cleaned_resume.csv       # Cleaned dataset
│   ├── synthetic_resume_dataset.csv
│   └── synthetic_resume_dataset2.csv
└── model_training/               # Model training scripts
    ├── eda.ipynb                # Exploratory Data Analysis notebook
    └── synthetic.py             # Synthetic data generation script
```

## 🚀 Installation & Deployment

### Option 1: Local Development

#### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Google Gemini API key (for enhanced job description analysis)

#### Setup Instructions

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
   pip install -r requirements.txt
   ```

4. **Download NLTK data**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   ```

5. **Set up Gemini API (Required for Job Description Analysis)**
   
   a. Get a Gemini API key:
      - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
      - Create a new API key
   
   b. Create a `.env` file in the project root:
      ```
      GEMINI_API_KEY=your_api_key_here
      ```

6. **Run the application**
   ```bash
   python home.py
   ```

### Option 2: Railway Deployment (Recommended)

#### Prerequisites
- Railway account (free tier available)
- GitHub account
- Google Gemini API key

#### Deployment Steps

1. **Push your code to GitHub**
   - Create a new repository on GitHub
   - Push your project files to the repository

2. **Deploy on Railway**
   - Visit [railway.app](https://railway.app)
   - Sign in with your GitHub account
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Configure Environment Variables**
   - In Railway dashboard, go to **Variables** tab
   - Add: `GEMINI_API_KEY` = your Gemini API key

4. **Access your app**
   - Railway will provide a URL like: `https://your-app-name.railway.app`
   - Your app will be automatically deployed and updated

For detailed Railway deployment instructions, see [RAILWAY_DEPLOYMENT_GUIDE.md](RAILWAY_DEPLOYMENT_GUIDE.md)

## 🎯 Usage

### Accessing the Application

- **Railway Deployment**: Visit your Railway app URL (e.g., `https://your-app-name.railway.app`)
- **Local Development**: Run `python home.py` and visit `http://localhost:5000`

### Using the Application

#### Resume Category Predictor
1. **Navigate to Resume Category Predictor**
   - Click on "Resume Category Predictor" from the home page

2. **Input Resume**
   - **Option 1**: Upload a PDF resume by dragging and dropping or clicking "Choose File"
   - **Option 2**: Paste your resume text directly into the text area

3. **Analyze**
   - Click "Analyze Resume" to process your input
   - Wait for the AI to categorize your resume

4. **View Results**
   - See the top 3 predicted job categories
   - View confidence scores for each prediction
   - Optionally view the processed text

#### Job Description Score Analysis
1. **Navigate to Job Description Score**
   - Click on "Job Description Score" from the home page

2. **Input Resume and Job Description**
   - **Resume**: Upload a PDF or paste text
   - **Job Description**: Upload a PDF or paste text

3. **Get AI-Powered Insights**
   - View the match score and level (Excellent/Good/Fair/Poor)
   - Get detailed analysis including:
     - Key insights about the match
     - Your strengths for the role
     - Areas for improvement
     - Missing skills
     - Specific recommendations
     - Overall assessment

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

### Similarity Analysis
- **TF-IDF Vectorization**: For both resume and job description
- **Cosine Similarity**: Calculate match percentage
- **AI Analysis**: Gemini API for detailed insights

## 🎨 UI/UX Features

### Design Highlights
- **Modern Interface**: Clean, professional design with glass morphism effects
- **Responsive Layout**: Mobile-first design approach
- **Smooth Animations**: CSS transitions and keyframe animations
- **Interactive Elements**: Hover effects and micro-interactions
- **Loading States**: Beautiful spinner animations during processing

### User Experience
- **Drag & Drop**: Intuitive file upload interface
- **Real-time Validation**: Immediate feedback on input quality
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
- Resume length validation (minimum 100 characters)
- Content quality checks (no repetitive characters)
- File format verification
- Special character handling

### Model Performance Tests
- Accuracy metrics
- Processing speed tests
- Memory usage optimization
- Cross-validation results

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Required for job description analysis features

### Model Files
- `models/rf.pkl`: Random Forest classifier
- `models/tf_idf.pkl`: TF-IDF vectorizer
- `models/le.pkl`: Label encoder



## 👥 Authors

- **Ahmed Raza** - [Github](https://github.com/ahmed2402), [LinkedIn](https://www.linkedin.com/in/ahmvd/)

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact: ahmedraza312682@gmail.com

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

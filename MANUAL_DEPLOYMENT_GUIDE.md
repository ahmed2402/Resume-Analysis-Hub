# Manual Deployment Guide for PythonAnywhere

## Prerequisites
1. PythonAnywhere account (free tier available)
2. Gemini API key from Google AI Studio
3. All your project files ready for upload

## Step-by-Step Manual Deployment

### Step 1: Prepare Your Files
Ensure you have these files ready for upload:
- `home.py` (main Flask application)
- `wsgi.py` (WSGI configuration)
- `requirements.txt` (dependencies)
- `runtime.txt` (Python version)
- `models/` folder (with all .pkl files)
- `templates/` folder (all HTML templates)
- `static/` folder (CSS, JS, images)
- `uploads/` folder (empty folder for file uploads)

### Step 2: Create Project Directory on PythonAnywhere

1. **Go to PythonAnywhere Dashboard**
   - Login to [pythonanywhere.com](https://www.pythonanywhere.com)
   - Go to **Files** tab

2. **Create Project Directory**
   - Click **New directory**
   - Name it: `Resume-Analysis-Hub`
   - Click **Create**

### Step 3: Upload Your Files

#### Option A: Upload Individual Files
1. **Navigate to your project directory**
   - Click on `Resume-Analysis-Hub` folder

2. **Upload main files**
   - Click **Upload a file** for each file:
     - `home.py`
     - `wsgi.py`
     - `requirements.txt`
     - `runtime.txt`

3. **Create and upload folders**
   - Click **New directory** for each folder:
     - `models`
     - `templates`
     - `static`
     - `uploads`

4. **Upload folder contents**
   - Go into each folder and upload the contents:
     - `models/`: Upload all `.pkl` files
     - `templates/`: Upload all HTML files
     - `static/`: Upload all CSS, JS, and image files

#### Option B: Upload ZIP File (Recommended)
1. **Create ZIP file locally**
   - Select all your project files
   - Right-click → Create archive/ZIP
   - Name it: `Resume-Analysis-Hub.zip`

2. **Upload ZIP file**
   - Go to `Resume-Analysis-Hub` directory
   - Click **Upload a file**
   - Select your ZIP file

3. **Extract ZIP file**
   - In PythonAnywhere console (Bash):
   ```bash
   cd /home/yourusername/Resume-Analysis-Hub
   unzip Resume-Analysis-Hub.zip
   rm Resume-Analysis-Hub.zip
   ```

### Step 4: Set Up Virtual Environment

1. **Open Bash Console**
   - Go to **Consoles** tab
   - Click **Bash**

2. **Navigate to project directory**
   ```bash
   cd /home/yourusername/Resume-Analysis-Hub
   ```

3. **Create virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Download NLTK data**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
   ```

### Step 5: Create Web App

1. **Go to Web Tab**
   - Click **Web** tab in PythonAnywhere dashboard
   - Click **Add a new web app**

2. **Configure Web App**
   - **Domain name**: Choose your subdomain
   - **Python version**: Select **3.11** (or 3.12)
   - **Framework**: Select **Flask**
   - **Python file**: Enter `home.py`

3. **Set up configuration**
   - **Source code**: `/home/yourusername/Resume-Analysis-Hub`
   - **Working directory**: `/home/yourusername/Resume-Analysis-Hub`
   - **Virtual environment**: `/home/yourusername/Resume-Analysis-Hub/venv`

### Step 6: Configure WSGI File

1. **Edit WSGI file**
   - In **Web** tab, click on your web app
   - Click **WSGI configuration file**
   - Replace content with:
   ```python
   import sys
   import os
   
   # Add your project directory to the sys.path
   path = '/home/yourusername/Resume-Analysis-Hub'
   if path not in sys.path:
       sys.path.append(path)
   
   from home import app as application
   ```
   - **Important**: Replace `yourusername` with your actual username

2. **Save the file**

### Step 7: Set Environment Variables

1. **Add environment variable**
   - In **Web** tab → **Environment variables**
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Your actual Gemini API key
   - Click **Add**

### Step 8: Reload and Test

1. **Reload web app**
   - Click **Reload** button in **Web** tab

2. **Test your application**
   - Visit your PythonAnywhere URL
   - Test resume classification feature
   - Test job description matching

## File Structure on PythonAnywhere

Your final structure should look like:
```
/home/yourusername/
└── Resume-Analysis-Hub/
    ├── home.py
    ├── wsgi.py
    ├── requirements.txt
    ├── runtime.txt
    ├── venv/
    ├── models/
    │   ├── rf.pkl
    │   ├── tf_idf.pkl
    │   └── le.pkl
    ├── templates/
    │   ├── home/
    │   ├── resume_classifier/
    │   └── job_desc/
    ├── static/
    │   ├── home/
    │   ├── resume_classifier/
    │   ├── job_desc/
    │   └── js/
    └── uploads/
```

## Troubleshooting

### Common Issues:

1. **Import errors**
   - Check file paths in WSGI file
   - Verify all files are uploaded correctly

2. **Model loading errors**
   - Ensure all `.pkl` files are in `models/` directory
   - Check file permissions

3. **Template not found errors**
   - Verify `templates/` folder structure
   - Check template file names

4. **Static files not loading**
   - Ensure `static/` folder structure is correct
   - Check file permissions

### Verification Commands:
```bash
cd /home/yourusername/Resume-Analysis-Hub
ls -la  # Check all files are present
ls -la models/  # Check model files
ls -la templates/  # Check template files
ls -la static/  # Check static files
```

## Your App URL
Once deployed, your app will be available at:
`yourusername.pythonanywhere.com`

## Maintenance
- Monitor error logs in PythonAnywhere dashboard
- Keep dependencies updated
- Backup your models and data regularly

Your Resume Classifier should now be successfully deployed manually on PythonAnywhere! 🚀 
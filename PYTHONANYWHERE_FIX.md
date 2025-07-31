# Fix Python 3.13 Compatibility Issue on PythonAnywhere

## Problem
You're getting a `ModuleNotFoundError: No module named 'distutils'` error because Python 3.13 removed the `distutils` module, which some packages still depend on.

## Solution: Use Python 3.11

### Step 1: Delete Current Virtual Environment
```bash
cd /home/ahmvd/Resume-Analysis-Hub
rm -rf venv
```

### Step 2: Create New Virtual Environment with Python 3.11
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### Step 3: Upgrade pip
```bash
pip install --upgrade pip
```

### Step 4: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 5: Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

## Alternative Solution: If Python 3.11 is not available

### Option A: Use Python 3.12
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Option B: Install setuptools first
If you must use Python 3.13:
```bash
pip install setuptools wheel
pip install -r requirements.txt
```

## Configure PythonAnywhere Web App

### Step 1: Go to Web Tab
1. In PythonAnywhere dashboard, go to **Web** tab
2. Click on your web app

### Step 2: Set Python Version
1. In **Code** section, set **Python version** to **3.11** (or 3.12)
2. Set **Source code** to: `/home/ahmvd/Resume-Analysis-Hub`
3. Set **Working directory** to: `/home/ahmvd/Resume-Analysis-Hub`

### Step 3: Configure Virtual Environment
1. In **Virtual environment** section:
   - Set to: `/home/ahmvd/Resume-Analysis-Hub/venv`

### Step 4: Update WSGI File
Make sure your WSGI file contains:
```python
import sys
import os

# Add your project directory to the sys.path
path = '/home/ahmvd/Resume-Analysis-Hub'
if path not in sys.path:
    sys.path.append(path)

from home import app as application
```

### Step 5: Set Environment Variables
1. In **Environment variables** section:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Your actual Gemini API key

### Step 6: Reload Web App
1. Click **Reload** button
2. Check error logs if any issues occur

## Verify Installation
```bash
cd /home/ahmvd/Resume-Analysis-Hub
source venv/bin/activate
python -c "import flask, joblib, nltk, sklearn; print('All packages installed successfully!')"
```

## Common Issues and Solutions

### Issue 1: Python 3.11 not available
- Try Python 3.12 or 3.10
- Contact PythonAnywhere support if needed

### Issue 2: Permission errors
```bash
chmod +x venv/bin/activate
```

### Issue 3: Path issues
- Double-check all paths in WSGI file
- Ensure project directory exists and has correct permissions

### Issue 4: Model loading errors
- Verify all `.pkl` files are in `models/` directory
- Check file permissions: `ls -la models/`

## Testing Your Deployment
1. Visit your PythonAnywhere URL
2. Test resume classification
3. Test job description matching
4. Check error logs in PythonAnywhere dashboard

Your app should now work without the Python 3.13 compatibility issues! 🚀 
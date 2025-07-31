# Deployment Guide for Resume Classifier on Render

## Prerequisites
1. A Render account (free tier available)
2. A Gemini API key from Google AI Studio
3. Your project code pushed to a Git repository (GitHub, GitLab, etc.)

## Step-by-Step Deployment Instructions

### 1. Prepare Your Repository
- Ensure all files are committed and pushed to your Git repository
- Make sure your repository is public or you have a paid Render account for private repos

### 2. Set Up Render Account
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your Git repository

### 3. Configure the Web Service
- **Name**: `resume-classifier` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn wsgi:app`
- **Plan**: Free (or choose a paid plan for better performance)

### 4. Set Environment Variables
In the Render dashboard, go to your service settings and add:
- **Key**: `GEMINI_API_KEY`
- **Value**: Your actual Gemini API key from Google AI Studio

### 5. Deploy
- Click "Create Web Service"
- Render will automatically build and deploy your application
- The first deployment may take 5-10 minutes

### 6. Access Your Application
- Once deployed, Render will provide a URL like: `https://your-app-name.onrender.com`
- Your application will be accessible at this URL

## Important Notes
- The free tier of Render will spin down your service after 15 minutes of inactivity
- The first request after inactivity may take 30-60 seconds to respond
- For production use, consider upgrading to a paid plan

## Troubleshooting
- Check the build logs in Render dashboard if deployment fails
- Ensure all dependencies are listed in `requirements.txt`
- Verify your Gemini API key is correctly set in environment variables
- Make sure your model files are included in the repository

## Local Testing
Before deploying, test locally:
```bash
pip install -r requirements.txt
python home.py
``` 
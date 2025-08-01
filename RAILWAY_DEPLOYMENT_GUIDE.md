# Railway Deployment Guide for Resume Classifier

## Prerequisites
1. Railway account (free tier available)
2. GitHub account
3. Gemini API key from Google AI Studio

## Step-by-Step Railway Deployment

### Step 1: Prepare Your Repository
1. **Push your code to GitHub**
   - Create a new repository on GitHub
   - Push your project files to the repository
   - Ensure all files are committed and pushed

### Step 2: Connect to Railway
1. **Go to Railway Dashboard**
   - Visit [railway.app](https://railway.app)
   - Sign in with your GitHub account

2. **Create New Project**
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose your repository

### Step 3: Configure Environment Variables
1. **Add Environment Variables**
   - In your Railway project dashboard, go to **Variables** tab
   - Add the following variable:
     - **Key**: `GEMINI_API_KEY`
     - **Value**: Your actual Gemini API key from Google AI Studio

### Step 4: Deploy
1. **Automatic Deployment**
   - Railway will automatically detect your Flask app
   - It will use the `Procfile` to know how to run your application
   - The deployment will start automatically

2. **Monitor Deployment**
   - Check the **Deployments** tab to monitor the build process
   - Look for any errors in the build logs

### Step 5: Access Your App
1. **Get Your App URL**
   - Once deployed, Railway will provide a URL
   - You can find it in the **Settings** tab under **Domains**
   - Your app will be available at: `https://your-app-name.railway.app`

## File Structure for Railway

Your project should have this structure:
```
Resume-Classifier/
├── home.py                 # Main Flask application
├── Procfile               # Railway deployment file
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version
├── models/               # ML model files
│   ├── rf.pkl
│   ├── tf_idf.pkl
│   └── le.pkl
├── templates/            # HTML templates
│   ├── home/
│   ├── resume_classifier/
│   └── job_desc/
├── static/              # CSS, JS, images
│   ├── home/
│   ├── resume_classifier/
│   ├── job_desc/
│   └── js/
└── uploads/             # Upload directory (empty)
```

## Important Notes

### Environment Variables
- Railway automatically provides a `PORT` environment variable
- Your app is configured to use this port automatically
- Make sure to set `GEMINI_API_KEY` in Railway dashboard

### File Uploads
- Railway uses ephemeral storage, so uploaded files will be temporary
- Files are automatically cleaned up after processing
- This is handled in your `home.py` code

### Dependencies
- All required packages are listed in `requirements.txt`
- Railway will automatically install them during deployment

## Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check the build logs in Railway dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify Python version in `runtime.txt`

2. **Import Errors**
   - Make sure all model files (`.pkl`) are in the `models/` directory
   - Check that all template and static files are present

3. **Environment Variable Issues**
   - Verify `GEMINI_API_KEY` is set correctly in Railway dashboard
   - Check that the variable name matches exactly

4. **Port Issues**
   - Railway automatically handles port configuration
   - Your app is configured to use the `PORT` environment variable

### Verification Commands:
You can check your deployment logs in the Railway dashboard:
- Go to **Deployments** tab
- Click on the latest deployment
- Check the build and runtime logs

## Updating Your App

1. **Automatic Updates**
   - Push changes to your GitHub repository
   - Railway will automatically redeploy

2. **Manual Redeploy**
   - In Railway dashboard, go to **Deployments**
   - Click **"Redeploy"** if needed

## Monitoring

- **Logs**: Check the **Deployments** tab for logs
- **Metrics**: Railway provides basic metrics in the dashboard
- **Errors**: Monitor the logs for any runtime errors

## Cost Considerations

- Railway free tier includes:
  - 500 hours of runtime per month
  - 1GB of storage
  - Automatic sleep after inactivity

Your Resume Classifier should now be successfully deployed on Railway! 🚀

## Next Steps

1. Test all features of your app
2. Set up a custom domain if needed
3. Monitor the app performance
4. Set up alerts for any issues 
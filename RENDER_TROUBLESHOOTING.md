# Deployment Troubleshooting Guide for Render

## Error: "Error in prediction. Please check your inputs."

This generic error message can be caused by several issues. The updated app.py now provides detailed error logging.

## Step-by-Step Troubleshooting

### 1. Check Render Deployment Logs

After deploying, go to your Render dashboard and check the logs:

1. Go to https://dashboard.render.com
2. Select your service "employee-prediction"
3. Click on "Logs" tab
4. Look for error messages from the application startup and prediction

You should see messages like:
- `✓ Model loaded successfully from: /path/to/gwp.pkl`
- `✓ Dataset loaded successfully from: /path/to/garments_worker_productivity.csv`
- `✓ Static directory is writable`

If you see error messages like:
- `✗ Model file not found`
- `✗ Dataset file not found`
- `✗ Static directory is not writable`

Then we need to fix file path issues.

### 2. Ensure Required Files are Deployed

Make sure these files are in your repository:

```
Employee Performance Prediction/
├── Flask/
│   ├── app.py
│   ├── gwp.pkl           ← Model file (REQUIRED)
│   ├── static/
│   └── templates/
├── Dataset/
│   └── garments_worker_productivity.csv  ← Dataset (REQUIRED)
├── requirements.txt
├── .python-version
└── render.yaml
```

**Critical:** Both `gwp.pkl` and `garments_worker_productivity.csv` MUST be in your Git repository.

### 3. Verify Files in Git

Run these commands to check if files are committed:

```bash
git status
git ls-files | grep gwp.pkl
git ls-files | grep garments_worker_productivity.csv
```

If files are not listed, add them:

```bash
git add Flask/gwp.pkl
git add Dataset/garments_worker_productivity.csv
git commit -m "Add model and dataset files"
git push
```

### 4. Common Issues and Solutions

#### Issue: Model or Dataset Not Found

**Solution:** Check your .gitignore file. Remove any patterns that might be excluding these files:

```bash
# BAD - These will exclude required files:
*.pkl
*.csv
Dataset/

# GOOD - Your .gitignore should NOT contain the above patterns
```

#### Issue: File Size Too Large

If `gwp.pkl` is larger than 100MB:

**Solution 1:** Use Git LFS (Large File Storage)
```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes Flask/gwp.pkl
git commit -m "Track model file with LFS"
git push
```

**Solution 2:** Host model file externally and download during build:
1. Upload gwp.pkl to cloud storage (Google Drive, Dropbox, S3)
2. Modify Flask/app.py to download the model on startup:

```python
import requests

MODEL_URL = "https://your-cloud-storage-url/gwp.pkl"
model_path = os.path.join(BASE_DIR, 'gwp.pkl')

if not os.path.exists(model_path):
    print("Downloading model file...")
    response = requests.get(MODEL_URL)
    with open(model_path, 'wb') as f:
        f.write(response.content)
    print("Model downloaded successfully")
```

#### Issue: Static Directory Not Writable

Render's file system might be read-only for certain directories.

**Solution:** Store generated graphs in memory or use Render's disk:

Update render.yaml to add a disk:

```yaml
services:
  - type: web
    name: employee-prediction
    runtime: python
    plan: free
    buildCommand: pip install --upgrade pip && pip install -r requirements.txt
    startCommand: cd Flask && gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120 app:app
    disk:
      name: employee-prediction-disk
      mountPath: /opt/render/project/Flask/static/output
      sizeGB: 1
```

### 5. Test Locally First

Before deploying again, test locally:

```bash
cd Flask
python app.py
```

Visit http://127.0.0.1:5000 and test a prediction. If it works locally but not on Render, the issue is deployment-specific.

### 6. Redeploy with Enhanced Logging

After making the above changes:

```bash
git add .
git commit -m "Fix deployment issues - add enhanced error logging"
git push
```

Render will automatically redeploy. Watch the logs carefully.

### 7. Check Render Build Output

In the "Deploy" tab, check the build logs to ensure:
- Python 3.11.7 is being used (not 3.13)
- All packages install successfully
- No warnings about missing files

### 8. Environment-Specific Issues

If the error persists, it might be environment-specific. Check:

**File Permissions:**
- Render might have strict file permissions
- Static directory might not exist or be writable

**Memory Limits:**
- Free tier has 512MB RAM limit
- Model loading might fail due to memory constraints

**Path Separators:**
- Local Windows uses `\` but Render (Linux) uses `/`
- The updated app.py uses `os.path.join()` which handles this correctly

## Updated Features in Latest app.py

The latest version includes:

1. **Startup Validation:**
   - Checks model file exists and loads correctly
   - Checks dataset file exists and loads correctly
   - Tests static directory write permissions

2. **Detailed Error Messages:**
   - Each error includes specific cause (model loading, prediction, graph generation)
   - Traceback printed to logs for debugging

3. **Graceful Degradation:**
   - If graphs fail to generate, prediction still returns (graphs will be empty)
   - Individual graph generation errors don't break entire prediction

4. **Better Logging:**
   - Print statements at each step to track execution flow
   - Helps identify exactly where failure occurs

## Next Steps

1. Commit and push all changes
2. Check Render logs after deployment
3. Look for specific error messages from the enhanced logging
4. If you see file not found errors, verify files are in Git repository
5. If you see permission errors, add disk mount to render.yaml
6. Report specific error message for targeted help

## Contact Points for Further Help

If issues persist, provide:
1. Complete error message from Render logs
2. Output of `git ls-files` to verify files are committed
3. Screenshot of Render deployment logs showing the startup messages

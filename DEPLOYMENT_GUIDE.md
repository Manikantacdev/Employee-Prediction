# 🚀 Production Deployment Guide

## ⚠️ Development Server Warning

The warning you're seeing:
```
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
```

This means Flask's built-in server (`app.run()`) is **not suitable for production** because:
- ❌ Not secure enough
- ❌ Can't handle multiple concurrent requests efficiently
- ❌ Lacks performance optimizations
- ❌ No load balancing
- ❌ Poor stability under heavy load

---

## 🎯 Recommended Deployment Options

### Option 1: 🟢 Simple Production Server (Waitress - Windows Friendly)

**Best for:** Small to medium projects, Windows servers, quick deployment

#### Step 1: Install Waitress
```bash
pip install waitress
```

#### Step 2: Create Production Starter File

Create `production_server.py` in the Flask folder:

```python
from waitress import serve
from app import app
import os

# Disable debug mode in production
app.config['DEBUG'] = False

# Set production configurations
app.config['PROPAGATE_EXCEPTIONS'] = True

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Starting production server on port {port}...")
    print(f"📊 Access the application at: http://localhost:{port}")
    serve(app, host='0.0.0.0', port=port, threads=4)
```

#### Step 3: Run Production Server
```bash
cd Flask
python production_server.py
```

**Advantages:**
- ✅ Works perfectly on Windows
- ✅ Production-ready WSGI server
- ✅ Handles multiple concurrent requests
- ✅ Better performance than development server
- ✅ Easy to set up

**Configuration Options:**
- `threads=4`: Number of worker threads (adjust based on CPU cores)
- `host='0.0.0.0'`: Accept connections from any IP
- `port=8080`: Server port

---

### Option 2: 🔵 Gunicorn (Linux/Mac Only)

**Best for:** Linux servers, production environments, better performance

#### Step 1: Install Gunicorn
```bash
pip install gunicorn
```

#### Step 2: Create Gunicorn Configuration

Create `gunicorn_config.py`:

```python
import multiprocessing

# Server socket
bind = "0.0.0.0:8080"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'employee_prediction'

# Server mechanics
daemon = False
pidfile = 'gunicorn.pid'
umask = 0
user = None
group = None
tmp_upload_dir = None
```

#### Step 3: Run with Gunicorn
```bash
cd Flask
gunicorn -c gunicorn_config.py app:app
```

**Advantages:**
- ✅ Industry standard for Flask apps
- ✅ Excellent performance
- ✅ Auto-restart workers
- ✅ Pre-fork worker model
- ❌ Linux/Mac only (doesn't work on Windows)

---

### Option 3: ☁️ Cloud Platform Deployment

#### A. **Azure App Service** (Recommended for Enterprise)

**Step 1: Prepare Files**

Create `requirements.txt`:
```bash
cd "d:\Py and ipynb\Employee Performance Prediction"
pip freeze > requirements.txt
```

Create `startup.sh`:
```bash
#!/bin/bash
cd Flask
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 4 app:app
```

**Step 2: Deploy via Azure CLI**
```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create resource group
az group create --name EmployeeProductivityRG --location eastus

# Create App Service plan
az appservice plan create --name EmployeePredictionPlan --resource-group EmployeeProductivityRG --sku B1 --is-linux

# Create web app
az webapp create --resource-group EmployeeProductivityRG --plan EmployeePredictionPlan --name employee-prediction-app --runtime "PYTHON|3.9"

# Deploy code
cd Flask
az webapp up --name employee-prediction-app --resource-group EmployeeProductivityRG
```

**Advantages:**
- ✅ Automatic scaling
- ✅ Built-in monitoring
- ✅ SSL certificates
- ✅ Custom domains
- ✅ High availability
- 💰 Paid service

---

#### B. **Heroku** (Easy & Free Tier Available)

**Step 1: Create Heroku Files**

Create `Procfile` in project root:
```
web: cd Flask && gunicorn app:app
```

Create `runtime.txt`:
```
python-3.9.18
```

**Step 2: Deploy**
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create employee-productivity-prediction

# Deploy
git init
git add .
git commit -m "Initial deployment"
git push heroku main

# Open app
heroku open
```

**Advantages:**
- ✅ Free tier available
- ✅ Very easy to deploy
- ✅ Git-based deployment
- ✅ Automatic SSL
- ⚠️ Free tier sleeps after 30 mins inactivity

---

#### C. **Google Cloud Run** (Containerized Deployment)

**Step 1: Create Dockerfile**

Create `Dockerfile` in Flask folder:
```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8080

# Run with Gunicorn
CMD exec gunicorn --bind :8080 --workers 2 --threads 4 --timeout 120 app:app
```

**Step 2: Deploy to Cloud Run**
```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy employee-prediction \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Advantages:**
- ✅ Serverless (pay per use)
- ✅ Auto-scaling
- ✅ Containerized (portable)
- ✅ Fast cold starts
- 💰 Pay per request

---

### Option 4: 🐳 Docker Containerization

**Best for:** Consistent deployment across environments, scalability

#### Create Docker Setup

**Dockerfile** (in Flask folder):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for matplotlib
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir waitress

# Copy application code
COPY . .

# Create static directory if it doesn't exist
RUN mkdir -p static

# Expose port
EXPOSE 8080

# Run with Waitress
CMD ["python", "production_server.py"]
```

**docker-compose.yml** (in project root):
```yaml
version: '3.8'

services:
  web:
    build: ./Flask
    ports:
      - "8080:8080"
    volumes:
      - ./Flask:/app
      - ./Dataset:/app/../Dataset
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

**Build and Run:**
```bash
# Build image
docker build -t employee-prediction ./Flask

# Run container
docker run -p 8080:8080 employee-prediction

# Or use docker-compose
docker-compose up -d
```

**Advantages:**
- ✅ Consistent environment
- ✅ Easy to scale
- ✅ Portable across platforms
- ✅ Isolates dependencies

---

## 🔧 Production Configuration Checklist

### 1. Update `app.py` for Production

Add these configurations at the top of `app.py`:

```python
import os

# Production mode detection
IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production'

# Configuration
app.config['DEBUG'] = False if IS_PRODUCTION else True
app.config['TESTING'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure static directory exists
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
```

### 2. Create `requirements.txt`

```bash
pip freeze > requirements.txt
```

Or manually create:
```txt
Flask==3.0.0
pandas==2.1.0
numpy==1.24.3
scikit-learn==1.3.0
matplotlib==3.7.2
seaborn==0.12.2
xgboost==1.7.6
Werkzeug==3.0.1
```

### 3. Environment Variables

Create `.env` file (don't commit to Git):
```env
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
PORT=8080
```

### 4. Security Improvements

Install security packages:
```bash
pip install flask-talisman flask-cors
```

Update `app.py`:
```python
from flask_talisman import Talisman
from flask_cors import CORS

# Enable HTTPS redirect and security headers
if IS_PRODUCTION:
    Talisman(app, content_security_policy=None)
    
# Enable CORS if needed
CORS(app)
```

### 5. Logging Setup

Add to `app.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

if IS_PRODUCTION:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/employee_prediction.log', 
                                      maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Employee Prediction startup')
```

---

## 🎯 Recommended Deployment Path

### For Quick Production (Windows):
1. ✅ Use **Waitress** (Option 1)
2. ✅ Create `production_server.py`
3. ✅ Run with `python production_server.py`

### For Professional Deployment:
1. ✅ Create **Docker container** (Option 4)
2. ✅ Deploy to **Azure App Service** or **Google Cloud Run**
3. ✅ Set up monitoring and logging
4. ✅ Configure custom domain and SSL

### For Budget-Friendly:
1. ✅ Use **Heroku** (free tier)
2. ✅ Simple git-based deployment
3. ✅ Automatic SSL included

---

## 📊 Performance Optimization

### 1. Enable Caching

Install Flask-Caching:
```bash
pip install Flask-Caching
```

Add to `app.py`:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=300)
def expensive_operation():
    # Your code here
    pass
```

### 2. Use CDN for Static Files

- Upload CSS, JS, images to a CDN
- Update templates to use CDN URLs
- Reduces server load

### 3. Database Connection Pooling

If using a database:
```bash
pip install SQLAlchemy
```

### 4. Compress Responses

```bash
pip install Flask-Compress
```

```python
from flask_compress import Compress
Compress(app)
```

---

## 🔐 Security Best Practices

1. **Never expose debug mode in production**
   ```python
   app.config['DEBUG'] = False
   ```

2. **Use environment variables for secrets**
   ```python
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

3. **Enable HTTPS**
   - Use SSL certificates
   - Redirect HTTP to HTTPS

4. **Input validation**
   - Already implemented in form validation
   - Add server-side validation

5. **Rate limiting**
   ```bash
   pip install Flask-Limiter
   ```

6. **Keep dependencies updated**
   ```bash
   pip list --outdated
   pip install --upgrade <package>
   ```

---

## 📈 Monitoring & Maintenance

### 1. Set Up Application Monitoring

**Using Azure Application Insights:**
```bash
pip install applicationinsights
```

**Using New Relic:**
```bash
pip install newrelic
```

### 2. Error Tracking

**Using Sentry:**
```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

### 3. Health Check Endpoint

Add to `app.py`:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'version': '1.0'}, 200
```

---

## 🚀 Quick Start Production Deployment

### Immediate Action (Waitress on Windows):

1. **Install Waitress:**
   ```bash
   pip install waitress
   ```

2. **Create `production_server.py` in Flask folder:**
   ```python
   from waitress import serve
   from app import app
   
   app.config['DEBUG'] = False
   
   if __name__ == '__main__':
       print("🚀 Production server starting on http://localhost:8080")
       serve(app, host='0.0.0.0', port=8080, threads=4)
   ```

3. **Run:**
   ```bash
   cd Flask
   python production_server.py
   ```

4. **Access:**
   ```
   http://localhost:8080
   ```

**That's it! Your app is now running on a production-grade server!** 🎉

---

## 📞 Support & Resources

- **Flask Deployment Documentation**: https://flask.palletsprojects.com/en/latest/deploying/
- **Waitress Documentation**: https://docs.pylonsproject.org/projects/waitress/
- **Gunicorn Documentation**: https://docs.gunicorn.org/
- **Azure App Service**: https://azure.microsoft.com/en-us/services/app-service/
- **Heroku Flask Guide**: https://devcenter.heroku.com/articles/getting-started-with-python

---

**Project by:** Manikanta Gedda  
**Last Updated:** December 21, 2025  
**Version:** 1.0

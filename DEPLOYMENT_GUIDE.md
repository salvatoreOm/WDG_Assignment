# 🚀 NGO Impact Tracker - Deployment Guide

This guide will help you deploy your full-stack NGO Impact Tracker application.

## 📋 **Architecture Overview**

- **Frontend (React)**: Deploy to Vercel ✅
- **Backend (Django + Celery + Redis)**: Deploy to Railway/Render/Heroku ⚙️

## 🎯 **Part 1: Deploy Frontend to Vercel**

### **Prerequisites**
- GitHub account
- Vercel account (free)
- Push your code to GitHub

### **Step 1: Prepare Repository**

```bash
# Make sure your code is pushed to GitHub
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### **Step 2: Deploy to Vercel**

1. **Go to [vercel.com](https://vercel.com)** and sign in with GitHub
2. **Click "New Project"**
3. **Import your repository**
4. **Configure Project Settings**:
   - **Framework Preset**: `Create React App`
   - **Root Directory**: Leave empty (we have `vercel.json` config)
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `frontend/build`
   - **Install Command**: `npm install` (auto-detected)

5. **Set Environment Variables** in Vercel Dashboard:
   ```
   REACT_APP_API_URL = https://your-backend-url.railway.app/api
   ```
   *(Replace with your actual backend URL once deployed)*

6. **Click "Deploy"**

### **Step 3: Configure Custom Domain (Optional)**
- In Vercel Dashboard → Domains
- Add your custom domain
- Update DNS settings as instructed

---

## ⚙️ **Part 2: Deploy Backend to Railway**

### **Why Railway?**
- ✅ Supports Django + Celery + Redis
- ✅ Built-in Redis service
- ✅ Easy database management
- ✅ Free tier available
- ✅ Automatic deployments from GitHub

### **Step 1: Prepare Backend for Production**

Create production requirements:

```bash
# Add to requirements.txt:
gunicorn==21.2.0
psycopg2-binary==2.9.7
whitenoise==6.5.0
```

### **Step 2: Create Production Settings**

Create `ngo_impact_tracker/settings_production.py`:

```python
from .settings import *
import os

# Production settings
DEBUG = False
ALLOWED_HOSTS = ['*']  # Configure specific domains in production

# Database - Use PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE'),
        'USER': os.environ.get('PGUSER'),
        'PASSWORD': os.environ.get('PGPASSWORD'),
        'HOST': os.environ.get('PGHOST'),
        'PORT': os.environ.get('PGPORT', 5432),
    }
}

# Redis Configuration
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS for production frontend
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-app.vercel.app",
]
```

### **Step 3: Create Railway Configuration Files**

**Procfile** (for Railway):
```
web: gunicorn ngo_impact_tracker.wsgi:application
worker: celery -A ngo_impact_tracker worker --loglevel=info
```

**railway.json**:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn ngo_impact_tracker.wsgi:application",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**nixpacks.toml**:
```toml
[phases.setup]
nixPkgs = ['...', 'postgresql']

[phases.install]
cmds = ['pip install -r requirements.txt']

[phases.build]
cmds = ['python manage.py collectstatic --noinput']

[start]
cmd = 'gunicorn ngo_impact_tracker.wsgi:application'
```

### **Step 4: Deploy to Railway**

1. **Go to [railway.app](https://railway.app)** and sign in with GitHub
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository**
5. **Add Services**:
   - **PostgreSQL Database** (click "Add Service" → "Database" → "PostgreSQL")
   - **Redis** (click "Add Service" → "Database" → "Redis")

6. **Configure Environment Variables**:
   ```
   DJANGO_SETTINGS_MODULE = ngo_impact_tracker.settings_production
   SECRET_KEY = your-secret-key-here
   PGDATABASE = ${{Postgres.PGDATABASE}}
   PGHOST = ${{Postgres.PGHOST}}
   PGPASSWORD = ${{Postgres.PGPASSWORD}}
   PGPORT = ${{Postgres.PGPORT}}
   PGUSER = ${{Postgres.PGUSER}}
   REDIS_URL = ${{Redis.REDIS_URL}}
   ```

7. **Deploy**:
   - Railway will automatically build and deploy
   - Check logs for any issues
   - Run migrations: `python manage.py migrate`

### **Step 5: Configure Celery Worker**

Add a second service for Celery worker:
1. **Duplicate your main service**
2. **Change start command to**: `celery -A ngo_impact_tracker worker --loglevel=info`
3. **Use same environment variables**

---

## 🔗 **Part 3: Connect Frontend to Backend**

### **Update Vercel Environment Variables**

Once your backend is deployed, update Vercel:

1. **Go to Vercel Dashboard** → Your Project → Settings → Environment Variables
2. **Update**:
   ```
   REACT_APP_API_URL = https://your-backend-app.railway.app/api
   ```
3. **Redeploy** frontend

### **Update CORS Settings**

In your backend `settings_production.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-app.vercel.app",
]
```

---

## 🧪 **Part 4: Test Deployment**

### **Test Frontend**
- Visit your Vercel URL
- Check browser console for API calls
- Test form submission

### **Test Backend**
- Visit `https://your-backend-app.railway.app/api/docs/`
- Test API endpoints
- Check Celery worker logs

### **Test Full Flow**
1. Submit a single report
2. Upload a CSV file
3. Check job status
4. View dashboard data

---

## 🛡️ **Part 5: Production Security (Important!)**

### **Environment Variables**
```python
# Generate new secret key
SECRET_KEY = os.environ.get('SECRET_KEY')

# Specific allowed hosts
ALLOWED_HOSTS = ['your-backend-app.railway.app']

# Specific CORS origins
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-app.vercel.app",
]
```

### **Database Security**
- Use PostgreSQL (not SQLite)
- Enable SSL connections
- Regular backups

### **Redis Security**
- Use Railway's managed Redis
- Enable authentication
- Monitor connections

---

## 📊 **Alternative Backend Platforms**

If Railway doesn't work for you:

### **Render** (Similar to Railway)
```yaml
# render.yaml
services:
  - type: web
    name: ngo-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn ngo_impact_tracker.wsgi:application"
  
  - type: worker
    name: ngo-worker
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "celery -A ngo_impact_tracker worker"
```

### **Heroku** (Requires paid Redis)
```
# Add buildpacks
heroku buildpacks:add heroku/python

# Add addons
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
```

### **DigitalOcean App Platform**
```yaml
# .do/app.yaml
name: ngo-impact-tracker
services:
- name: web
  source_dir: /
  github:
    repo: your-username/your-repo
    branch: main
  run_command: gunicorn ngo_impact_tracker.wsgi:application
  
- name: worker
  source_dir: /
  run_command: celery -A ngo_impact_tracker worker
```

---

## 🎯 **Summary**

1. **Frontend**: `your-app.vercel.app` ✅
2. **Backend**: `your-app.railway.app` ✅
3. **Database**: PostgreSQL on Railway ✅
4. **Redis**: Managed Redis on Railway ✅
5. **Background Jobs**: Celery worker on Railway ✅

Your NGO Impact Tracker is now production-ready! 🚀

---

## 🆘 **Troubleshooting**

### **Common Issues**

**CORS Errors**:
```python
# Add to Django settings
CORS_ALLOWED_ORIGINS = ["https://your-frontend.vercel.app"]
```

**Database Connection Issues**:
```bash
# Check Railway logs
railway logs

# Run migrations
railway run python manage.py migrate
```

**Celery Not Working**:
```bash
# Check worker logs
railway logs --service your-worker-service
```

**Build Failures**:
```bash
# Check requirements.txt
# Ensure all dependencies are listed
# Check Python version compatibility
``` 
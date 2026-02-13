# 🚀 Cinemania - Docker & Render Deployment Guide

## 📋 Quick Overview

Your Django application has been containerized and is ready for deployment on Render's free tier. This guide explains the error you encountered and how it's been fixed.

---

## ❌ The Error You Had

```
ModuleNotFoundError: No module named 'cinemania.wsgi'
```

### What Was Wrong?
1. **Incorrect working directory handling**: Gunicorn couldn't find the `cinemania.wsgi` module
2. **Missing entrypoint script**: No proper startup sequence
3. **Static files not collected**: Would cause 404 errors for CSS/JS

### Why It Happened?
Your project structure has Django's `manage.py` in a subdirectory:
```
/app/cinemania/manage.py         ← The actual manage.py location
/app/cinemania/cinemania/wsgi.py ← What Gunicorn needs to find
```

Gunicorn was being run from `/app` and couldn't locate the module properly.

---

## ✅ What's Been Fixed

### 1. **New `entrypoint.sh` Script**
This is the core fix! It:
- ✅ Navigates to the Django directory
- ✅ Runs database migrations
- ✅ Collects static files
- ✅ Starts Gunicorn with proper configuration
- ✅ Handles the Render PORT environment variable

### 2. **Updated `Dockerfile`**
- ✅ Uses your Python 3.12 version
- ✅ Calls the entrypoint script instead of running Gunicorn directly
- ✅ Sets up environment variables properly
- ✅ Optimized for production

### 3. **Production Django Settings**
- ✅ `ALLOWED_HOSTS` properly configured
- ✅ `DEBUG=False` for security
- ✅ `SECRET_KEY` from environment
- ✅ Static files handled correctly

### 4. **Deployment Configuration**
- ✅ `render.yaml` - Render deployment spec
- ✅ `.env` - Environment variables
- ✅ `.dockerignore` - Optimization

---

## 🚀 Deployment Steps

### Step 1: Generate a Secure Secret Key
Run this in Python to generate a strong key:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
Copy the output - you'll need it for Render.

### Step 2: Commit and Push to Git
```bash
cd /home/jonaz/Cinemania
git add .
git commit -m "Add Docker and Render deployment configuration"
git push origin main
```

### Step 3: Deploy on Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Select **"Deploy an existing repository"**
4. Choose your Cinemania repository
5. Configure:
   - **Name**: `cinemania` (or your preferred name)
   - **Environment**: `Docker`
   - **Region**: `Oregon` (free tier)
   - **Plan**: `Free`

### Step 4: Set Environment Variables
In the Render dashboard, go to **"Environment"** and add:

```
SECRET_KEY=<paste-your-generated-secret-key-here>
DEBUG=False
ALLOWED_HOSTS=cinemania.onrender.com
TMDB_API_KEY=92492102bdac5ee5e66f112789815a7e
TMDB_API_BASE_URL=https://api.themoviedb.org/3/
TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p/w500/
```

### Step 5: Deploy
Click **"Deploy"** and wait for the build to complete (5-10 minutes).

### Step 6: Monitor
- Check the **Logs** tab in Render for any issues
- Once deployment is complete, your app will be at: `https://your-app-name.onrender.com`

---

## 📁 Files & What They Do

| File | Purpose |
|------|---------|
| `Dockerfile` | Defines how to build your Docker container |
| `entrypoint.sh` | Startup script that runs migrations and Gunicorn |
| `render.yaml` | Configuration for Render deployment |
| `.env` | Local environment variables |
| `.dockerignore` | Excludes unnecessary files from Docker image |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment documentation |
| `FIX_SUMMARY.md` | Technical explanation of the fix |

---

## 🧪 Testing Locally (Optional)

If you have Docker installed, you can test locally:

```bash
# Build the image
docker build -t cinemania:latest .

# Run the container
docker run -p 8000:8000 \
  -e SECRET_KEY='test-secret-key' \
  -e DEBUG='False' \
  -e ALLOWED_HOSTS='localhost,127.0.0.1' \
  -e TMDB_API_KEY='92492102bdac5ee5e66f112789815a7e' \
  cinemania:latest

# Visit http://localhost:8000
```

---

## ⚠️ Important Production Notes

### Security
- ⚠️ **Never commit `.env` to Git** (it contains sensitive data)
- ⚠️ Generate a unique `SECRET_KEY` for production (not the default)
- ⚠️ Set `DEBUG=False` (already configured)
- ⚠️ Use specific `ALLOWED_HOSTS` values (not `*`)

### Database
- Current setup uses SQLite (good for testing)
- For production, consider Render's PostgreSQL add-on
- SQLite can be slow with concurrent users

### Static Files
- CSS, JS, and images are automatically collected
- Served through WhiteNoise (already in middleware)
- First deployment might take longer due to collection

### Migrations
- Automatically run on startup via entrypoint script
- Check Render logs if migrations fail

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'cinemania.wsgi'"
✅ **Fixed**: The new entrypoint script handles this correctly.

### Build fails with "Dockerfile not found"
- Ensure `Dockerfile` is in the root directory
- Check Render settings - it should auto-detect

### Static files not loading (404 errors)
- Check that `STATIC_ROOT` is correctly set in `settings.py`
- Migrations must run successfully first

### Application crashes after deployment
- Check Render **Logs** tab for error messages
- Verify all environment variables are set
- Check that the SECRET_KEY is strong

### Can't access the application
- Wait a few minutes - Render might still be initializing
- Check that your domain shows in Render dashboard
- Clear browser cache

---

## 📊 What Happens During Deployment

1. **Build Phase**
   - Docker image is built
   - Python dependencies installed
   - Files copied to container

2. **Startup Phase** (handled by `entrypoint.sh`)
   - Database migrations run
   - Static files collected
   - Gunicorn starts

3. **Runtime Phase**
   - Your app handles requests
   - Logs appear in Render dashboard

---

## 📝 Checklist Before Deploying

- [ ] Generated a new `SECRET_KEY`
- [ ] Committed all changes to Git
- [ ] Pushed to main branch
- [ ] Created Render account
- [ ] Connected Git repository to Render
- [ ] Set all environment variables on Render dashboard
- [ ] `SECRET_KEY` is strong and unique
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` includes your Render domain

---

## 🆘 Need Help?

### Common Issues:
1. **Migrations fail** → Check database connection
2. **Static files missing** → Ensure `python manage.py collectstatic` ran
3. **500 errors** → Check Render logs and Django DEBUG settings

### Documentation:
- [Render Docs](https://render.com/docs)
- [Django Deployment](https://docs.djangoproject.com/en/5.0/howto/deployment/)
- [Gunicorn Configuration](https://docs.gunicorn.org/)

---

## 🎉 You're All Set!

Your Django application is now containerized and ready for production deployment on Render. Follow the deployment steps above, and you'll have your app live in minutes!

**Questions?** Check the detailed guides:
- `DEPLOYMENT_GUIDE.md` - Step-by-step guide
- `FIX_SUMMARY.md` - Technical details
- `DEPLOYMENT_CHECKLIST.txt` - Quick reference

Happy deploying! 🚀

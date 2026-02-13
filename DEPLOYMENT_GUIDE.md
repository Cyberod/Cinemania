# Django Application Deployment Guide - Render Free Plan

## Problem Analysis & Solution

### The Error You Encountered
```
ModuleNotFoundError: No module named 'cinemania.wsgi'
```

**Root Cause**: Gunicorn was being run from the wrong working directory without proper Python path configuration.

---

## What Was Fixed

### 1. **Dockerfile Improvements**
- ✅ Updated Python version to 3.12 (matching your local environment)
- ✅ Added proper working directory setup
- ✅ Added entrypoint script to handle migrations and static files
- ✅ Proper environment variables for production

### 2. **Created `entrypoint.sh` Script**
This script:
- Runs migrations automatically before starting the server
- Collects static files
- Properly sets the working directory
- Uses the `PORT` environment variable from Render (defaults to 8000)
- Runs Gunicorn with appropriate worker configuration

### 3. **Django Settings Updates**
- ✅ Better `ALLOWED_HOSTS` configuration with proper formatting
- ✅ Production-ready settings
- ✅ Proper static files handling with WhiteNoise (already in your middleware)

### 4. **Environment Variables**
Created proper `.env` configuration with:
- `SECRET_KEY` for production
- `DEBUG=False` for production
- `ALLOWED_HOSTS` configuration

---

## Deployment Steps

### Step 1: Prepare Your Git Repository
```bash
cd /home/jonaz/Cinemania

# Make sure all files are staged
git add Dockerfile entrypoint.sh render.yaml .env requirements.txt

# Commit your changes
git commit -m "Add Docker and Render configuration for deployment"

# Push to your repository (GitHub, GitLab, etc.)
git push origin main
```

### Step 2: Generate a Secure Secret Key
In Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
Copy this value - you'll need it for Render.

### Step 3: Set Up Render Service
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your Git repository
4. Configure the service:
   - **Name**: cinemania
   - **Region**: Oregon (free tier available)
   - **Branch**: main
   - **Runtime**: Docker
   - **Plan**: Free

### Step 4: Set Environment Variables on Render
In the Render dashboard, under "Environment Variables" add:

```
SECRET_KEY=<paste-the-secret-key-you-generated>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
TMDB_API_KEY=92492102bdac5ee5e66f112789815a7e
TMDB_API_BASE_URL=https://api.themoviedb.org/3/
TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p/w500/
```

### Step 5: Deploy
- Render will automatically build and deploy your application
- Check the Render dashboard logs for any issues
- Once deployed, your app will be available at `https://your-app-name.onrender.com`

---

## Testing Locally (If Docker is Available)

```bash
cd /home/jonaz/Cinemania

# Build the image
docker build -t cinemania:latest .

# Run the container
docker run -p 8000:8000 \
  -e SECRET_KEY='test-secret-key' \
  -e DEBUG='False' \
  -e ALLOWED_HOSTS='localhost,127.0.0.1' \
  -e TMDB_API_KEY='92492102bdac5ee5e66f112789815a7e' \
  -e TMDB_API_BASE_URL='https://api.themoviedb.org/3/' \
  -e TMDB_IMAGE_BASE_URL='https://image.tmdb.org/t/p/w500/' \
  cinemania:latest

# Visit http://localhost:8000
```

---

## Files Modified/Created

1. ✅ **Dockerfile** - Updated with proper configuration and entrypoint
2. ✅ **entrypoint.sh** - Handles migrations, static files, and Gunicorn startup
3. ✅ **render.yaml** - Render deployment configuration
4. ✅ **.env** - Environment variables for production
5. ✅ **settings.py** - Updated for production deployment
6. ✅ **build.sh** - Local build script for testing

---

## Troubleshooting

### If you still get "ModuleNotFoundError: No module named 'cinemania.wsgi'"
- Ensure the entrypoint.sh file has execute permissions
- Check that the Dockerfile correctly copies all files
- Verify your Git repository contains all necessary files

### If migrations fail
- Check Render logs for specific error messages
- Ensure your database is properly configured
- You may need to set up a persistent volume for SQLite or switch to PostgreSQL for free

### If static files don't load
- WhiteNoise is already in your middleware (good!)
- Static files are collected during container startup
- Check that `STATIC_ROOT` and `STATICFILES_DIRS` are correct in settings.py

### If the app keeps crashing
- Check Render logs for the exact error
- Verify all environment variables are set correctly
- Ensure the SECRET_KEY is strong and properly set

---

## Production Checklist

- [ ] SECRET_KEY is strong and unique (not the default)
- [ ] DEBUG is set to False
- [ ] ALLOWED_HOSTS includes your Render domain
- [ ] All environment variables are set on Render dashboard
- [ ] Code is pushed to main branch
- [ ] requirements.txt includes all dependencies
- [ ] entrypoint.sh has proper permissions
- [ ] Docker builds successfully locally (if testable)

---

## Next Steps (Optional but Recommended)

1. **Use PostgreSQL**: SQLite doesn't scale well. Consider using Render's PostgreSQL add-on.
2. **Set up logging**: Monitor your application in Render dashboard
3. **Use environment-specific settings**: Create separate settings for dev/prod
4. **Add health checks**: Implement `/health/` endpoint for Render monitoring
5. **Set up automated backups**: If using PostgreSQL, enable backups

---

## Support Resources

- [Render Deployment Docs](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Gunicorn Docs](https://docs.gunicorn.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

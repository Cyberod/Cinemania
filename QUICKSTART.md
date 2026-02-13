# 🚀 Quick Start: Deploy to Render in 5 Minutes

## What Was the Problem?
```
ModuleNotFoundError: No module named 'cinemania.wsgi'
```

**Why?** Gunicorn couldn't find your Django module because it was looking in the wrong directory.

**How Fixed?** Created an `entrypoint.sh` script that properly handles directory navigation before starting Gunicorn.

---

## 5-Step Deployment

### Step 1: Generate Secret Key (2 min)
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output - you'll need it.

### Step 2: Commit & Push (1 min)
```bash
cd /home/jonaz/Cinemania
git add .
git commit -m "Fix Docker deployment with entrypoint script"
git push origin main
```

### Step 3: Create Render Service (1 min)
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Name it: `cinemania`
5. Select Docker runtime

### Step 4: Set Environment Variables (1 min)
Add these in Render dashboard under "Environment":
```
SECRET_KEY=<paste-your-secret-key>
DEBUG=False
ALLOWED_HOSTS=cinemania.onrender.com
TMDB_API_KEY=92492102bdac5ee5e66f112789815a7e
TMDB_API_BASE_URL=https://api.themoviedb.org/3/
TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p/w500/
```

### Step 5: Deploy (5-10 min)
Click "Deploy" and wait. Check logs if there are issues.

---

## Done! ✅

Your app will be live at: `https://cinemania.onrender.com`

---

## If Something Goes Wrong

**Check Render Logs:**
1. Go to your Render dashboard
2. Click your service
3. Look at "Logs" tab

**Common Issues:**

| Issue | Fix |
|-------|-----|
| Still getting ModuleNotFoundError | Make sure entrypoint.sh file exists locally and was pushed |
| Static files not loading | Wait for build to complete, rebuild if needed |
| Port connection error | Check PORT env var is available (Render sets this) |
| 500 errors | Verify all environment variables are set |

---

## File Changes Summary

✅ **entrypoint.sh** - New startup script (THE KEY FIX)  
✅ **Dockerfile** - Updated to use entrypoint script  
✅ **settings.py** - Updated for production  
✅ **.env** - Added production variables  
✅ **render.yaml** - Added Render config  

---

## Need More Details?

- Quick reference: `DEPLOYMENT_CHECKLIST.txt`
- Full guide: `DEPLOYMENT_README.md`
- Technical details: `FIX_SUMMARY.md`
- Architecture: `ARCHITECTURE.md`

---

## Support

- Render Docs: https://render.com/docs
- Django Docs: https://docs.djangoproject.com/en/5.0/howto/deployment/

---

**You're all set! Your application is now containerized and ready for production.** 🎉

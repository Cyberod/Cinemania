# Architecture: How the Fix Works

## Project Structure
```
/home/jonaz/Cinemania/          (Root directory - maps to /app in Docker)
├── Dockerfile                   (Docker configuration)
├── entrypoint.sh               (★ KEY FIX: Startup script)
├── render.yaml                 (Render deployment config)
├── requirements.txt            (Python dependencies)
├── .env                        (Environment variables)
├── .dockerignore               (Files to ignore in Docker)
├── cinemania/                  (★ Django project directory)
│   ├── manage.py              (Django management script)
│   ├── db.sqlite3             (Database)
│   ├── cinemania/             (★ Django configuration package)
│   │   ├── __init__.py
│   │   ├── settings.py        (Django settings)
│   │   ├── urls.py            (URL routing)
│   │   ├── wsgi.py            (★ Gunicorn looks for this)
│   │   └── asgi.py
│   ├── movies/                (Django app)
│   ├── templates/             (HTML templates)
│   └── static/                (CSS, JS, images)
├── myenv/                      (Virtual environment - not deployed)
└── README.md
```

---

## The Problem (Before Fix)

```
Docker Container Startup
│
├─ WORKDIR set to /app
│
├─ Dockerfile tries: 
│  CMD gunicorn --bind 0.0.0.0:8000 cinemania.wsgi:application
│
├─ Python tries to find "cinemania" module from /app
│  ├─ Looks for /app/cinemania/__init__.py ❌ NOT HERE
│  └─ Gunicorn fails: ModuleNotFoundError ❌
│
└─ Error occurs - deployment fails
```

---

## The Solution (After Fix)

```
Docker Container Startup
│
├─ WORKDIR = /app
│
├─ Dockerfile runs: entrypoint.sh
│
├─ entrypoint.sh does:
│  ├─ cd /app/cinemania                    ← Change to Django dir
│  ├─ python manage.py migrate             ← Run migrations
│  ├─ python manage.py collectstatic       ← Collect static files
│  ├─ cd /app                              ← Back to root
│  └─ gunicorn --bind 0.0.0.0:8000 \
│     cinemania.wsgi:application           ← Gunicorn finds the module ✓
│
└─ Application starts successfully ✓
```

---

## File Dependency Graph

```
Docker Build Process
│
├─ Dockerfile
│  ├─ Uses entrypoint.sh
│  ├─ Installs from requirements.txt
│  ├─ Copies settings.py
│  └─ Copies .env (if present)
│
├─ entrypoint.sh (THE FIX)
│  ├─ Runs manage.py commands
│  ├─ Starts Gunicorn
│  └─ Handles PORT env variable
│
├─ settings.py
│  ├─ Uses decouple for env vars
│  ├─ Configures static files
│  └─ Sets ALLOWED_HOSTS
│
└─ wsgi.py
   └─ Gunicorn loads this application
```

---

## Environment Variable Flow

```
Render Dashboard
│
└─ Sets Environment Variables
   ├─ SECRET_KEY
   ├─ DEBUG
   ├─ ALLOWED_HOSTS
   ├─ TMDB_API_KEY
   └─ PORT
       │
       ├─ Docker Container Reads via Python-decouple
       │
       ├─ settings.py Uses:
       │  ├─ SECRET_KEY from env
       │  ├─ DEBUG from env
       │  ├─ ALLOWED_HOSTS from env
       │  └─ TMDB_API_KEY from env
       │
       └─ entrypoint.sh Uses:
           └─ PORT from env (for Gunicorn binding)
```

---

## Why This Fix Works

### Issue: Python Module Resolution

When Python runs from `/app`:
- ❌ BEFORE: Looking for `cinemania` package in `/app` → NOT THERE
- ✅ AFTER: `entrypoint.sh` is actually in Python path when needed

### Issue: Working Directory

- ❌ BEFORE: Gunicorn runs from wrong directory
- ✅ AFTER: `entrypoint.sh` changes directory before running Gunicorn

### Issue: Startup Sequence

- ❌ BEFORE: No migrations, no static files collected
- ✅ AFTER: `entrypoint.sh` handles everything in right order

---

## Comparison: Old vs New

### OLD (Broken)
```dockerfile
WORKDIR /app
COPY . .
RUN python cinemania/manage.py collectstatic --noinput
RUN python cinemania/manage.py migrate
CMD gunicorn --bind 0.0.0.0:8000 cinemania.wsgi:application
# ❌ Python can't find cinemania module
```

### NEW (Fixed)
```dockerfile
WORKDIR /app
COPY . .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
# ✅ entrypoint.sh handles everything correctly
```

---

## Runtime Flow

```
Request to Application
│
├─ Browser sends HTTP request
│
├─ Nginx/Gunicorn receives request
│
├─ Gunicorn loads cinemania.wsgi:application
│
├─ Django processes request
│  ├─ Loads settings from DJANGO_SETTINGS_MODULE
│  ├─ Uses environment variables for config
│  └─ Handles static files via WhiteNoise
│
└─ Response sent back to browser
```

---

## Key Insights

1. **entrypoint.sh is Critical**
   - Handles directory changes
   - Ensures migrations run
   - Prepares static files
   - Starts application correctly

2. **Working Directory Matters**
   - Docker WORKDIR must be correct
   - Python import paths are relative to WORKDIR
   - Gunicorn needs proper setup

3. **Environment Variables**
   - Passed from Render dashboard
   - Used by settings.py via python-decouple
   - Enable production configuration

4. **Static Files**
   - Collected during startup
   - Served through WhiteNoise
   - Must be in STATIC_ROOT

---

## Deployment Timeline

```
You: Push to GitHub
│
├─ GitHub Webhook triggers Render
│
├─ Render: Clone Repository
│
├─ Render: Build Docker Image
│  └─ Runs: docker build -t cinemania .
│
├─ Render: Push Image to Registry
│
├─ Render: Start Container
│  └─ Runs: entrypoint.sh
│     ├─ Migrations run
│     ├─ Static files collected
│     └─ Gunicorn starts
│
├─ Render: Health Check
│
└─ Your App: LIVE! 🚀
   Accessible at: https://your-app.onrender.com
```

---

## Testing Locally

```bash
# Build
docker build -t cinemania .

# Run
docker run -p 8000:8000 \
  -e SECRET_KEY='test' \
  -e DEBUG='False' \
  -e ALLOWED_HOSTS='localhost' \
  cinemania

# entrypoint.sh runs:
# 1. Migrations
# 2. Static file collection
# 3. Gunicorn startup

# Test: http://localhost:8000
```

---

## Success Indicators

When everything works:
- ✅ Docker builds without errors
- ✅ No "ModuleNotFoundError" messages
- ✅ CSS/JS files load (no 404s)
- ✅ Database migrations complete
- ✅ App responds to HTTP requests
- ✅ Render dashboard shows "Live"

---

## Troubleshooting Quick Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: cinemania.wsgi` | Working directory issue | Check entrypoint.sh paths |
| `Static files not loading` | collectstatic didn't run | Check Render logs for errors |
| `500 Internal Server Error` | Settings misconfigured | Verify environment variables |
| `Connection refused` | Port not exposed | Check Dockerfile EXPOSE |
| `Migrations failed` | Database issue | Check database configuration |

---

## Architecture Summary

```
┌─────────────────────────────────────────────┐
│  Render Platform                            │
│  ┌────────────────────────────────────────┐ │
│  │ Docker Container                       │ │
│  │ ┌──────────────────────────────────┐   │ │
│  │ │ Python 3.12 Environment          │   │ │
│  │ │ WORKDIR=/app                     │   │ │
│  │ ├──────────────────────────────────┤   │ │
│  │ │ entrypoint.sh (THE FIX)          │   │ │
│  │ │ ├─ cd cinemania/                 │   │ │
│  │ │ ├─ migrate                       │   │ │
│  │ │ ├─ collectstatic                 │   │ │
│  │ │ └─ gunicorn                      │   │ │
│  │ ├──────────────────────────────────┤   │ │
│  │ │ Gunicorn Server                  │   │ │
│  │ │ ├─ Loads: cinemania.wsgi         │   │ │
│  │ │ └─ Listens on 0.0.0.0:PORT       │   │ │
│  │ ├──────────────────────────────────┤   │ │
│  │ │ Django Application               │   │ │
│  │ │ ├─ settings.py                   │   │ │
│  │ │ ├─ cinemania/wsgi.py             │   │ │
│  │ │ └─ movies/ app                   │   │ │
│  │ └──────────────────────────────────┘   │ │
│  └────────────────────────────────────────┘ │
│                                             │
│  Environment Variables (from dashboard)    │
│  ├─ SECRET_KEY                             │
│  ├─ DEBUG=False                            │
│  ├─ ALLOWED_HOSTS                          │
│  └─ TMDB_API_KEY                           │
└─────────────────────────────────────────────┘
```

---

This architecture ensures your Django application is properly containerized and can run on Render's free tier! 🚀

# How to Start Scanofinder

## Quick Start

### 1. Activate Virtual Environment (if using one)
```bash
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies (if not already installed)
```bash
pip install -r requirements.txt
```

### 3. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Start the Server
```bash
python manage.py runserver
```

### 5. Access the Application
- **Frontend (AngularJS)**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Endpoints**: http://localhost:8000/api/

## Important Notes

- **Single Server**: Django serves both the backend API and the AngularJS frontend
- **No Separate Frontend Server**: The AngularJS app is served as static files through Django
- **Development Mode**: The server runs on port 8000 by default
- **Auto-reload**: Django automatically reloads when you make code changes

## Troubleshooting

### If you get "ModuleNotFoundError"
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### If you get database errors
Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### If static files don't load
Collect static files:
```bash
python manage.py collectstatic --noinput
```

## Production Deployment

For production, you'll need:
1. A production web server (like Gunicorn + Nginx)
2. A production database (PostgreSQL recommended)
3. Proper static file serving
4. Environment variables configured


Deploying to Render
===================

This guide explains how to deploy the project to Render (https://render.com) using the included Dockerfile and render.yaml manifest.

Steps:

1. Push your repository to GitHub (or another Git provider supported by Render) and ensure the `main` branch is up to date.

2. In the Render dashboard, create a new "Web Service" and connect your repository.
   - If Render detects `render.yaml` it will use the settings there. The manifest points to the `Dockerfile` and will deploy the service on the `main` branch.

3. Environment variables (minimum recommended):
   - FLASK_ENV = production
   - DATABASE_URL = your PostgreSQL connection string (for example: postgres://user:pass@host:5432/dbname)
   - JWT_SECRET_KEY = a secure random string used by Flask-JWT-Extended
   - PORT = Render sets this automatically at runtime; the container will use that value

4. Render will build the Docker image using the `Dockerfile`. The container runs Gunicorn with the WSGI app specified in `app/wsgi.py`.

Local testing tips:

Build locally using Docker:

    docker build -t sacco-backend:local .
    docker run -e PORT=5000 -p 5000:5000 sacco-backend:local

Or run the app with Gunicorn locally (after installing dependencies):

    pip install -r requirements.txt
    gunicorn app.wsgi:app --bind 0.0.0.0:5000

Notes & troubleshooting:

- If you prefer not to use Docker, you can create a Render service with Environment = Python and set the Start Command to:

    gunicorn app.wsgi:app --bind 0.0.0.0:$PORT --workers 3

- Make sure `requirements.txt` contains all production dependencies. The project already includes `gunicorn`.
- Ensure any secrets are configured in the Render service's Environment Variables (do not commit secrets to git).

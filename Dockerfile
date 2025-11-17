FROM python:3.10-slim

# System deps and non-interactive settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build deps first (kept minimal)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app source
COPY . /app

# Runtime port provided by Render in $PORT
ENV PORT 10000

# Use a shell form so $PORT is expanded at runtime
CMD ["/bin/sh", "-lc", "gunicorn app.wsgi:app --bind 0.0.0.0:$PORT --workers 3"]

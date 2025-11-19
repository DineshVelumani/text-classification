FROM python:3.10-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps required by some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r /app/requirements.txt \
    && pip install gunicorn

# Copy application files
COPY . /app

# Vercel will set the PORT environment variable at runtime; default to 5000
ENV PORT=5000

EXPOSE 5000

# Use gunicorn to run the Flask app; fallback to 5000 if PORT not set
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 1 --threads 4 --timeout 120"]

# Use Python 3.11 slim image as base
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        postgresql-client \
        gettext \
        curl \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Create non-root user
RUN addgroup --system django \
    && adduser --system --ingroup django django

# Copy project files
COPY . .

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media \
    && chown -R django:django /app

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "hitech_store.wsgi:application"]

# Multi-stage build for production
FROM base as production

# Copy entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch back to root to set permissions
USER root
RUN chown django:django /entrypoint.sh

# Switch back to django user
USER django

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "hitech_store.wsgi:application"]

# Development stage
FROM base as development

# Install development dependencies
USER root
RUN pip install watchdog[watchmedo]

# Switch back to django user
USER django

# Override command for development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
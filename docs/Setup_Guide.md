# Setup Guide

This guide walks you through preparing a local development environment for Numerologist and explains how to configure the project for staging or production deployments.

## 1. Prerequisites

Before you begin, make sure the following tools are installed:

- **Python 3.11 or newer**
- **pip** for managing Python packages
- **virtualenv** (optional, but recommended)
- **Git**
- A supported database engine: SQLite (default), PostgreSQL, or MySQL
- (Optional) **Node.js** if you plan to extend the frontend with a JavaScript build pipeline in the future

## 2. Clone the repository

```bash
git clone https://github.com/XS227/Numerologist.git
cd Numerologist
```

If you are contributing to a fork, clone your fork instead and add the upstream remote afterwards.

## 3. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate          # Windows PowerShell
```

Keep the virtual environment activated while you install dependencies and run the project. To leave the environment at any time, run `deactivate`.

## 4. Install Python dependencies

Install all required packages from `requirements.txt`.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If your network blocks outbound traffic to PyPI, download the wheels on a separate machine and install them locally with `pip install --no-index --find-links <path-to-wheels> -r requirements.txt`.

## 5. Configure environment variables

Copy the example environment configuration and adjust it for your setup (create the file if it does not yet exist):

```bash
cp .env.example .env  # (if the example file is available)
```

Set the following variables either in `.env` or in your shell session:

| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | `dev-change-me` | Secret key for cryptographic signing. Always override in production. |
| `DEBUG` | `False` | Set to `True` during development for verbose error pages. |
| `ALLOWED_HOSTS` | `numerologist.setaei.com,localhost,127.0.0.1` | Comma-separated list of hosts allowed to access the site. |
| `DATABASE_URL` | *(empty)* | Optional database connection string. Leave empty to use SQLite. |

When `DATABASE_URL` is provided, the settings module automatically selects PostgreSQL (`postgres://` or `postgresql://`) or MySQL (`mysql://`). Any other value falls back to SQLite.

## 6. Apply database migrations

Numerologist currently relies on Django built-ins and the intake app, which use Django's default migrations. Apply them after configuring the database.

```bash
python manage.py migrate
```

If you plan to access the admin or Wagtail CMS, create a superuser:

```bash
python manage.py createsuperuser
```

## 7. Run the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ to access the marketing landing page with the lightweight calculator. The intake form lives at http://127.0.0.1:8000/intake/.

## 8. Collect static files (production/staging)

When preparing a deployment on a platform such as a VPS or PaaS, run:

```bash
python manage.py collectstatic --no-input
```

Static assets are collected into the `static_collected` directory and served by WhiteNoise.

## 9. Running tests

```bash
python manage.py test
```

Add tests to `intake/tests/` or new Django apps to ensure numerology calculations remain accurate.

## 10. Deployment checklist

- Disable `DEBUG`.
- Set a strong `DJANGO_SECRET_KEY`.
- Configure `ALLOWED_HOSTS` for your domain(s).
- Point `DATABASE_URL` to a managed PostgreSQL or MySQL instance, or ensure file permissions for SQLite.
- Use HTTPS and configure CSRF trusted origins (`CSRF_TRUSTED_ORIGINS`) for the production domain.
- Enable a process manager (systemd, supervisor, Gunicorn + nginx, Passenger) depending on your hosting provider.

You now have a working environment ready to extend the Numerologist platform.

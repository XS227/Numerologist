# Architecture Overview

Numerologist is built on Django with an additional Wagtail CMS layer for content management. The project follows a modular structure that separates the marketing site, practitioner intake workflow, and reusable numerology engine helpers.

```
Numerologist/
├── manage.py
├── requirements.txt
├── tall_project/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── forms.py
│   └── templates/
│       └── pages/home.html
├── intake/
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── constants.py
│   └── templates/intake/intake_form.html
└── docs/
```

## Key Components

### Django Project (`tall_project`)
- **`settings.py`**: Configures Django, Wagtail, and Django REST Framework. Supports SQLite by default with optional PostgreSQL/MySQL via `DATABASE_URL`.
- **`urls.py`**: Routes requests to the marketing site, intake app, Wagtail admin, Django admin, and a `/healthz/` endpoint.
- **`views.py`**: Defines the `home` view that renders the lightweight calculator.
- **`forms.py`**: Contains `LiteCalculatorForm`, a condensed interface that reuses numerology helpers to compute life path, expression, and soul urge numbers.
- **Templates**: The marketing page lives in `tall_project/templates/pages/home.html` and leverages Tailwind-esque utility classes.

### Intake App (`intake`)
- **`forms.py`**: Implements the full numerology engine (`IntakeForm`) and helper methods for digit reduction. Provides `NumerologyResult` for structured data access.
- **`views.py`**: Handles the practitioner intake workflow. Accepts form submissions, calculates numbers, and renders output with explanations from `INTAKE_EXPLANATIONS`.
- **`constants.py`**: Holds descriptive text for each numerology number.
- **Templates**: `intake/templates/intake/intake_form.html` renders the practitioner interface and displays computed results.
- **`tests/`**: Placeholder for unit tests that validate numerology calculations and form behaviour.

### Content Management

Wagtail is installed for future content authoring. The CMS admin lives under `/cms/` and can be used to create landing pages, blog posts, or resource hubs without touching code. Static assets are served with WhiteNoise, simplifying deployment to environments like Passenger or Gunicorn.

## Data Flow

1. A visitor submits either the marketing calculator or the intake form.
2. The corresponding Django form validates input, normalises names, and calls helper methods.
3. Calculated numbers are packaged into dictionaries (or `NumerologyResult`) and passed to templates.
4. Templates render the results with interpretations from `constants.py`.

## Deployment Considerations

- **Static files**: `collectstatic` gathers assets into `static_collected/` for WhiteNoise.
- **Environment variables**: `.env` should supply secrets, database URLs, and debug flags.
- **Process management**: The repository includes `passenger_wsgi.py` for Passenger-based deployments; alternatively use Gunicorn + systemd.
- **Health checks**: `/healthz/` returns `OK` for uptime monitoring.

## Future Enhancements

- Add dedicated Django apps for API endpoints (`api/`) and CMS-driven pages.
- Introduce Celery for asynchronous report generation.
- Persist intake submissions in the database and expose them via dashboards or exports.
- Layer a React or HTMX front-end for richer interactivity while keeping Django as the backend.

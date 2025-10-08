# API Reference

Numerologist currently exposes a minimal set of HTTP endpoints designed for form-based interactions and operational monitoring. This document lists the available routes, expected payloads, and response formats. Future releases will extend these endpoints with a formal JSON API using Django REST Framework.

## Base URLs

- **Marketing site / lightweight calculator**: `https://numerologist.setaei.com/`
- **Intake form**: `https://numerologist.setaei.com/intake/`

During local development the application runs at `http://127.0.0.1:8000/` by default.

## Public Endpoints

### `GET /`
Renders the marketing landing page along with the lightweight numerology calculator.

- **Response**: HTML (`pages/home.html`)
- **Form fields**:
  - `full_name` *(string, required)*
  - `birth_date` *(date, required, ISO-8601)*
- **POST behaviour**: Submitting the form returns the same template with a `result` context containing `life_path`, `expression`, and `soul_urge` numbers. All calculations reuse the helpers defined in `IntakeForm`.

### `GET /intake/`
Displays the practitioner intake workflow.

- **Response**: HTML (`intake/intake_form.html`)
- **Form fields**:
  - `full_name` *(string, required)*
  - `email` *(email, required)*
  - `birth_date` *(date, required)*
  - `focus_area` *(string, optional)*
  - `notes` *(string, optional)*
- **POST behaviour**: Returns the same template with a `result` context. The context includes:
  - `numbers`: list of calculated numerology numbers with labels and descriptions (`life_path`, `expression`, `soul_urge`, `personality`, `birth_day`, `maturity`).
  - `focus_area`, `notes`, `full_name`, `email`, `birth_date` (echoed back for practitioner convenience).

### `GET /healthz/`
Simple health check endpoint useful for uptime monitoring and load balancer probes.

- **Response**: Plain text `OK` with HTTP status 200.

## Administrative Endpoints

| Endpoint | Description | Notes |
| --- | --- | --- |
| `GET /admin/` | Django admin interface. | Requires staff credentials. |
| `GET /cms/` | Wagtail admin dashboard. | Requires Wagtail login. |
| `GET /documents/` | Wagtail document management. | Requires Wagtail login. |

These routes are protected by Django's authentication system. Use `python manage.py createsuperuser` to create an initial administrator account in development.

## Planned JSON API

The project already depends on Django REST Framework (`rest_framework`) but does not expose public JSON endpoints yet. When introducing the API, follow these guidelines:

1. Serialise `NumerologyResult` outputs to JSON for programmatic access.
2. Provide endpoint versioning (e.g., `/api/v1/`) to allow iterative changes.
3. Document authentication requirements (token or session-based) before exposing client integrations.
4. Add automated tests for each endpoint in `intake/tests/` or a dedicated `api` app.

## Error Handling

Form submissions leverage Django's built-in form validation. If a field is missing or invalid, the response re-renders the template with inline error messages. JSON APIs should adopt a structured error format once implemented (e.g., `{ "detail": "Invalid birth date." }`).

## Rate Limiting & Security

- Enable HTTPS in production to protect personal information.
- Use `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` to prevent host header attacks.
- When exposing JSON APIs, add throttling via Django REST Framework's throttling classes or a gateway proxy (NGINX, Cloudflare, etc.).

# Project Context

## Purpose
Itzimna Dashboard is a property management and content administration system for a real estate platform. It serves as a backend providing a REST API for property searches, blog content, and lead management, while offering a customized admin interface for content managers.

## Tech Stack
- **Backend**: Python 3.12, Django 4.2.7
- **API**: Django REST Framework (DRF) 3.15, Simple JWT 5.4
- **Database**: PostgreSQL (psycopg 3.2), MySQL (optional), SQLite (test)
- **Storage**: AWS S3 (django-storages, boto3)
- **Static Files**: WhiteNoise 6.2
- **Web Server**: Gunicorn 20.1
- **Deployment**: Docker, Caprover
- **Admin UI**: Jazzmin (Admin skin)
- **Libraries**: Pillow (Image processing), Selenium (Testing), python-slugify, python-dotenv

## Project Conventions

### Code Style
- **Python**: Follow PEP 8 guidelines.
- **Naming**: `snake_case` for variables/functions, `PascalCase` for classes.
- **Docstrings**: Use descriptive docstrings for methods, specifying Args and Returns (especially in API views and serializers).
- **L10N**: Preference for Spanish (ES-MX) defaults with multi-language support (ES/EN).

### Architecture Patterns
- **Standard Django Apps**: Logic organized into modules (`properties`, `blog`, `leads`, `translations`, `core`).
- **Base Serializers**: Use `BaseModelTranslationsSerializer` or `BaseSearchSerializer` for consistent multi-language response handling.
- **Standardized API Responses**: All API responses follow a `{ "status": "ok|error", "message": "...", "data": {...} }` structure, managed via `custom_exception_handler`.
- **Environment Management**: Configuration driven by `.env.{ENV}` files (dev, prod).

### Testing Strategy
- **Framework**: Django TestCase (unittest).
- **Isolation**: Uses SQLite for testing (`IS_TESTING` flag in settings).
- **E2E/Browser**: Selenium for automated browser testing.
- **Automation**: Support for headless testing (`TEST_HEADLESS`).

### Git Workflow
- **Branching**: standard `main` (production), `develop` (staging/dev), and feature/fix branches.
- **Commits**: Clear, descriptive commit messages in English or Spanish.

## Domain Context
- **Entities**: Properties, Companies (Developers/Agencies), Locations, Sellers, Categories, and Tags.
- **Translations**: Core feature; many models link to a `Translation` model or have explicit `_es`/`_en` fields.
- **SEO**: Focus on slug generation, alt text for images, and structured metadata.

## Important Constraints
- **Versioning**: Python 3.12 and Django 4.2.x are strictly required.
- **Security**: Must maintain strict CORS and CSRF configurations in production.
- **Storage**: Media must be handled via the specified storage backend (AWS S3 in production).

## External Dependencies
- **AWS S3**: Primary media and static file host in production.
- **Google Maps**: Used for embedding property locations.
- **WhatsApp**: Integration for seller contact links.
- **SMTP**: Used for sending lead notification emails.

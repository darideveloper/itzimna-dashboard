# Proposal: Update Media Files Storage System

## Summary
Update the current AWS S3 integration to fully support both AWS S3 and DigitalOcean Spaces for static files, public media, and private media. This change relies on adjusting the Django settings and `storage_backends.py` configurations according to the newly defined standard (`docs/media-file-storage.md`).

## Motivation
The current implementation hardcodes bucket structure values (e.g., `'static'`, `'media'`, `'private'`) and lacks configuration options for regional and custom domain parameters, limiting flexibility and the potential to use alternative providers like DigitalOcean Spaces. Additionally, multiple projects or environments cannot safely share the same bucket without folder isolation mapping, which the new standard provides via `AWS_PROJECT_FOLDER`.

## Goals
- Allow using either AWS S3 or DigitalOcean Spaces based on environment variable inputs.
- Introduce `AWS_PROJECT_FOLDER` to isolate storage items from other environments/projects sharing the same bucket.
- Properly map region, endpoint, and custom domains (CDN).
- Upgrade underlying storage dependencies (`django-storages` and `boto3`) to correctly support the updated standards.

## Affected Areas
- `requirements.txt`: Bumping library versions.
- `project/storage_backends.py`: Replacing hardcoded paths with environment-driven variables.
- `project/settings.py`: Refactoring the `STORAGE_AWS` block.
- Environment templates (`.env.dev`): Adding new mapping keys (`AWS_S3_ENDPOINT_URL`, etc.).

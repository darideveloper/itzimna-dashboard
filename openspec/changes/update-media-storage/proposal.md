# Proposal: Update Media Files Storage System

## Summary
Update the current AWS S3 integration to fully support both AWS S3 and DigitalOcean Spaces for static files, public media, and private media. This change relies on adjusting the Django settings and `storage_backends.py` configurations according to the newly defined standard (`docs/media-file-storage.md`).

## Why
The current implementation hardcodes bucket structure values (e.g., 'static', 'media', 'private') and lacks configuration options for regional and custom domain parameters, limiting flexibility and the potential to use alternative providers like DigitalOcean Spaces. Additionally, multiple projects or environments cannot safely share the same bucket without folder isolation mapping, which the new standard provides via AWS_PROJECT_FOLDER.

## What Changes
- Refactor classes in `project/storage_backends.py` to use dynamic locations from settings.
- Update the `STORAGE_AWS` configuration block in `project/settings.py` to support endpoints, regions, and custom domains.
- Add `AWS_PROJECT_FOLDER` for bucket level isolation.
- Upgrade `django-storages` to `1.14.4` and `boto3` to `1.34.162` in `requirements.txt`.

## Impact
- Affected specs: `aws-do-spaces-integration`
- Affected code: `project/settings.py`, `project/storage_backends.py`, `requirements.txt`, `.env.dev`

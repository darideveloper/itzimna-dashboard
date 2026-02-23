## ADDED Requirements

#### Scenario: Update Cloud Storage Support configuration
- **Scenario:** The backend requires configuring a flexible file storage mechanism to support isolation and custom domains.
- **Given** the environment variables enable AWS/DO spaces configuration
- **When** Django initializes `settings.py` and `storage_backends.py`
- **Then** the `STORAGE_AWS` block correctly grabs new env settings and propagates them into location classes.

### Code implementations required

#### 1. Modify `requirements.txt`
Update dependencies for exact matches specified in documentation.
```text
django-storages==1.14.4
boto3==1.34.162
```

#### 2. Modify `project/storage_backends.py`
Replace hardcoded strings with values passed down from `django.conf.settings` and add `custom_domain=False` constraint to `PrivateMediaStorage` for bypassing CDN signed URLs.
```python
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.STATIC_LOCATION
    default_acl = "public-read"

class PublicMediaStorage(S3Boto3Storage):
    location = settings.PUBLIC_MEDIA_LOCATION
    default_acl = "public-read"
    file_overwrite = False

class PrivateMediaStorage(S3Boto3Storage):
    location = settings.PRIVATE_MEDIA_LOCATION
    default_acl = "private"
    file_overwrite = False
    custom_domain = False
```

#### 3. Modify `project/settings.py`
Rewrite the entire `if STORAGE_AWS` block. Include regional settings, domain settings, and project folder grouping.
```python
if STORAGE_AWS:
    # 1. Credentials
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

    # 2. Regional Settings
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")

    # 3. Domain/CDN settings
    AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN")

    # 4. Folder isolation
    AWS_PROJECT_FOLDER = os.getenv("AWS_PROJECT_FOLDER", "")

    # 5. File Locations
    STATIC_LOCATION = f"{AWS_PROJECT_FOLDER}/static" if AWS_PROJECT_FOLDER else "static"
    PUBLIC_MEDIA_LOCATION = f"{AWS_PROJECT_FOLDER}/media" if AWS_PROJECT_FOLDER else "media"
    PRIVATE_MEDIA_LOCATION = f"{AWS_PROJECT_FOLDER}/private" if AWS_PROJECT_FOLDER else "private"

    # 6. Django-Storages Engine Mapping
    STATICFILES_STORAGE = "project.storage_backends.StaticStorage"
    DEFAULT_FILE_STORAGE = "project.storage_backends.PublicMediaStorage"
    PRIVATE_FILE_STORAGE = "project.storage_backends.PrivateMediaStorage"

    # 7. Optimization & Security
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_DEFAULT_ACL = None

    STATIC_ROOT = None
    MEDIA_ROOT = None
```

#### 4. Update `.env.dev`
Add newly required default variables for development debugging.
```ini
AWS_PROJECT_FOLDER=itzimna-dashboard-dev
AWS_S3_REGION_NAME=
AWS_S3_ENDPOINT_URL=
AWS_S3_CUSTOM_DOMAIN=
```

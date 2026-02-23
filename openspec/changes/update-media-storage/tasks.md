## Updating Storage Backend Support

- [x] Update `django-storages` to `1.14.4` and `boto3` to `1.34.162` in `requirements.txt`.
- [x] Refactor classes in `project/storage_backends.py` to use `settings.STATIC_LOCATION`, `settings.PUBLIC_MEDIA_LOCATION`, `settings.PRIVATE_MEDIA_LOCATION` instead of hardcoded strings, and explicitly disable `custom_domain` for `PrivateMediaStorage` class.
- [x] Refactor the `STORAGE_AWS` configuration block in `project/settings.py` to enable endpoint and customizable region logic, referencing `AWS_PROJECT_FOLDER` to configure static, public, and private locations respectively.
- [x] Add `AWS_PROJECT_FOLDER`, `AWS_S3_REGION_NAME`, `AWS_S3_ENDPOINT_URL`, and `AWS_S3_CUSTOM_DOMAIN` keys to `.env.dev`.
- [x] Run `openspec validate update-media-storage` safely via CLI if any structural issues are suspected.

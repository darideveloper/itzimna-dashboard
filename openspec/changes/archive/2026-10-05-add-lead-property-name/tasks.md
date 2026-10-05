## 1. Data Model & Migrations

- [x] 1.1 Convert `property` field on `Lead` model in `leads/models.py` from `ForeignKey(Property)` to `models.CharField(max_length=200, blank=True, default="", verbose_name="Propiedad")` and verify syntax with `python manage.py check`.
- [x] 1.2 Create and apply database migration `leads/migrations/0007_alter_lead_property.py` using `python manage.py makemigrations leads` and `python manage.py migrate leads`, verifying column type altered in database.

## 2. Admin & Notifications

- [x] 2.1 Update `send_notification_email` method in `leads/models.py` to append `Propiedad: {self.property}` when `self.property` is populated, and verify email message construction.
- [x] 2.2 Verify `property` is included in `list_display` and added to `search_fields` in `leads/admin.py`, and verify Django Admin renders the text property column.

## 3. Verification & Tests

- [x] 3.1 Update unit tests in `leads/tests/test_models.py` and `leads/tests/test_views.py` to test string `property` persistence and API serialization.
- [x] 3.2 Verify API lead creation with property text: POST a payload containing `"property": "Palta 152"` to `/api/leads/` and verify HTTP 201 status and correct database persistence.
- [x] 3.3 Verify backward compatibility: POST a payload omitting `property` (or empty string) to `/api/leads/` and verify HTTP 201 status and default empty string persistence.
- [x] 3.4 Verify automated email notification delivery via configured SMTP/Mailpit server.

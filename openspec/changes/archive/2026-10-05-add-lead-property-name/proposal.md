## Why

Currently, when visitors submit inquiries through the website contact form, the lead is stored in the database without capturing which real estate property the customer is interested in. Although a `property` field already existed on the `Lead` model, it was defined as a relational `ForeignKey(Property)` meant for manual admin assignment, which prevented public inquiry forms from saving free-text property names. To directly record the customer's property of interest from contact forms, the existing `property` field must be converted to a text field and populated with the submitted form data.

## What Changes

- Convert the existing `property` field on the `Lead` model from `models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)` to `models.CharField(max_length=200, blank=True, default="", verbose_name="Propiedad")`.
- Update `send_notification_email` on the `Lead` model to include `Propiedad: {self.property}` in automated notification emails sent to administrators when present.
- Ensure `LeadAdmin` in `leads/admin.py` displays the text `property` in `list_display` and enables filtering/searching by `property` in `search_fields`.
- Generate and apply database migration `0007_alter_lead_property.py`.
- Update test cases in `leads/tests/test_views.py` and `leads/tests/test_models.py` to validate string-based property submissions.

## Capabilities

### New Capabilities
- `lead-property-tracking`: Capturing and displaying the free-text property of interest submitted with incoming leads in the dashboard and email alerts.

### Modified Capabilities
<!-- No existing capabilities under openspec/specs/ are being modified -->

## Impact

- Affected models: `leads.models.Lead` (`property` field altered from ForeignKey to CharField).
- Affected admin: `leads.admin.LeadAdmin` (`search_fields` includes `property`).
- Affected notification: `leads.models.Lead.send_notification_email`.
- Affected migrations: `leads/migrations/0007_alter_lead_property.py`.
- APIs: `POST /api/leads/` accepts `property` as a string without foreign key validation constraints.

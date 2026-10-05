## Context

The backend is built with Django and Django REST Framework. Incoming customer inquiries are received at `POST /api/leads/` and mapped to `leads.models.Lead`. Previously, `Lead` had a `property` field defined as `ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)`. Public inquiry forms on the frontend submit free-text describing properties (e.g., "Palta 152"), which could not be saved to a relational `ForeignKey` column without raising deserialization or validation errors.

The client requirement states: "The field already exist in the lead model, but its related to the properties table, instead, should be converted to a text and filled with the form data".

See `proposal.md` for background motivation and `specs/lead-property-tracking/spec.md` for behavioral requirements.

## Goals / Non-Goals

**Goals:**
- Convert the existing `property` field on `Lead` from a `ForeignKey(Property)` to a `CharField` storing free text.
- Ensure DRF endpoint `POST /api/leads/` validates and persists string-based `property` values from API payloads.
- Preserve `property` in Django Admin's `list_display` and add `property` to `search_fields`.
- Include the property text in automated notification emails sent to administrators (`send_notification_email`).
- Maintain backward compatibility for submissions that omit the property field by setting `blank=True, default=""`.
- Provide a clean database migration altering the existing column.

**Non-Goals:**
- Adding a separate second field (e.g. `property_name`) alongside `property` (rejected per explicit client requirement).
- Implementing dropdown or selection catalogs in the public inquiry form (inquiries are free-text).
- Modifying core execution flow or wrapping core methods in custom try/except blocks in `leads/models.py`.
- Modifying lead status workflows or unrelated applications.

## Decisions

### Decision 1: Convert `property` from ForeignKey to CharField
- **Decision**: Alter `property = models.CharField(max_length=200, blank=True, default="", verbose_name="Propiedad")` on `Lead`.
- **Rationale**: Directly aligns with client directive to convert the existing field rather than adding an extra column. Leads represent incoming prospective customer inquiries where the property is often entered as arbitrary free text before any formal catalog property is assigned.
- **Alternatives considered**:
  - *Add a separate `property_name` CharField*: Initial approach; rejected by the client because they specifically instructed converting the existing `property` field to text.
  - *Automatic fuzzy lookup to resolve ForeignKey*: Rejected because prospective inquiries often describe properties in ways that cannot be reliably matched automatically, and creating fake catalog records would pollute the catalog.

### Decision 2: Text field attributes (`blank=True, default=""`)
- **Decision**: Use `blank=True, default=""` for the `property` CharField.
- **Rationale**: Conforms to standard Django conventions for string-based fields, preventing duplicate null vs. empty states and ensuring backward compatibility. Inquiries submitted without specifying a property cleanly default to `""`.
- **Alternatives considered**: `null=True, blank=True` (anti-pattern in Django for CharField).

### Decision 3: Admin visibility and search integration
- **Decision**: Keep `property` in `list_display` and add `property` to `search_fields` in `leads/admin.py`.
- **Rationale**: Administrators immediately see the property name in the leads table without opening detail pages, and can quickly search leads by property text.

### Decision 4: Email notification integration
- **Decision**: Update `send_notification_email` to append `Propiedad: {self.property}` to the notification email body whenever `self.property` is truthy.
- **Rationale**: Ensures administrators receive the property details immediately via email alerts upon inquiry submission.

## Risks / Trade-offs

- **[Trade-off] Loss of relational integrity to `Property` model** → *Mitigation*: Accepted per client requirement. Lead records represent incoming contacts/inquiries rather than normalized catalog entities.
- **[Risk] Existing callers omit `property`** → *Mitigation*: The field has `default=""` and `blank=True`; omitting it in API payloads or admin forms remains completely valid.

## Migration Plan

1. Generate and apply migration: `leads/migrations/0007_alter_lead_property.py` altering the column from `bigint` (foreign key) to `varchar(200)`.
2. Verification: Verify existing lead records load without errors and create new leads via API and Django Admin.

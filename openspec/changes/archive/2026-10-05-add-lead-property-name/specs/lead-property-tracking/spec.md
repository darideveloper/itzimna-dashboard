## Purpose

Provides tracking and administrative visibility for real estate properties of interest specified by users during lead submission.

## ADDED Requirements

### Requirement: Ingestion of Property of Interest via API
The system SHALL accept an optional `property` free-text field in lead creation requests (`POST /api/leads/`) and store it directly in the `property` field of the lead record while maintaining full backward compatibility.

#### Scenario: Lead submitted with property name
- **WHEN** an API client sends a `POST` request to `/api/leads/` with valid contact fields and a `property` string (e.g., `"Palta 152"`)
- **THEN** the system creates the lead record, persists the submitted text in `property`, and responds with HTTP 201 Created

#### Scenario: Lead submitted without property name
- **WHEN** an API client sends a `POST` request to `/api/leads/` omitting `property` or passing an empty string
- **THEN** the system creates the lead record with an empty string as default and responds with HTTP 201 Created

### Requirement: Administrative Display and Search
The Django Admin interface SHALL display the submitted `property` text in the leads list table and enable administrators to search leads by requested property name.

#### Scenario: Admin views leads list
- **WHEN** an administrator navigates to the Leads section in the Django Admin dashboard
- **THEN** the table view displays the "Propiedad" column showing the requested property text for each lead

#### Scenario: Admin searches leads by property name
- **WHEN** an administrator enters a search query matching a lead's `property` in the Django Admin search box
- **THEN** the system returns matching lead records in the results

### Requirement: Notification Email Inclusion
The system SHALL include the requested property name in automated email alerts sent to administrators upon lead creation.

#### Scenario: Notification email with property of interest
- **WHEN** a new lead record is created with a non-empty `property`
- **THEN** the outgoing notification email sent to configured recipient addresses explicitly includes `Propiedad: {property}`

#### Scenario: Notification email without property of interest
- **WHEN** a new lead record is created with an empty `property`
- **THEN** the outgoing notification email is sent successfully without the property line and without formatting errors

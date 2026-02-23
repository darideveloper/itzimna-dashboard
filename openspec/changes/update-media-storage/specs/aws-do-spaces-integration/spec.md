## ADDED Requirements

### Requirement: Cloud Storage Configuration
The system SHALL support configurable cloud storage backends (AWS S3 or DigitalOcean Spaces) using environment variables for endpoints, regions, and project folders.

#### Scenario: Backend initialization with cloud storage
- **GIVEN** the `STORAGE_AWS` environment variable is enabled
- **WHEN** the Django application initializes
- **THEN** it SHALL load storage settings from environment variables including project folder isolation and custom domains

### Requirement: Project Folder Isolation
The system SHALL use a project-specific folder in the cloud storage bucket to isolate files from other projects.

#### Scenario: Storage location with project folder
- **GIVEN** `AWS_PROJECT_FOLDER` is set in environment variables
- **WHEN** files are uploaded or accessed
- **THEN** they SHALL be stored within the specified project folder

### Requirement: Private Media Storage
The system SHALL support private media storage that bypasses custom CDN domains for secure access.

#### Scenario: Private media access
- **GIVEN** a `PrivateMediaStorage` backend is configured
- **WHEN** a private file is accessed
- **THEN** it SHALL use the default provider domain instead of a custom domain to ensure signed URL validity

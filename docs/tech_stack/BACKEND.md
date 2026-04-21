# Backend

## Source Code Folder (`backend/app/`)

### `api/`
**Route Handlers.**
- **Purpose:** Defines API endpoints and handles HTTP status codes.

### `core/`
**Configuration & Security.**
- **Purpose:** Centralizes app-wide settings, authentication logic, and environment variables.

### `services/`
**Business Logic.**
- **Purpose:** Contains the core functional logic of the application, API routes should call services / services should never know they are being called by an API.

### `models/`
- **Data Modeling.**
- **Purpose:** Pydantic models for request validation and response serialization.

### `schemas/`
**Data Modeling.**
- **Purpose:** Definitions for database tables and relations.

### `storage/`
**Data Access Layer.**
- **Purpose:** Manages database connections and utility clients (e.g., Supabase client).

### `tests/`
**Quality Assurance.**
- **Purpose:** Tests for API endpoints / backend functionality.

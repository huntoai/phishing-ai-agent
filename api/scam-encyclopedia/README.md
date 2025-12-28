# Scam Encyclopedia API

Backend API for scam information and education.

## Endpoints (Planned)

### GET /api/encyclopedia/scams
List all scam types with pagination and filters

### GET /api/encyclopedia/scam/:id
Get detailed information about a specific scam type

### GET /api/encyclopedia/search?q=query
Search scam information

### GET /api/encyclopedia/related/:id
Get related scam types

## Implementation Notes

- Will require content management system for scam information
- Search indexing (Elasticsearch or similar)
- Regular updates from security sources
- Analytics tracking for popular searches

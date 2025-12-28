# Scam Report API

Backend API for scam reporting functionality.

## Endpoints (Planned)

### POST /api/scam-report
Submit a new scam report

### GET /api/scam-report/:id
Check the status of a submitted report

### GET /api/scam-report/guidance
Get guidance resources for different types of scams

## Implementation Notes

- Will require database for storing reports
- Email/notification system for status updates
- Integration with external scam databases
- Rate limiting to prevent spam

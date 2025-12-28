# Awareness Training API

Backend API for gamified awareness training system.

## Endpoints (Planned)

### POST /api/training/sync
Sync local storage data with backend

### GET /api/training/courses
Get available courses and modules

### POST /api/training/progress
Update user progress

### POST /api/training/subscribe
Subscribe to drip content on WhatsApp/email

### POST /api/training/complete
Mark lesson/module as complete and award points

## Implementation Notes

- Will require user session management (anonymous or authenticated)
- WhatsApp Business API integration for drip content
- Gamification engine (points, streaks, achievements)
- Content delivery scheduler

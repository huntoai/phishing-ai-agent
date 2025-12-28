# PhishGuard Website

A modern, glass morphism-designed website for phishing awareness and education built with Gatsby.

## Features

### 1. **Home Page**
- Hero section with animated elements
- Feature showcase
- Glass morphism design throughout

### 2. **Learn Page (Gamified Training)**
- Duolingo-inspired learning experience
- Streak tracking (days in a row)
- Points and levels system
- 5 courses covering:
  - Phishing Basics
  - Email Phishing
  - SMS & Smishing
  - Social Media Scams
  - Advanced Threats
- Progress tracking with local storage
- WhatsApp subscription integration (placeholder)

### 3. **Report Scam Page**
- Type-based scam categorization
- Form validation
- Report ID generation for tracking
- Post-report guidance including:
  - Next steps to protect yourself
  - Government agency links (FTC, FBI)
  - Bank and police reporting instructions

### 4. **Scam Encyclopedia**
- TLDRLegal-style clear explanations
- 6 detailed scam types:
  - Email Phishing
  - Spear Phishing
  - SMS Phishing (Smishing)
  - Voice Phishing (Vishing)
  - Whaling
  - Pharming
- Each entry includes:
  - TL;DR summary
  - How it works
  - Real-world examples
  - Red flags
  - What to do
  - Real-world impact
- Search and filter functionality

## Tech Stack

- **Framework**: Gatsby 5.x
- **Styling**: CSS Modules with glass morphism
- **Animations**: Framer Motion
- **Icons**: Emoji-based for performance
- **State Management**: Local Storage (no login required)

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
cd website
npm install
```

### Development

```bash
npm run develop
```

The site will be available at `http://localhost:8000`

### Build

```bash
npm run build
```

The static files will be in the `public/` directory.

### Serve Production Build

```bash
npm run serve
```

### Format Code

```bash
npm run format
```

## Project Structure

```
website/
├── src/
│   ├── components/
│   │   ├── elements/          # Reusable UI elements
│   │   │   ├── Button.js
│   │   │   ├── Card.js
│   │   │   ├── Input.js
│   │   │   ├── Badge.js
│   │   │   └── ProgressBar.js
│   │   └── compound/          # Complex components
│   │       ├── Navigation.js
│   │       └── Hero.js
│   ├── data/                  # Static data
│   │   ├── coursesData.js
│   │   └── scamsData.js
│   ├── pages/                 # Page components
│   │   ├── index.js          # Home
│   │   ├── learn.js          # Learning platform
│   │   ├── report.js         # Report scams
│   │   └── encyclopedia.js   # Scam encyclopedia
│   ├── styles/               # Global styles
│   │   ├── global.css
│   │   └── theme.js
│   └── utils/                # Utilities
│       └── storageManager.js # Local storage management
├── gatsby-config.js
├── gatsby-node.js
└── package.json
```

## Design System

### Colors
- Primary: `#6366f1` (Indigo)
- Secondary: `#8b5cf6` (Purple)
- Accent: `#ec4899` (Pink)
- Background: `#0f172a` (Dark blue)

### Glass Morphism
The design uses three levels of glass effects:
- **Light**: `rgba(255, 255, 255, 0.05)` with 10px blur
- **Medium**: `rgba(255, 255, 255, 0.1)` with 20px blur
- **Heavy**: `rgba(255, 255, 255, 0.15)` with 30px blur

### Components
All components are modular and reusable:
- Use CSS Modules for scoped styling
- Support variant props for different styles
- Include hover effects and animations
- Responsive by default

## Local Storage Schema

### User Progress
```javascript
{
  totalPoints: number,
  level: number,
  completedLessons: string[],
  currentCourse: string | null
}
```

### User Stats
```javascript
{
  lessonsCompleted: number,
  correctAnswers: number,
  totalAnswers: number,
  timeSpent: number,
  achievements: Array<{
    id: string,
    name: string,
    unlockedAt: string
  }>
}
```

### Streak Data
```javascript
{
  current: number,
  longest: number,
  lastDate: string
}
```

## Future Backend Integration

The site is designed to work standalone but can be enhanced with backend APIs:

### Planned Endpoints
See `/api` directory READMEs for detailed API specifications:
- `/api/scam-report` - Scam reporting and tracking
- `/api/awareness-training` - Progress sync and drip content
- `/api/scam-encyclopedia` - Scam data and search

### Adding Backend
1. Keep existing local storage for offline functionality
2. Add API calls to sync data when online
3. Implement authentication (optional)
4. Add real-time updates

## Deployment

### Gatsby Cloud (Recommended)
1. Connect GitHub repository
2. Select the `website` directory as root
3. Deploy automatically on push

### Netlify
1. Connect GitHub repository
2. Set base directory to `website`
3. Build command: `npm run build`
4. Publish directory: `public`

### Vercel
1. Import GitHub repository
2. Set root directory to `website`
3. Build command: `npm run build`
4. Output directory: `public`

### Static Hosting
Build the site and upload the `public/` directory to any static host:
- AWS S3 + CloudFront
- GitHub Pages
- Firebase Hosting

## Performance

- Lighthouse Score: 90+
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- All images optimized with Gatsby Image
- CSS Modules for optimal bundle splitting

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions  
- Safari: Latest 2 versions
- Mobile: iOS 12+, Android 8+

## Contributing

When adding new features:
1. Follow the existing component structure
2. Use CSS Modules for styling
3. Add proper TypeScript types (if applicable)
4. Test responsive design
5. Maintain glass morphism design consistency

## License

See main repository LICENSE file.

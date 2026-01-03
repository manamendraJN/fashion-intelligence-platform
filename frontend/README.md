# Frontend - Fashion Intelligence Platform

A modern React web application for AI-powered body measurement prediction.

## Overview

This frontend provides an intuitive interface for users to upload body images and receive accurate body measurements through AI analysis.

## Features

- **Image Upload Interface** - Drag-and-drop or click to upload front and side view images
- **Real-time Preview** - Background removal preview with mask visualization
- **Live API Status** - Connection indicator with auto-retry on disconnection
- **Measurement Display** - Clear visualization of all predicted body measurements
- **Responsive Design** - Mobile-friendly interface with Tailwind CSS
- **Error Handling** - Comprehensive validation and user feedback

## Tech Stack

- **Framework**: React 19
- **Build Tool**: Vite 7
- **Styling**: Tailwind CSS 4
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Dev Tools**: ESLint

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main application component
│   ├── main.jsx             # Application entry point
│   ├── index.css            # Global styles
│   ├── components/          # React components
│   │   ├── ImageUpload.jsx       # Image upload component
│   │   ├── MaskPreview.jsx       # Background removal preview
│   │   └── MeasurementsDisplay.jsx  # Results display
│   └── services/            # API integration
│       └── api.js           # Backend API calls
├── public/                  # Static assets
├── index.html              # HTML entry point
├── vite.config.js          # Vite configuration
├── package.json            # Dependencies
└── eslint.config.js        # ESLint configuration
```

## Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Configure environment** (optional)
   
   Create `.env` file:
   ```bash
   VITE_API_URL=http://localhost:5000
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

   Access at: `http://localhost:5173`

## Available Scripts

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build
```

## API Integration

The frontend communicates with the backend API through the `api.js` service:

- **Health Check** - `GET /health` - Monitor backend status
- **Model Info** - `GET /model-info` - Get current model details
- **Predict Measurements** - `POST /predict` - Submit images for analysis
- **Complete Analysis** - `POST /complete-analysis` - Full body measurement prediction
- **Preview Mask** - `POST /preview-mask` - Generate background removal preview

## Components

### ImageUpload
Handles image file selection with validation:
- File type checking (jpg, png, jpeg)
- File size validation (max 10MB)
- Preview generation
- Remove/replace functionality

### MaskPreview
Displays background removal preview:
- Original image view
- Processed image with removed background
- Binary mask visualization
- Accept/retry options

### MeasurementsDisplay
Shows predicted body measurements:
- All 14 body measurements
- Formatted display with units (cm)
- Warning indicators for unusual values
- Clean, organized layout

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:5000` | Backend API base URL |

## Development

### Prerequisites
- Node.js 18+ and npm
- Backend API running on port 5000

### Hot Module Replacement
Vite provides instant hot module replacement for fast development.

### Code Style
ESLint is configured for React best practices. Run `npm run lint` to check.

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ support required
- Responsive design for mobile devices

## Troubleshooting

**Image upload fails:**
- Check file size (must be < 10MB)
- Verify file type (jpg, png, jpeg only)
- Ensure both front and side images are uploaded

## License

Part of the Fashion Intelligence Platform project.

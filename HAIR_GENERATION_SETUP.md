# Hair Generation Setup Guide

## Backend Setup

### 1. Install Python Dependencies
```bash
cd Backend
pip install -r requirements.txt
```

### 2. Set Gemini API Key

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY="2vNDU9nTXcRgxm0fl5W33NVQ8qOVMjE71tWiLAdcHG7yUtmjkQI1FPSLDBrPJbYv"
```

**Or add to your environment permanently:**
```powershell
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', '2vNDU9nTXcRgxm0fl5W33NVQ8qOVMjE71tWiLAdcHG7yUtmjkQI1FPSLDBrPJbYv', 'User')
```

### 3. Start Backend Server
```bash
python app.py
```

The backend will run on `http://localhost:5000`

## Frontend Setup

### 1. Install Node Dependencies
```bash
cd Frontend
npm install
```

This will install:
- react-router-dom (for page navigation)
- axios (already installed)
- All other dependencies

### 2. Start Frontend Development Server
```bash
npm run dev
```

The frontend will run on `http://localhost:5173` (or another port shown in terminal)

## Testing the Application

1. **Skin Analysis Page** (Home)
   - Upload an image
   - Get skin tone, color, and blackhead predictions

2. **Hair Generation Page**
   - Navigate to "Hair Generation" from the top menu
   - Upload a photo
   - Optionally modify the AI prompt
   - Click "Generate Recommendations"
   - Get AI-powered hairstyle suggestions from Gemini

## API Endpoints

### Existing:
- `POST /predict` - Skin analysis predictions

### New:
- `POST /generate-hair` - Hair generation using Gemini AI
  - Parameters:
    - `file`: Image file (multipart/form-data)
    - `prompt`: Custom prompt for Gemini (optional)

## Features Added

### Backend (app.py)
- Gemini API integration
- New `/generate-hair` endpoint
- Image processing for Gemini Vision model

### Frontend
- New `HairGeneration` component with beautiful UI
- React Router for navigation
- Top navigation bar
- API function for hair generation
- Responsive design

## Troubleshooting

### If Gemini API returns an error:
1. Check your API key is set correctly
2. Ensure you have API quota remaining
3. Check the image format is supported (JPG, PNG, WEBP)

### If frontend can't connect:
1. Make sure backend is running on port 5000
2. Check CORS is enabled (already configured)
3. Verify the API_BASE_URL in `api.ts`

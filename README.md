<<<<<<< Updated upstream
# fashion-intelligence-platform
AI-powered fashion intelligence platform combining body measurement, size recommendations, wardrobe optimization, garment fitting analysis, accessories coordination, grooming recommendations, and personalized styling. Complete solution for smart fashion management.
=======
# Tone & Color Prediction System

A full-stack application for predicting tone and color characteristics from images using ConvNeXt Tiny models.

## Project Structure

```
project-root/
├─ backend/
│  ├─ app.py                 # Flask app with inference endpoints
│  ├─ models/
│  │  ├─ tone_convnext_tiny.onnx
│  │  ├─ color_convnext_tiny.onnx
│  │  ├─ tone_labels.json
│  │  └─ color_labels.json
│  ├─ requirements.txt       # flask, onnxruntime, pillow, torchvision, numpy
│  └─ utils/
│     └─ preprocess.py       # shared preprocessing (resize/center-crop/normalize)
├─ frontend/
│  ├─ package.json
│  ├─ src/
│  │  ├─ api.ts              # axios/fetch client
│  │  ├─ App.tsx             # main UI: upload, show predictions
│  │  ├─ components/
│  │  │  ├─ UploadCard.tsx
│  │  │  ├─ PredictionTable.tsx
│  │  │  └─ ImagePreview.tsx
│  │  └─ types.ts
│  └─ public/
└─ README.md
```

## Backend Setup

### Prerequisites
- Python 3.8+

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Running the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### API Endpoints

- `POST /predict` - Predict tone and color from an uploaded image
- `GET /health` - Health check endpoint

## Frontend Setup

### Prerequisites
- Node.js 16+

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

### Build

```bash
npm run build
```

## Features

- Upload images and get instant predictions
- Tone classification (warm, cool, neutral)
- Color classification (red, blue, green, yellow, orange, purple)
- Confidence scores for each prediction
- Real-time processing and results display

## Technologies

### Backend
- Flask for REST API
- ONNX Runtime for model inference
- Torchvision for image preprocessing
- Pillow for image handling

### Frontend
- React with TypeScript
- Axios for API communication
- Vite for build tooling
>>>>>>> Stashed changes

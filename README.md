# Heart Disease Predictor

A modern, user-friendly web application for predicting heart disease risk using machine learning.

## Features

- Beautiful, modern UI with light color palette
- Step-by-step questionnaire for easy data entry
- Clear explanations for each health metric
- Local Python ML model (scikit-learn .pkl file)
- Responsive design for all devices
- Real-time predictions with model kept in memory
- Deployed on Render.com with Flask backend

## Setup

### Local Development

1. Install Node.js dependencies:
```bash
npm install
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Build the frontend:
```bash
npm run build
```

4. Start the Flask server (serves both API and frontend):
```bash
python app.py
```

The app will be available at `http://localhost:5000`

**Alternative:** For frontend-only development:
```bash
npm run dev
```
(Note: API calls will need to point to a running Flask server)

### Production Build

```bash
npm run build
```

## Deployment to Render.com

### Why Render.com?
- **Real-time predictions**: Model stays loaded in memory (no cold starts)
- **Low latency**: Instant predictions with persistent server
- **Simple deployment**: One-click deployment from GitHub

### Deployment Steps

1. **Push your code to GitHub**
   - Make sure `binary_heart_disease_model.pkl` is in your repository root (not in `.gitignore`)
   - Ensure all files are committed

2. **Create a new Web Service on Render.com**
   - Go to [Render.com](https://render.com) and sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure the service:**
   - **Name**: `heart-disease-predictor` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `npm run build`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: `3.11.0` (or latest stable)

4. **Deploy!**
   - Render will automatically:
     - Install Node.js dependencies and build the React app
     - Install Python dependencies
     - Start the Flask server with Gunicorn
     - Load the model into memory on startup

5. **Your app will be live at**: `https://your-app-name.onrender.com`

### Using render.yaml (Optional)
If you've included `render.yaml` in your repo, Render will automatically detect and use these settings. You can also deploy via:
- Render Dashboard → New Web Service → Select your repo → Render will auto-detect the config

**Important:** 
- Make sure `binary_heart_disease_model.pkl` is in your repository root (not in `.gitignore`)
- The model loads once on startup and stays in memory for fast, real-time predictions

## Project Structure

```
├── api/
│   └── predict.py          # Python serverless function (legacy, for Vercel)
├── app.py                  # Flask app (serves API + static files)
├── src/
│   ├── components/         # React components
│   ├── App.jsx             # Main app logic
│   └── styles.css          # Styling
├── binary_heart_disease_model.pkl  # ML model
├── requirements.txt        # Python dependencies
├── render.yaml             # Render.com deployment config
└── package.json            # Node.js dependencies
```

## Usage

1. Start on the homepage and click "Let's Begin"
2. Answer each question one at a time:
   - Age
   - Biological sex
   - Chest pain type
   - ST depression value
   - Maximum heart rate
   - Cholesterol level
3. View your risk assessment results
4. Consult with a healthcare professional if risk is detected

## API Endpoint

The app uses a Flask API endpoint at `/api/predict` that:
- Loads the `.pkl` model once on startup (kept in memory for real-time predictions)
- Accepts POST requests with features array: `[age, sex, cp, oldpeak, thalach, chol]`
- Returns: `{ "prediction": 0 or 1, "has_risk": boolean, "probability": float }`

**Real-time Performance:**
- Model is loaded once when the server starts
- Stays in memory for instant predictions
- No cold start delays
- Typical response time: < 100ms

## Important Note

This tool is for informational purposes only and should not replace professional medical advice.


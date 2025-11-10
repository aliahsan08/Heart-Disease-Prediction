# Heart Disease Predictor

A modern, user-friendly web application for predicting heart disease risk using machine learning.

## Features

- Beautiful, modern UI with light color palette
- Step-by-step questionnaire for easy data entry
- Clear explanations for each health metric
- Local Python ML model (scikit-learn .pkl file)
- Responsive design for all devices
- Deployed on Vercel with Python serverless functions

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

3. Start development server:
```bash
npm run dev
```

4. For testing the API locally, use Vercel CLI:
```bash
npm i -g vercel
vercel dev
```

### Production Build

```bash
npm run build
```

## Deployment to Vercel

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Vercel will automatically detect:
   - Frontend: React/Vite app
   - Backend: Python serverless function in `/api`
   - Dependencies: `package.json` and `requirements.txt`
4. The `.pkl` model file will be included in deployment
5. Deploy!

**Important:** Make sure `binary_heart_disease_model.pkl` is in your repository root (not in `.gitignore`)

## Project Structure

```
├── api/
│   └── predict.py          # Python serverless function
├── src/
│   ├── components/         # React components
│   ├── App.jsx             # Main app logic
│   └── styles.css          # Styling
├── binary_heart_disease_model.pkl  # ML model
├── requirements.txt        # Python dependencies
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

The app uses a Python serverless function at `/api/predict` that:
- Loads the `.pkl` model on first request (cached for subsequent requests)
- Accepts POST requests with features array: `[age, sex, cp, oldpeak, thalach, chol]`
- Returns: `{ "prediction": 0 or 1, "has_risk": boolean }`

## Important Note

This tool is for informational purposes only and should not replace professional medical advice.


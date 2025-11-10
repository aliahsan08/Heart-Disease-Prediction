from http.server import BaseHTTPRequestHandler
import json
import pickle
import os
import sys

# Add the root directory to the path to access the model file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Global variable to store the loaded model (loaded once on cold start)
model = None

def load_model():
    """Load the model once and cache it"""
    global model
    if model is None:
        # Get the path to the model file
        # Try multiple possible locations (works in both local dev and Vercel)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        
        # Try root directory first (Vercel deployment)
        model_path = os.path.join(root_dir, 'heart_disease_binary_model.pkl')
        
        # If not found, try current directory (fallback)
        if not os.path.exists(model_path):
            model_path = os.path.join(current_dir, 'heart_disease_binary_model.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f'Model file not found. Tried: {model_path}')
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
    return model

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract features from request
            # Expected order: age, sex, cp, oldpeak, thalach, chol
            features = data.get('features', [])
            
            if len(features) != 6:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Invalid number of features. Expected 6 features.'
                }).encode())
                return
            
            # Load model (cached after first load)
            model = load_model()
            
            # Prepare input as 2D array (model expects shape [1, 6])
            import numpy as np
            input_data = np.array([features])
            
            # Make prediction
            prediction = model.predict(input_data)[0]
            
            # Get prediction probability if available
            prediction_proba = None
            if hasattr(model, 'predict_proba'):
                prediction_proba = model.predict_proba(input_data)[0]
            
            # Convert to binary (0 or 1)
            result = int(prediction)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'prediction': result,
                'has_risk': bool(result)
            }
            
            if prediction_proba is not None:
                response['probability'] = float(max(prediction_proba))
            
            self.wfile.write(json.dumps(response).encode())
            
        except FileNotFoundError:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': 'Model file not found'
            }).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e)
            }).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


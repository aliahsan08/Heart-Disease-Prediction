from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Add the root directory to the path to access the model file
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import joblib (preferred for scikit-learn models)
try:
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

# Global variable to store the loaded model (loaded once on startup)
model = None

def load_model():
    """Load the model once and cache it"""
    global model
    if model is None:
        # Get the path to the model file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'binary_heart_disease_model.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f'Model file not found at: {model_path}')
        
        # Try loading with joblib first (preferred for scikit-learn models)
        # If that fails, fall back to pickle
        loaded_data = None
        load_error = None
        
        if HAS_JOBLIB:
            try:
                loaded_data = joblib.load(model_path)
            except Exception as e:
                load_error = str(e)
                # Fall back to pickle
                import pickle
                try:
                    with open(model_path, 'rb') as f:
                        loaded_data = pickle.load(f)
                except Exception as pickle_error:
                    raise ValueError(f'Failed to load model with both joblib and pickle. Joblib error: {load_error}, Pickle error: {str(pickle_error)}')
        else:
            # Use pickle if joblib is not available
            import pickle
            try:
                with open(model_path, 'rb') as f:
                    loaded_data = pickle.load(f)
            except Exception as e:
                # Try to provide helpful error message for version mismatch
                error_msg = str(e)
                if '_RemainderColsList' in error_msg or 'Can\'t get attribute' in error_msg:
                    # This is a scikit-learn version mismatch issue
                    # Try to work around it by using joblib with compatibility mode
                    if HAS_JOBLIB:
                        try:
                            # joblib handles version mismatches better
                            loaded_data = joblib.load(model_path)
                        except Exception as joblib_error:
                            raise ValueError(
                                f'Model version mismatch detected. The model was saved with a different version of scikit-learn. '
                                f'Original error: {error_msg}. '
                                f'Joblib error: {str(joblib_error)}. '
                                f'\n\nSolution: Please retrain and save your model using joblib instead of pickle:\n'
                                f'  import joblib\n'
                                f'  joblib.dump(model, "binary_heart_disease_model.pkl")\n'
                                f'Or ensure you use the same scikit-learn version for training and deployment.'
                            )
                    else:
                        raise ValueError(
                            f'Model version mismatch. The model was saved with a different version of scikit-learn. '
                            f'Error: {error_msg}. '
                            f'Please install joblib (pip install joblib) and retrain the model using joblib.save() instead of pickle.'
                        )
                else:
                    raise
        
        # Import numpy to check for numpy arrays
        import numpy as np
        
        # Handle different pickle file structures
        # Case 1: Direct model object (but not a numpy array)
        if isinstance(loaded_data, np.ndarray):
            raise ValueError('Pickle file contains a numpy array, not a model. Please check the model file format.')
        elif hasattr(loaded_data, 'predict') and not isinstance(loaded_data, np.ndarray):
            model = loaded_data
        # Case 2: Dictionary with model inside
        elif isinstance(loaded_data, dict):
            # Try common keys
            if 'model' in loaded_data:
                candidate = loaded_data['model']
                if isinstance(candidate, np.ndarray):
                    raise ValueError('Dictionary contains numpy array at "model" key, not a model object.')
                model = candidate
            elif 'classifier' in loaded_data:
                candidate = loaded_data['classifier']
                if isinstance(candidate, np.ndarray):
                    raise ValueError('Dictionary contains numpy array at "classifier" key, not a model object.')
                model = candidate
            elif 'clf' in loaded_data:
                candidate = loaded_data['clf']
                if isinstance(candidate, np.ndarray):
                    raise ValueError('Dictionary contains numpy array at "clf" key, not a model object.')
                model = candidate
            else:
                # Try to find any object with predict method
                for key, value in loaded_data.items():
                    if isinstance(value, np.ndarray):
                        continue  # Skip numpy arrays
                    if hasattr(value, 'predict'):
                        model = value
                        break
                if model is None:
                    raise ValueError(f'Could not find model in dictionary. Keys: {list(loaded_data.keys())}')
        # Case 3: Tuple or list with model
        elif isinstance(loaded_data, (tuple, list)):
            for item in loaded_data:
                if isinstance(item, np.ndarray):
                    continue  # Skip numpy arrays
                if hasattr(item, 'predict'):
                    model = item
                    break
            if model is None:
                raise ValueError('Could not find model in tuple/list')
        else:
            raise ValueError(f'Unexpected model format: {type(loaded_data)}. Model must have a predict method.')
        
        # Final verification: model must have predict method and not be a numpy array
        if isinstance(model, np.ndarray):
            raise ValueError('Model is a numpy array, not a scikit-learn model object.')
        if not hasattr(model, 'predict'):
            raise ValueError(f'Loaded object does not have predict method. Type: {type(model)}')
    
    return model

# Initialize model on import (runs when app starts)
# This ensures the model is loaded once and kept in memory for fast predictions
try:
    load_model()
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict():
    """Handle prediction requests"""
    if request.method == 'OPTIONS':
        # Handle CORS preflight
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    try:
        data = request.get_json()
        
        # Extract features from request
        # Expected order: age, sex, cp, oldpeak, thalach, chol
        features = data.get('features', [])
        
        if len(features) != 6:
            return jsonify({
                'error': 'Invalid number of features. Expected 6 features.'
            }), 400
        
        # Get model (already loaded)
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
        
        response = {
            'prediction': result,
            'has_risk': bool(result)
        }
        
        if prediction_proba is not None:
            response['probability'] = float(max(prediction_proba))
        
        return jsonify(response)
        
    except FileNotFoundError as e:
        return jsonify({
            'error': 'Model file not found',
            'details': str(e)
        }), 500
    except Exception as e:
        import traceback
        error_details = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error in prediction: {error_details}")
        print(f"Traceback: {traceback_str}")
        
        return jsonify({
            'error': error_details,
            'type': type(e).__name__
        }), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve the React app for all routes"""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # For local development
    app.run(debug=True, port=5000)


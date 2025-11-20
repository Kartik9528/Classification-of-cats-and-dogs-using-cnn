"""
Flask Web Application for Cat and Dog CNN Classification
This provides a web interface to interact with the trained model
"""
import os
import io
import base64
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from cnn_model import CatDogCNN

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# Global model variable
cnn_model = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_model():
    """Load the trained CNN model"""
    global cnn_model
    model_path = 'cat_dog_cnn_model.h5'
    
    if os.path.exists(model_path):
        try:
            cnn_model = CatDogCNN()
            cnn_model.load_model(model_path)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    else:
        print("Model file not found. Creating demo model...")
        return create_demo_model()

def create_demo_model():
    """Create a simple demo model if no trained model exists"""
    global cnn_model
    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models
        
        print("Creating demo model...")
        
        # Create a simple model
        model = models.Sequential([
            layers.Conv2D(16, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(32, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(32, activation='relu'),
            layers.Dense(2, activation='softmax')
        ])
        
        model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
        
        # Save the model
        model.save('cat_dog_cnn_model.h5')
        
        # Load it with our CNN class
        cnn_model = CatDogCNN()
        cnn_model.model = model
        cnn_model.compile_model()
        
        print("Demo model created and loaded!")
        return True
        
    except Exception as e:
        print(f"Could not create demo model: {e}")
        return False

def create_upload_folder():
    """Create upload folder if it doesn't exist"""
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    """Main page"""
    model_status = "✅ Model Loaded" if cnn_model else "❌ Model Not Found"
    return render_template('index.html', model_status=model_status)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and prediction"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Make prediction
        if cnn_model:
            try:
                result = cnn_model.predict_image(filepath)
                
                # Create visualization
                img = Image.open(filepath)
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                
                # Show image
                ax1.imshow(img)
                ax1.set_title(f'Uploaded Image: {filename}', fontsize=14, fontweight='bold')
                ax1.axis('off')
                
                # Show prediction probabilities
                classes = list(result['probabilities'].keys())
                probabilities = list(result['probabilities'].values())
                colors = ['#FF6B6B', '#4ECDC4']
                
                bars = ax2.bar(classes, probabilities, color=colors, alpha=0.8)
                ax2.set_title('Prediction Probabilities', fontsize=14, fontweight='bold')
                ax2.set_ylabel('Probability')
                ax2.set_ylim(0, 1)
                
                # Add percentage labels on bars
                for bar, prob in zip(bars, probabilities):
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                            f'{prob:.1%}', ha='center', va='bottom', fontweight='bold')
                
                # Highlight predicted class
                predicted_idx = classes.index(result['predicted_class'])
                bars[predicted_idx].set_edgecolor('black')
                bars[predicted_idx].set_linewidth(3)
                
                plt.tight_layout()
                
                # Save plot
                plot_path = os.path.join(app.config['UPLOAD_FOLDER'], f'plot_{filename}.png')
                plt.savefig(plot_path, dpi=150, bbox_inches='tight')
                plt.close()
                
                # Convert image to base64 for display
                with open(filepath, 'rb') as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode()
                
                with open(plot_path, 'rb') as plot_file:
                    plot_base64 = base64.b64encode(plot_file.read()).decode()
                
                return jsonify({
                    'success': True,
                    'prediction': result['predicted_class'],
                    'confidence': f"{result['confidence']:.2%}",
                    'probabilities': result['probabilities'],
                    'image': img_base64,
                    'plot': plot_base64,
                    'filename': filename
                })
                
            except Exception as e:
                return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/demo')
def demo():
    """Demo page with sample images"""
    return render_template('demo.html')

@app.route('/model_info')
def model_info():
    """Model information page"""
    if cnn_model and cnn_model.model:
        model_summary = []
        cnn_model.model.summary(print_fn=lambda x: model_summary.append(x))
        
        return render_template('model_info.html', 
                             model_summary='\n'.join(model_summary),
                             model_loaded=True)
    else:
        return render_template('model_info.html', 
                             model_summary="Model not loaded",
                             model_loaded=False)

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Handle batch prediction"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    if not cnn_model:
        return jsonify({'error': 'Model not loaded'}), 500
    
    results = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                result = cnn_model.predict_image(filepath)
                results.append({
                    'filename': filename,
                    'prediction': result['predicted_class'],
                    'confidence': f"{result['confidence']:.2%}",
                    'probabilities': result['probabilities']
                })
            except Exception as e:
                results.append({
                    'filename': filename,
                    'error': str(e)
                })
    
    return jsonify({'results': results})

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

if __name__ == '__main__':
    # Create necessary directories
    create_upload_folder()
    
    # Load model
    if load_model():
        print("✅ Model loaded successfully!")
    else:
        print("❌ Model not found. Please train the model first.")
        print("Run: python train_model.py")
    
    # Run the app
    print("🚀 Starting Flask app...")
    print("📱 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

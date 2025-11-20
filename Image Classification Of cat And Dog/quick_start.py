"""
Quick Start Script - Minimal setup for immediate web app launch
Use this if you want to skip training and just run the web interface
"""
import os
import sys
import subprocess
import webbrowser
import time
from threading import Timer

def print_banner():
    print("🚀 Quick Start - Cat & Dog CNN Web App")
    print("=" * 50)

def check_basic_requirements():
    """Check if basic requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python
    try:
        import sys
        print(f"✅ Python: {sys.version}")
    except:
        print("❌ Python not found")
        return False
    
    # Check if Flask is available
    try:
        import flask
        print("✅ Flask available")
    except ImportError:
        print("⚠️  Flask not found. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "flask"], check=True)
            print("✅ Flask installed")
        except:
            print("❌ Could not install Flask")
            return False
    
    return True

def create_directories():
    """Create minimal required directories"""
    dirs = ['static/uploads', 'templates', 'static/css', 'static/js']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✅ Directories created")

def create_demo_model():
    """Create a simple demo model"""
    print("🔧 Creating demo model...")
    
    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models
        
        # Simple model for demo
        model = models.Sequential([
            layers.Conv2D(16, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(32, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(32, activation='relu'),
            layers.Dense(2, activation='softmax')
        ])
        
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.save('cat_dog_cnn_model.h5')
        print("✅ Demo model created")
        return True
        
    except Exception as e:
        print(f"❌ Could not create model: {e}")
        return False

def launch_app():
    """Launch the web application"""
    print("🚀 Starting web app...")
    
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:5000')
    
    Timer(2.0, open_browser).start()
    
    try:
        from app import app
        print("📱 Opening http://localhost:5000")
        print("🛑 Press Ctrl+C to stop")
        app.run(debug=False, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print_banner()
    
    if not check_basic_requirements():
        print("❌ Requirements not met")
        return
    
    create_directories()
    
    if not os.path.exists('cat_dog_cnn_model.h5'):
        create_demo_model()
    
    launch_app()

if __name__ == "__main__":
    main()

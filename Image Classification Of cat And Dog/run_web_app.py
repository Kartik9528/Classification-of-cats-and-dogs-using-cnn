"""
Web Application Launcher for Cat and Dog CNN Classifier
This script provides an easy way to start the web application
"""
import os
import sys
import subprocess
import webbrowser
import time
from threading import Timer

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import tensorflow
        import numpy
        import matplotlib
        import PIL
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_model():
    """Check if the trained model exists"""
    model_path = 'cat_dog_cnn_model.h5'
    if os.path.exists(model_path):
        print("✅ Trained model found!")
        return True
    else:
        print("❌ Trained model not found!")
        print("Please train the model first: python train_model.py")
        return False

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

def main():
    """Main function to launch the web application"""
    print("🐱🐶 Cat & Dog CNN Classifier - Web Application Launcher")
    print("=" * 60)
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    if not check_dependencies():
        return
    
    # Check model
    print("\n2. Checking trained model...")
    if not check_model():
        print("\n⚠️  You can still run the web app, but predictions won't work without a trained model.")
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response != 'y':
            return
    
    # Create necessary directories
    print("\n3. Setting up directories...")
    directories = ['static/uploads', 'templates', 'static/css', 'static/js']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created!")
    
    # Start the web application
    print("\n4. Starting web application...")
    print("🚀 Launching Flask server...")
    print("📱 The web interface will open automatically in your browser")
    print("🔗 Manual access: http://localhost:5000")
    print("\n" + "=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Open browser after delay
    Timer(3.0, open_browser).start()
    
    # Start Flask app
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Web application stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting web application: {e}")
        print("Please check the error message above and try again.")

if __name__ == "__main__":
    main()

"""
Simple Web App Starter - One-click launch for Cat & Dog CNN
This is the simplest way to start the web application
"""
import os
import sys
import webbrowser
import time
from threading import Timer

def main():
    print("🐱🐶 Cat & Dog CNN Web App - Simple Starter")
    print("=" * 50)
    
    # Create directories if they don't exist
    dirs = ['static/uploads', 'templates', 'static/css', 'static/js']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    print("✅ Directories ready")
    
    # Check if model exists, if not create a simple one
    if not os.path.exists('cat_dog_cnn_model.h5'):
        print("🔧 Creating demo model...")
        try:
            import tensorflow as tf
            from tensorflow.keras import layers, models
            
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
        except Exception as e:
            print(f"⚠️  Could not create model: {e}")
            print("The web app will still start, but predictions may not work")
    
    # Open browser after delay
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:5000')
    
    Timer(2.0, open_browser).start()
    
    print("🚀 Starting web server...")
    print("📱 Browser will open at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Web app stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")

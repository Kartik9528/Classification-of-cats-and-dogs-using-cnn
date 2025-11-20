"""
🚀 LAUNCH WEBSITE - Cat & Dog CNN Classification
This is the MAIN script to run everything smoothly
"""
import os
import sys
import subprocess
import webbrowser
import time
from threading import Timer

def print_header():
    print("=" * 70)
    print("🐱🐶 CAT & DOG CNN CLASSIFICATION - WEBSITE LAUNCHER 🐱🐶")
    print("=" * 70)
    print("🎯 This script will:")
    print("   ✅ Check your system")
    print("   ✅ Install dependencies if needed")
    print("   ✅ Create necessary files")
    print("   ✅ Launch the web interface")
    print("   ✅ Open your browser automatically")
    print("=" * 70)

def check_system():
    """Check if system is ready"""
    print("\n🔍 Checking system...")
    
    # Check Python
    try:
        python_version = sys.version_info
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
            print("⚠️  Python 3.7+ recommended")
        
        return True
    except:
        print("❌ Python not found")
        return False

def install_packages():
    """Install required packages"""
    print("\n📦 Installing packages...")
    
    packages = [
        "flask",
        "tensorflow", 
        "numpy",
        "matplotlib",
        "pillow",
        "scikit-learn",
        "opencv-python",
        "requests"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True, timeout=60)
            print(f"✅ {package} installed")
        except:
            print(f"⚠️  {package} installation failed, continuing...")

def setup_files():
    """Setup all necessary files and directories"""
    print("\n📁 Setting up files...")
    
    # Create directories
    directories = [
        'static/uploads',
        'templates', 
        'static/css',
        'static/js',
        'dataset/train/cats',
        'dataset/train/dogs',
        'dataset/validation/cats',
        'dataset/validation/dogs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Directories created")
    
    # Create demo model if needed
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

def launch_website():
    """Launch the website"""
    print("\n🚀 Launching website...")
    
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:5000')
            print("🌐 Browser opened!")
        except:
            print("⚠️  Could not open browser automatically")
            print("📱 Please open: http://localhost:5000")
    
    # Open browser after delay
    Timer(3.0, open_browser).start()
    
    print("=" * 50)
    print("🎉 WEBSITE IS STARTING!")
    print("=" * 50)
    print("📱 URL: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please run: pip install flask tensorflow")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print_header()
    
    # Check system
    if not check_system():
        print("\n❌ System check failed")
        input("Press Enter to exit...")
        return
    
    # Install packages
    install_packages()
    
    # Setup files
    setup_files()
    
    # Launch website
    print("\n🎯 Everything ready! Starting website...")
    launch_website()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Website stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to exit...")

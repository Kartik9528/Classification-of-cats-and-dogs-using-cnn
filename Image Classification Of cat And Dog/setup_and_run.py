"""
Complete Setup and Run Script for Cat & Dog CNN Web Application
This script handles everything from setup to running the web application
"""
import os
import sys
import subprocess
import platform
import webbrowser
import time
from threading import Timer

def print_banner():
    """Print welcome banner"""
    print("=" * 70)
    print("🐱🐶 Cat & Dog CNN Classification - Complete Setup & Run 🐱🐶")
    print("=" * 70)
    print("This script will:")
    print("1. Check Python installation")
    print("2. Install required dependencies")
    print("3. Setup dataset structure")
    print("4. Train the CNN model")
    print("5. Launch the web application")
    print("=" * 70)

def check_python():
    """Check if Python is installed and accessible"""
    print("\n🔍 Checking Python installation...")
    
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Python found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Python not working properly")
            return False
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        print("\n💡 Solutions:")
        print("1. Install Python from https://python.org")
        print("2. Make sure Python is added to PATH")
        print("3. Try running: python --version")
        return False

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        print("Upgrading pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        print("Installing packages from requirements.txt...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ All dependencies installed successfully!")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out. Please try again.")
        return False
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def setup_directories():
    """Create necessary directories"""
    print("\n📁 Setting up directories...")
    
    directories = [
        'dataset/train/cats',
        'dataset/train/dogs',
        'dataset/validation/cats', 
        'dataset/validation/dogs',
        'static/uploads',
        'templates',
        'static/css',
        'static/js'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    print("✅ All directories created!")

def setup_dataset():
    """Setup the dataset"""
    print("\n🖼️  Setting up dataset...")
    
    try:
        result = subprocess.run([sys.executable, "dataset_downloader.py"], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Dataset setup completed!")
            return True
        else:
            print(f"⚠️  Dataset setup had issues: {result.stderr}")
            print("Continuing anyway...")
            return True
            
    except subprocess.TimeoutExpired:
        print("⚠️  Dataset setup timed out. Continuing...")
        return True
    except Exception as e:
        print(f"⚠️  Dataset setup error: {e}. Continuing...")
        return True

def train_model():
    """Train the CNN model"""
    print("\n🧠 Training CNN model...")
    print("This may take several minutes...")
    
    try:
        # Run training with reduced epochs for faster setup
        result = subprocess.run([sys.executable, "train_model.py"], 
                              capture_output=True, text=True, timeout=1800)  # 30 minutes timeout
        
        if result.returncode == 0:
            print("✅ Model training completed!")
            return True
        else:
            print(f"⚠️  Training had issues: {result.stderr}")
            print("Checking if model file exists...")
            
            if os.path.exists('cat_dog_cnn_model.h5'):
                print("✅ Model file found! Continuing...")
                return True
            else:
                print("❌ No model file found. Training failed.")
                return False
                
    except subprocess.TimeoutExpired:
        print("⚠️  Training timed out. Checking for model file...")
        if os.path.exists('cat_dog_cnn_model.h5'):
            print("✅ Model file found! Continuing...")
            return True
        else:
            print("❌ Training incomplete. You can train manually later.")
            return False
    except Exception as e:
        print(f"⚠️  Training error: {e}")
        return False

def create_simple_model():
    """Create a simple model for demo if training fails"""
    print("\n🔧 Creating simple demo model...")
    
    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models
        
        # Create a simple model
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(2, activation='softmax')
        ])
        
        model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
        
        # Save the model
        model.save('cat_dog_cnn_model.h5')
        print("✅ Demo model created!")
        return True
        
    except Exception as e:
        print(f"❌ Could not create demo model: {e}")
        return False

def launch_web_app():
    """Launch the web application"""
    print("\n🚀 Launching web application...")
    
    def open_browser():
        time.sleep(3)
        webbrowser.open('http://localhost:5000')
    
    # Open browser after delay
    Timer(3.0, open_browser).start()
    
    print("📱 Web interface will open at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("\n" + "=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Web application stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting web application: {e}")
        print("You can try running manually: python app.py")

def main():
    """Main setup and run function"""
    print_banner()
    
    # Step 1: Check Python
    if not check_python():
        print("\n❌ Setup failed: Python not found")
        input("Press Enter to exit...")
        return
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        input("Press Enter to exit...")
        return
    
    # Step 3: Setup directories
    setup_directories()
    
    # Step 4: Setup dataset
    setup_dataset()
    
    # Step 5: Train model
    model_trained = train_model()
    
    # Step 6: Create demo model if training failed
    if not model_trained:
        print("\n⚠️  Training failed. Creating demo model...")
        if not create_simple_model():
            print("❌ Could not create demo model. Web app may not work properly.")
    
    # Step 7: Launch web app
    print("\n🎉 Setup completed! Launching web application...")
    launch_web_app()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")

"""
Demo script to showcase the Cat and Dog CNN Classification
This script demonstrates the complete workflow
"""
import os
import sys
from cnn_model import CatDogCNN

def run_demo():
    """Run a complete demo of the CNN classification system"""
    
    print("🐱🐶 Cat and Dog CNN Classification Demo 🐱🐶")
    print("=" * 60)
    
    # Step 1: Check if dataset exists
    print("\n1. Checking dataset...")
    if not os.path.exists('dataset/train'):
        print("❌ Dataset not found!")
        print("   Please run: python dataset_downloader.py")
        return False
    else:
        print("✅ Dataset found!")
    
    # Step 2: Check if model exists
    print("\n2. Checking trained model...")
    if not os.path.exists('cat_dog_cnn_model.h5'):
        print("❌ Trained model not found!")
        print("   Please run: python train_model.py")
        return False
    else:
        print("✅ Trained model found!")
    
    # Step 3: Load model and make predictions
    print("\n3. Loading model and making predictions...")
    cnn = CatDogCNN()
    cnn.load_model('cat_dog_cnn_model.h5')
    
    # Find test images
    test_images = []
    for root, dirs, files in os.walk('dataset'):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                test_images.append(os.path.join(root, file))
                if len(test_images) >= 4:  # Limit to 4 images for demo
                    break
        if len(test_images) >= 4:
            break
    
    if not test_images:
        print("❌ No test images found!")
        return False
    
    print(f"✅ Found {len(test_images)} test images")
    
    # Make predictions
    print("\n4. Making predictions...")
    print("-" * 40)
    
    for i, image_path in enumerate(test_images, 1):
        try:
            result = cnn.predict_image(image_path)
            filename = os.path.basename(image_path)
            print(f"Image {i}: {filename}")
            print(f"  → Predicted: {result['predicted_class']}")
            print(f"  → Confidence: {result['confidence']:.2%}")
            print()
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    print("=" * 60)
    print("🎉 Demo completed successfully!")
    print("=" * 60)
    
    return True

def show_usage():
    """Show usage instructions"""
    print("\n📖 Usage Instructions:")
    print("-" * 30)
    print("1. Setup dataset:     python dataset_downloader.py")
    print("2. Train model:       python train_model.py")
    print("3. Predict image:     python predict_image.py <image_path>")
    print("4. Batch predict:     python predict_image.py --batch <directory>")
    print("5. Run demo:          python demo.py")
    
    print("\n📁 Expected file structure:")
    print("-" * 30)
    print("dataset/")
    print("├── train/")
    print("│   ├── cats/")
    print("│   └── dogs/")
    print("└── validation/")
    print("    ├── cats/")
    print("    └── dogs/")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        show_usage()
        return
    
    success = run_demo()
    
    if not success:
        print("\n❌ Demo failed. Please check the setup.")
        show_usage()

if __name__ == "__main__":
    main()

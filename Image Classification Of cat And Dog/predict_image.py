"""
Image Prediction Script for Cat and Dog CNN
This script loads a trained model and predicts the class of an input image
"""
import sys
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from cnn_model import CatDogCNN

def predict_single_image(image_path, model_path='cat_dog_cnn_model.h5'):
    """Predict the class of a single image"""
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"Model file '{model_path}' not found!")
        print("Please train the model first by running: python train_model.py")
        return
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Image file '{image_path}' not found!")
        return
    
    print("=" * 50)
    print("Cat and Dog Image Classification")
    print("=" * 50)
    
    # Load the model
    print(f"\nLoading model from {model_path}...")
    cnn = CatDogCNN()
    cnn.load_model(model_path)
    
    # Make prediction
    print(f"\nAnalyzing image: {image_path}")
    result = cnn.predict_image(image_path)
    
    # Display results
    print("\n" + "-" * 30)
    print("PREDICTION RESULTS")
    print("-" * 30)
    print(f"Predicted Class: {result['predicted_class']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print("\nClass Probabilities:")
    for class_name, probability in result['probabilities'].items():
        print(f"  {class_name}: {probability:.2%}")
    
    # Display the image
    try:
        img = Image.open(image_path)
        plt.figure(figsize=(8, 6))
        plt.imshow(img)
        plt.title(f"Prediction: {result['predicted_class']} (Confidence: {result['confidence']:.2%})")
        plt.axis('off')
        plt.show()
    except Exception as e:
        print(f"Could not display image: {e}")
    
    return result

def batch_predict(directory_path, model_path='cat_dog_cnn_model.h5'):
    """Predict classes for all images in a directory"""
    
    if not os.path.exists(model_path):
        print(f"Model file '{model_path}' not found!")
        return
    
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' not found!")
        return
    
    # Load the model
    cnn = CatDogCNN()
    cnn.load_model(model_path)
    
    # Get all image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    image_files = [f for f in os.listdir(directory_path) 
                   if f.lower().endswith(image_extensions)]
    
    if not image_files:
        print(f"No image files found in {directory_path}")
        return
    
    print(f"\nFound {len(image_files)} images to predict...")
    print("=" * 60)
    
    results = []
    for i, image_file in enumerate(image_files, 1):
        image_path = os.path.join(directory_path, image_file)
        print(f"\n[{i}/{len(image_files)}] Processing: {image_file}")
        
        try:
            result = cnn.predict_image(image_path)
            result['filename'] = image_file
            results.append(result)
            
            print(f"  → {result['predicted_class']} ({result['confidence']:.2%})")
            
        except Exception as e:
            print(f"  → Error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("BATCH PREDICTION SUMMARY")
    print("=" * 60)
    
    cat_count = sum(1 for r in results if r['predicted_class'] == 'Cat')
    dog_count = sum(1 for r in results if r['predicted_class'] == 'Dog')
    
    print(f"Total images processed: {len(results)}")
    print(f"Cats predicted: {cat_count}")
    print(f"Dogs predicted: {dog_count}")
    
    if results:
        avg_confidence = np.mean([r['confidence'] for r in results])
        print(f"Average confidence: {avg_confidence:.2%}")
    
    return results

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python predict_image.py <image_path>                    # Predict single image")
        print("  python predict_image.py --batch <directory_path>        # Predict all images in directory")
        print("\nExamples:")
        print("  python predict_image.py test_image.jpg")
        print("  python predict_image.py --batch test_images/")
        return
    
    if sys.argv[1] == '--batch':
        if len(sys.argv) < 3:
            print("Please provide directory path for batch prediction")
            return
        batch_predict(sys.argv[2])
    else:
        predict_single_image(sys.argv[1])

if __name__ == "__main__":
    main()

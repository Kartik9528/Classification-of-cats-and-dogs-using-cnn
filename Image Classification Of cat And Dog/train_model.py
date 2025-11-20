"""
Training script for Cat and Dog CNN Classification
This script trains the CNN model on the dataset
"""
import os
import sys
from cnn_model import CatDogCNN
import matplotlib.pyplot as plt

def main():
    """Main training function"""
    print("=" * 60)
    print("Cat and Dog CNN Classification Training")
    print("=" * 60)
    
    # Check if dataset exists
    if not os.path.exists('dataset/train'):
        print("Dataset not found! Please run dataset_downloader.py first.")
        print("Run: python dataset_downloader.py")
        return
    
    # Initialize the CNN model
    print("\n1. Initializing CNN Model...")
    cnn = CatDogCNN(input_shape=(224, 224, 3), num_classes=2)
    
    # Build the model
    print("\n2. Building Model Architecture...")
    model = cnn.build_model()
    
    # Display model summary
    print("\nModel Architecture:")
    model.summary()
    
    # Compile the model
    print("\n3. Compiling Model...")
    cnn.compile_model(learning_rate=0.001)
    
    # Get data generators
    print("\n4. Setting up Data Generators...")
    train_generator, validation_generator = cnn.get_data_generators(
        train_dir='dataset/train',
        validation_dir='dataset/validation',
        batch_size=16  # Smaller batch size for limited dataset
    )
    
    print(f"Training samples: {train_generator.samples}")
    print(f"Validation samples: {validation_generator.samples}")
    print(f"Classes: {train_generator.class_indices}")
    
    # Train the model
    print("\n5. Training Model...")
    print("This may take a while...")
    
    history = cnn.train(
        train_generator=train_generator,
        validation_generator=validation_generator,
        epochs=30,  # Reduced epochs for demo
        verbose=1
    )
    
    # Plot training history
    print("\n6. Plotting Training History...")
    cnn.plot_training_history()
    
    # Save the model
    print("\n7. Saving Model...")
    cnn.save_model('cat_dog_cnn_model.h5')
    
    # Final evaluation
    print("\n8. Final Model Evaluation...")
    print("Training completed successfully!")
    print(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run 'python predict_image.py <image_path>' to test predictions")
    print("2. Check 'training_history.png' for training plots")
    print("3. Model saved as 'cat_dog_cnn_model.h5'")

if __name__ == "__main__":
    main()

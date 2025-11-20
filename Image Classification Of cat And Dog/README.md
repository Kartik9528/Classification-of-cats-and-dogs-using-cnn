# Cat and Dog Image Classification using CNN

A complete working CNN model for classifying images of cats and dogs using TensorFlow/Keras.

## Features

- **Deep CNN Architecture**: Multi-layer convolutional neural network with batch normalization and dropout
- **Data Augmentation**: Automatic image augmentation to improve model generalization
- **Transfer Learning Ready**: Easy to extend with pre-trained models
- **Comprehensive Evaluation**: Training history plots, confusion matrix, and detailed metrics
- **Easy to Use**: Simple scripts for training and prediction

## Model Architecture

The CNN model includes:
- 4 Convolutional blocks with increasing filters (32, 64, 128, 256)
- Batch normalization and dropout for regularization
- Global Average Pooling instead of Flatten
- Dense layers with dropout
- Softmax output for binary classification

## Installation

1. **Clone or download this repository**

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### 1. Setup Dataset
```bash
python dataset_downloader.py
```
This will create the dataset structure and download sample images for demonstration.

### 2. Train the Model
```bash
python train_model.py
```
This will:
- Build the CNN model
- Train on the dataset
- Save the best model as `cat_dog_cnn_model.h5`
- Generate training history plots

### 3. Launch Web Interface (Recommended)
```bash
python run_web_app.py
```
This will:
- Start the Flask web server
- Open your browser automatically
- Provide a beautiful web interface for predictions

### 4. Alternative: Command Line Predictions
```bash
# Predict a single image
python predict_image.py path/to/your/image.jpg

# Predict all images in a directory
python predict_image.py --batch path/to/image/directory/
```

## File Structure

```
├── dataset_downloader.py      # Downloads sample images and creates dataset structure
├── cnn_model.py              # CNN model class and training functions
├── train_model.py            # Main training script
├── predict_image.py          # Prediction script for single images or batches
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── dataset/                  # Dataset directory (created after running dataset_downloader.py)
    ├── train/
    │   ├── cats/
    │   └── dogs/
    └── validation/
        ├── cats/
        └── dogs/
```

## Model Performance

The model includes several techniques to improve performance:
- **Data Augmentation**: Rotation, shifting, flipping, zooming
- **Regularization**: Batch normalization and dropout layers
- **Early Stopping**: Prevents overfitting
- **Learning Rate Reduction**: Adaptive learning rate
- **Model Checkpointing**: Saves the best model during training

## Customization

### Using Your Own Dataset

1. **Replace the sample images** in the `dataset/` directory with your own images
2. **Maintain the folder structure**:
   ```
   dataset/
   ├── train/
   │   ├── cats/     # Put cat images here
   │   └── dogs/     # Put dog images here
   └── validation/
       ├── cats/     # Put validation cat images here
       └── dogs/     # Put validation dog images here
   ```

### Modifying the Model

Edit `cnn_model.py` to:
- Change the architecture (add/remove layers)
- Adjust hyperparameters (learning rate, batch size, etc.)
- Modify data augmentation parameters

### Training Parameters

In `train_model.py`, you can adjust:
- Number of epochs
- Batch size
- Learning rate
- Early stopping patience

## Example Usage

```python
from cnn_model import CatDogCNN

# Initialize model
cnn = CatDogCNN()

# Build and compile
model = cnn.build_model()
cnn.compile_model()

# Get data generators
train_gen, val_gen = cnn.get_data_generators('dataset/train', 'dataset/validation')

# Train
history = cnn.train(train_gen, val_gen, epochs=50)

# Make prediction
result = cnn.predict_image('test_image.jpg')
print(f"Predicted: {result['predicted_class']} with {result['confidence']:.2%} confidence")
```

## Output Files

After training, you'll get:
- `cat_dog_cnn_model.h5` - The trained model
- `best_model.h5` - Best model during training
- `training_history.png` - Training plots
- `confusion_matrix.png` - Model evaluation (if test data available)

## Troubleshooting

### Common Issues

1. **Out of Memory Error**: Reduce batch size in `train_model.py`
2. **No Images Found**: Make sure dataset structure is correct
3. **Model Not Found**: Train the model first with `python train_model.py`

### Performance Tips

1. **Use GPU**: Install TensorFlow GPU version for faster training
2. **More Data**: Use larger datasets for better performance
3. **Transfer Learning**: Use pre-trained models like VGG16, ResNet50
4. **Hyperparameter Tuning**: Experiment with learning rates and architecture

## Requirements

- Python 3.7+
- TensorFlow 2.15.0
- NumPy
- Matplotlib
- Pillow
- Scikit-learn
- OpenCV
- Requests

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## Acknowledgments

- Sample images from Unsplash
- TensorFlow/Keras documentation
- Deep learning community for best practices

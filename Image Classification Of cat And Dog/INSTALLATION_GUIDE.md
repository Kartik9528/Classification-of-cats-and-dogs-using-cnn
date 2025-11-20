# 🐱🐶 Cat & Dog CNN Classification - Installation Guide

## Quick Start (Recommended)

### Option 1: One-Click Start (Windows)
1. **Double-click** `run_website.bat`
2. Wait for setup to complete
3. Browser will open automatically

### Option 2: Python Script
```bash
python start_web_app.py
```

### Option 3: Full Setup
```bash
python setup_and_run.py
```

## Manual Installation

### Step 1: Install Python
1. Download Python from [python.org](https://python.org)
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify installation: `python --version`

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Dataset (Optional)
```bash
python dataset_downloader.py
```

### Step 4: Train Model (Optional)
```bash
python train_model.py
```

### Step 5: Start Web App
```bash
python app.py
```

## Troubleshooting

### Python Not Found
- **Windows**: Reinstall Python with "Add to PATH" checked
- **Mac**: Install via Homebrew: `brew install python`
- **Linux**: `sudo apt install python3 python3-pip`

### Dependencies Issues
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# If TensorFlow fails, try:
pip install tensorflow-cpu
```

### Model Issues
- If training fails, the app will create a demo model automatically
- For better accuracy, use the full training process

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`
- Or kill the process using port 5000

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Python**: 3.7 or higher

### Recommended
- **RAM**: 8GB or more
- **GPU**: NVIDIA GPU with CUDA support
- **Storage**: 5GB free space

## Features

### Web Interface
- ✅ Drag & drop image upload
- ✅ Real-time predictions
- ✅ Beautiful UI with animations
- ✅ Mobile responsive design
- ✅ Sample images for testing

### Model Features
- ✅ CNN architecture with 4 convolutional blocks
- ✅ Data augmentation
- ✅ Batch normalization and dropout
- ✅ Early stopping and learning rate reduction
- ✅ Model checkpointing

## File Structure
```
├── app.py                    # Flask web application
├── cnn_model.py             # CNN model class
├── start_web_app.py         # Simple starter script
├── setup_and_run.py         # Complete setup script
├── run_website.bat          # Windows batch file
├── requirements.txt         # Python dependencies
├── templates/               # HTML templates
├── static/                  # CSS, JS, uploads
└── dataset/                 # Training data
```

## Usage

### Web Interface
1. Open browser to `http://localhost:5000`
2. Upload an image (drag & drop or click)
3. View prediction results with confidence scores
4. Try sample images on the Demo page

### Command Line
```bash
# Single image prediction
python predict_image.py image.jpg

# Batch prediction
python predict_image.py --batch folder/
```

## Support

### Common Issues
1. **"Python not found"**: Install Python and add to PATH
2. **"Module not found"**: Run `pip install -r requirements.txt`
3. **"Port in use"**: Change port or kill existing process
4. **"Model not found"**: App will create demo model automatically

### Getting Help
- Check the console output for error messages
- Ensure all dependencies are installed
- Try the quick start scripts first
- For training issues, use the demo model

## Performance Tips

### For Better Accuracy
1. Use more training data
2. Train for more epochs
3. Use data augmentation
4. Try transfer learning

### For Faster Training
1. Use GPU if available
2. Increase batch size
3. Reduce image resolution
4. Use fewer epochs

## Next Steps

After successful installation:
1. Try the web interface
2. Upload your own images
3. Experiment with different models
4. Customize the UI
5. Deploy to cloud services

---

**Happy Classifying! 🐱🐶**

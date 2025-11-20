"""
Dataset downloader for cat and dog images
This script downloads sample images from the web for training
"""
import os
import requests
from PIL import Image
import io

def create_dataset_structure():
    """Create the dataset directory structure"""
    directories = [
        'dataset/train/cats',
        'dataset/train/dogs', 
        'dataset/validation/cats',
        'dataset/validation/dogs',
        'dataset/test/cats',
        'dataset/test/dogs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def download_sample_images():
    """Download sample cat and dog images from URLs"""
    
    # Sample image URLs (you can replace these with your own dataset)
    cat_urls = [
        "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1571566882372-1598d88abd90?w=300&h=300&fit=crop"
    ]
    
    dog_urls = [
        "https://images.unsplash.com/photo-1552053831-71594a27632d?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1547407139-3c921a71905c?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1551717743-49959800b1f6?w=300&h=300&fit=crop",
        "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=300&h=300&fit=crop"
    ]
    
    def download_image(url, save_path):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Open and resize image
            image = Image.open(io.BytesIO(response.content))
            image = image.resize((224, 224))
            image.save(save_path)
            print(f"Downloaded: {save_path}")
            return True
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return False
    
    # Download cat images
    for i, url in enumerate(cat_urls):
        download_image(url, f"dataset/train/cats/cat_{i+1}.jpg")
        download_image(url, f"dataset/validation/cats/cat_val_{i+1}.jpg")
    
    # Download dog images  
    for i, url in enumerate(dog_urls):
        download_image(url, f"dataset/train/dogs/dog_{i+1}.jpg")
        download_image(url, f"dataset/validation/dogs/dog_val_{i+1}.jpg")

if __name__ == "__main__":
    print("Creating dataset structure...")
    create_dataset_structure()
    
    print("Downloading sample images...")
    download_sample_images()
    
    print("Dataset setup complete!")
    print("\nNote: This downloads only sample images for demonstration.")
    print("For a real project, you should use a larger dataset like:")
    print("- Kaggle Dogs vs Cats dataset")
    print("- CIFAR-10 dataset")
    print("- Or collect your own images")

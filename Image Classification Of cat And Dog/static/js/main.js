/**
 * Main JavaScript file for Cat & Dog CNN Classifier
 * Handles interactive features and animations
 */

// Global variables
let isUploading = false;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    addAnimations();
});

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('🐱🐶 Cat & Dog CNN Classifier initialized');
    
    // Check if model is loaded
    checkModelStatus();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Setup drag and drop
    setupDragAndDrop();
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // File input change
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', handleFileSelect);
    });
    
    // Form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
    
    // Window events
    window.addEventListener('resize', handleResize);
    
    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
}

/**
 * Add animations and effects
 */
function addAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

/**
 * Check model status
 */
function checkModelStatus() {
    // This would typically make an API call to check model status
    const modelStatusElement = document.querySelector('.alert-info strong');
    if (modelStatusElement) {
        // Add a pulse animation to the status
        modelStatusElement.style.animation = 'pulse 2s infinite';
    }
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Setup drag and drop functionality
 */
function setupDragAndDrop() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });
        
        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            area.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, unhighlight, false);
        });
        
        // Handle dropped files
        area.addEventListener('drop', handleDrop, false);
    });
}

/**
 * Prevent default drag behaviors
 */
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

/**
 * Highlight drop area
 */
function highlight(e) {
    e.currentTarget.classList.add('drag-over');
}

/**
 * Remove highlight from drop area
 */
function unhighlight(e) {
    e.currentTarget.classList.remove('drag-over');
}

/**
 * Handle dropped files
 */
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        const fileInput = e.currentTarget.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
}

/**
 * Handle file selection
 */
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    // Validate file type
    if (!isValidImageFile(file)) {
        showNotification('Please select a valid image file (JPG, PNG, GIF, BMP, TIFF)', 'error');
        return;
    }
    
    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        showNotification('File size too large. Maximum size is 16MB.', 'error');
        return;
    }
    
    // Preview image
    previewImage(file, e.target);
    
    // Enable predict button
    const predictBtn = e.target.closest('form').querySelector('button[type="submit"]');
    if (predictBtn) {
        predictBtn.disabled = false;
        predictBtn.classList.add('pulse');
    }
    
    // Show file info
    showFileInfo(file);
}

/**
 * Validate image file
 */
function isValidImageFile(file) {
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/tiff'];
    return validTypes.includes(file.type);
}

/**
 * Preview selected image
 */
function previewImage(file, inputElement) {
    const reader = new FileReader();
    reader.onload = function(e) {
        // Find the result image element
        const resultImage = inputElement.closest('.container').querySelector('#resultImage, #demoResultImage');
        if (resultImage) {
            resultImage.src = e.target.result;
            resultImage.style.opacity = '0';
            resultImage.style.transition = 'opacity 0.3s ease';
            
            setTimeout(() => {
                resultImage.style.opacity = '1';
            }, 100);
        }
    };
    reader.readAsDataURL(file);
}

/**
 * Show file information
 */
function showFileInfo(file) {
    const fileInfo = document.querySelector('#fileInfo');
    if (fileInfo) {
        const fileName = fileInfo.querySelector('#fileName');
        if (fileName) {
            fileName.textContent = file.name;
        }
        fileInfo.style.display = 'block';
        fileInfo.classList.add('fade-in');
    }
}

/**
 * Handle form submission
 */
function handleFormSubmit(e) {
    e.preventDefault();
    
    if (isUploading) {
        return;
    }
    
    const form = e.target;
    const fileInput = form.querySelector('input[type="file"]');
    
    if (!fileInput || !fileInput.files[0]) {
        showNotification('Please select a file first.', 'error');
        return;
    }
    
    uploadAndPredict(form, fileInput.files[0]);
}

/**
 * Upload file and make prediction
 */
function uploadAndPredict(form, file) {
    isUploading = true;
    
    const formData = new FormData();
    formData.append('file', file);
    
    // Show loading state
    showLoadingState(form);
    
    // Make API request
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        hideLoadingState(form);
        
        if (data.success) {
            displayResults(data, form);
            showNotification('Prediction completed successfully!', 'success');
        } else {
            showNotification(data.error || 'Prediction failed', 'error');
        }
    })
    .catch(error => {
        hideLoadingState(form);
        console.error('Error:', error);
        showNotification('Network error: ' + error.message, 'error');
    })
    .finally(() => {
        isUploading = false;
    });
}

/**
 * Show loading state
 */
function showLoadingState(form) {
    const loadingSpinner = form.closest('.container').querySelector('#loadingSpinner, #demoLoadingSpinner');
    const resultsSection = form.closest('.container').querySelector('#resultsSection, #demoResultsSection');
    const errorAlert = form.closest('.container').querySelector('#errorAlert, #demoErrorAlert');
    
    if (loadingSpinner) {
        loadingSpinner.style.display = 'block';
    }
    
    if (resultsSection) {
        resultsSection.style.display = 'none';
    }
    
    if (errorAlert) {
        errorAlert.style.display = 'none';
    }
    
    // Disable form elements
    const formElements = form.querySelectorAll('input, button');
    formElements.forEach(element => {
        element.disabled = true;
    });
}

/**
 * Hide loading state
 */
function hideLoadingState(form) {
    const loadingSpinner = form.closest('.container').querySelector('#loadingSpinner, #demoLoadingSpinner');
    
    if (loadingSpinner) {
        loadingSpinner.style.display = 'none';
    }
    
    // Re-enable form elements
    const formElements = form.querySelectorAll('input, button');
    formElements.forEach(element => {
        element.disabled = false;
    });
}

/**
 * Display prediction results
 */
function displayResults(data, form) {
    const resultsSection = form.closest('.container').querySelector('#resultsSection, #demoResultsSection');
    
    if (!resultsSection) return;
    
    // Update prediction elements
    updatePredictionElements(data, resultsSection);
    
    // Create probability chart
    createProbabilityChart(data.probabilities, resultsSection);
    
    // Show results with animation
    resultsSection.style.display = 'block';
    resultsSection.classList.add('fade-in');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Update prediction elements
 */
function updatePredictionElements(data, resultsSection) {
    // Update prediction class
    const predictionClass = resultsSection.querySelector('#predictionClass, #demoPredictionClass');
    if (predictionClass) {
        predictionClass.textContent = data.prediction;
    }
    
    // Update confidence
    const confidence = resultsSection.querySelector('#confidence, #demoConfidence');
    if (confidence) {
        confidence.textContent = data.confidence;
        
        // Update badge color based on confidence
        const confidenceValue = parseFloat(data.confidence);
        confidence.className = 'badge fs-6';
        
        if (confidenceValue >= 80) {
            confidence.classList.add('bg-success');
        } else if (confidenceValue >= 60) {
            confidence.classList.add('bg-warning');
        } else {
            confidence.classList.add('bg-danger');
        }
    }
    
    // Update prediction icon
    const predictionIcon = resultsSection.querySelector('#predictionIcon, #demoPredictionIcon');
    if (predictionIcon) {
        if (data.prediction === 'Cat') {
            predictionIcon.className = 'fas fa-cat fa-3x text-warning';
        } else {
            predictionIcon.className = 'fas fa-dog fa-3x text-info';
        }
    }
}

/**
 * Create probability chart
 */
function createProbabilityChart(probabilities, resultsSection) {
    const chartContainer = resultsSection.querySelector('#probabilityChart, #demoProbabilityChart');
    if (!chartContainer) return;
    
    chartContainer.innerHTML = '';
    
    Object.entries(probabilities).forEach(([className, probability]) => {
        const percentage = (probability * 100).toFixed(1);
        const color = className === 'Cat' ? '#FF6B6B' : '#4ECDC4';
        
        const barContainer = document.createElement('div');
        barContainer.className = 'probability-bar mb-2';
        
        barContainer.innerHTML = `
            <div class="d-flex justify-content-between mb-1">
                <span class="fw-bold">${className}</span>
                <span>${percentage}%</span>
            </div>
            <div class="progress" style="height: 20px;">
                <div class="progress-bar" role="progressbar" 
                     style="width: 0%; background-color: ${color};" 
                     aria-valuenow="${percentage}" aria-valuemin="0" aria-valuemax="100">
                </div>
            </div>
        `;
        
        chartContainer.appendChild(barContainer);
        
        // Animate progress bar
        setTimeout(() => {
            const progressBar = barContainer.querySelector('.progress-bar');
            progressBar.style.width = percentage + '%';
        }, 100);
    });
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

/**
 * Handle window resize
 */
function handleResize() {
    // Adjust layout for mobile devices
    if (window.innerWidth < 768) {
        document.body.classList.add('mobile');
    } else {
        document.body.classList.remove('mobile');
    }
}

/**
 * Handle keyboard shortcuts
 */
function handleKeyboardShortcuts(e) {
    // Ctrl/Cmd + U to focus file input
    if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
        e.preventDefault();
        const fileInput = document.querySelector('input[type="file"]:not([style*="display: none"])');
        if (fileInput) {
            fileInput.click();
        }
    }
    
    // Escape to clear results
    if (e.key === 'Escape') {
        const resultsSection = document.querySelector('#resultsSection, #demoResultsSection');
        if (resultsSection && resultsSection.style.display !== 'none') {
            resultsSection.style.display = 'none';
        }
    }
}

/**
 * Utility function to format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Utility function to get file extension
 */
function getFileExtension(filename) {
    return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2);
}

// Export functions for global access
window.CatDogCNN = {
    showNotification,
    formatFileSize,
    getFileExtension
};

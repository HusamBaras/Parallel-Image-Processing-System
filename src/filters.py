import numpy as np
from PIL import Image

def grayscale(image_np):
    """
    Convert RGB image to grayscale using the luminance formula.
    This formula accounts for human perception of color brightness.
    Formula: L = 0.299*R + 0.587*G + 0.114*B
    """
    if len(image_np.shape) == 3:
        weights = np.array([0.299, 0.587, 0.114])
        grayscale_img = np.dot(image_np[..., :3], weights)
        return grayscale_img.astype(np.uint8)
    return image_np

def gaussian_blur(image_np):
    """
    Apply a 3x3 Gaussian kernel for image smoothing/blurring.
    The kernel reduces high-frequency noise by averaging pixel values 
    with their neighbors using Gaussian weights.
    """
    kernel = np.array([[1, 2, 1],
                       [2, 4, 2],
                       [1, 2, 1]]) / 16.0
    return apply_kernel(image_np, kernel)

def sobel_edge_detection(image_np):
    """
    Apply the Sobel operator to detect edges in the image.
    It calculates the gradient of the image intensity at each pixel.
    Uses two 3x3 kernels (Gx and Gy) to find horizontal and vertical changes.
    """
    # Convert to grayscale first if it's RGB as Sobel operates on intensity
    if len(image_np.shape) == 3:
        img = grayscale(image_np)
    else:
        img = image_np
    
    kx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])
    ky = np.array([[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]])
    
    ix = apply_kernel(img, kx)
    iy = apply_kernel(img, ky)
    
    # Combine gradients
    gradient_magnitude = np.sqrt(ix.astype(float)**2 + iy.astype(float)**2)
    gradient_magnitude = (gradient_magnitude / gradient_magnitude.max() * 255).astype(np.uint8)
    return gradient_magnitude

def sharpen(image_np):
    """Enhance edges and details using a sharpening kernel."""
    kernel = np.array([[ 0, -1,  0],
                       [-1,  5, -1],
                       [ 0, -1,  0]])
    return apply_kernel(image_np, kernel)

def adjust_brightness(image_np, factor=1.5):
    """Increase or decrease image brightness."""
    brightened = image_np.astype(float) * factor
    return np.clip(brightened, 0, 255).astype(np.uint8)

def apply_kernel(image_np, kernel):
    """Generic 2D convolution for 3x3 kernels."""
    if len(image_np.shape) == 3:
        # Apply to each channel
        result = np.zeros_like(image_np)
        for i in range(3):
            result[..., i] = convolve2d(image_np[..., i], kernel)
        return result
    else:
        return convolve2d(image_np, kernel)

def convolve2d(image, kernel):
    """Simple 2D convolution."""
    h, w = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    
    padded_img = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    output = np.zeros_like(image)
    
    for i in range(h):
        for j in range(w):
            region = padded_img[i:i+kh, j:j+kw]
            output[i, j] = np.sum(region * kernel)
            
    return np.clip(output, 0, 255).astype(np.uint8)

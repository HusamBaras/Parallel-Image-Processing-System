import os
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
import numpy as np
import src.filters as filters

def process_single_image(args):
    """
    Process a single image by applying all filters in sequence.
    This function is designed to be used with parallel mapping.
    """
    img_path, output_dir = args
    try:
        # 1. Load image
        img = Image.open(img_path).convert('RGB')
        img_np = np.array(img)
        
        # 2. Apply Grayscale
        img_gray = filters.grayscale(img_np)
        
        # 3. Apply Gaussian Blur
        img_blur = filters.gaussian_blur(img_gray)
        
        # 4. Apply Sobel Edge Detection
        img_edge = filters.sobel_edge_detection(img_blur)
        
        # 5. Apply Sharpening
        img_sharpen = filters.sharpen(img_edge)
        
        # 6. Apply Brightness Adjustment
        img_final = filters.adjust_brightness(img_sharpen, factor=1.2)
        
        # 7. Save result
        filename = os.path.basename(img_path)
        output_path = os.path.join(output_dir, f"processed_{filename}")
        
        # Convert back to PIL Image to save
        result_img = Image.fromarray(img_final)
        result_img.save(output_path)
        return True
    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        return False

def run_sequential(image_paths, output_dir):
    start_time = time.time()
    results = []
    for path in image_paths:
        results.append(process_single_image((path, output_dir)))
    end_time = time.time()
    return end_time - start_time

def run_multiprocessing(image_paths, output_dir, num_processes):
    start_time = time.time()
    args = [(path, output_dir) for path in image_paths]
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(process_single_image, args)
    end_time = time.time()
    return end_time - start_time

def run_concurrent_futures(image_paths, output_dir, num_workers):
    start_time = time.time()
    args = [(path, output_dir) for path in image_paths]
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(process_single_image, args))
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    # Simple test run
    data_dir = "data"
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    image_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Found {len(image_paths)} images.")
    
    print("Running Sequential...")
    t_seq = run_sequential(image_paths, output_dir)
    print(f"Sequential Time: {t_seq:.4f}s")
    
    print(f"Running Multiprocessing (4 processes)...")
    t_mp = run_multiprocessing(image_paths, output_dir, 4)
    print(f"Multiprocessing Time: {t_mp:.4f}s")
    
    print(f"Running Concurrent.Futures (4 workers)...")
    t_cf = run_concurrent_futures(image_paths, output_dir, 4)
    print(f"Concurrent.Futures Time: {t_cf:.4f}s")

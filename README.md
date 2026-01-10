# Parallel Image Processing System (CST435 Assignment 2)

This project implements a parallel image processing pipeline using Python. It applies multiple filters to a collection of images and compares the performance of different parallel programming paradigms.

## Features
- **Five Image Filters**:
  1. Grayscale Conversion
  2. Gaussian Blur (3x3)
  3. Sobel Edge Detection
  4. Image Sharpening
  5. Brightness Adjustment
- **Parallel Paradigms**:
  - `multiprocessing` module
  - `concurrent.futures` (ProcessPoolExecutor)
- **Performance Analysis**: Automated benchmarking and visualization of speedup and efficiency.

## Project Structure
- `src/filters.py`: Implementation of image processing algorithms using NumPy.
- `src/image_processor.py`: Core logic for sequential and parallel execution.
- `benchmark.py`: Script to run performance tests and generate graphs.
- `setup_data.py`: Utility to generate sample image data for testing.
- `data/`: Input images directory.
- `output/`: Processed images directory.

## Setup and Execution

1. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install Pillow numpy matplotlib pandas
   ```

3. **Generate Sample Data**:
   ```bash
   python3 setup_data.py
   ```

4. **Run Benchmarks**:
   ```bash
   python3 benchmark.py
   ```

## Performance Metrics
The system evaluates performance based on:
- **Execution Time**: Total time taken to process the dataset.
- **Speedup**: $S_p = \frac{T_1}{T_p}$
- **Efficiency**: $E_p = \frac{S_p}{p}$

Where $T_1$ is sequential time, $T_p$ is parallel time with $p$ processes.

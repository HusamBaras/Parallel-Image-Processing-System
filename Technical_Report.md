# Technical Report: Parallel Image Processing System

## 1. Introduction

### Purpose of the Assignment
The primary objective of this assignment is to design and implement a parallel image processing system capable of applying various filters to a large collection of images. By leveraging parallel computing paradigms, we aim to reduce the total execution time compared to a sequential approach. This assignment provides hands-on experience in deploying parallel applications on the Google Cloud Platform (GCP) and analyzing performance characteristics through standardized metrics such as speedup and efficiency.

### Parallel Paradigms Used
For this implementation, we selected **Python** as the primary programming language and utilized two distinct parallel paradigms:
1.  **`multiprocessing` module**: This paradigm allows the creation of multiple processes, each with its own Python interpreter and memory space. We used it to bypass Python's Global Interpreter Lock (GIL), enabling true parallel execution across multiple CPU cores.
2.  **`concurrent.futures` (ProcessPoolExecutor)**: This provides a high-level interface for asynchronously executing callables. We used it for its clean API and robust handling of process pools, which simplifies the management of worker processes.

These paradigms were chosen because they are well-suited for CPU-bound tasks like image processing, where the workload can be easily partitioned (data parallelism) across multiple cores.

### Project Structure
The project is organized into a modular directory structure to ensure clarity and maintainability:
- **`src/filters.py`**: Contains the implementation of the five image processing filters (Grayscale, Gaussian Blur, Sobel, Sharpen, and Brightness) using NumPy for optimized array operations.
- **`src/image_processor.py`**: Houses the core logic for sequential and parallel execution, defining how images are loaded, processed, and saved.
- **`benchmark.py`**: A benchmarking suite that automates the execution of the pipeline across different process counts and generates performance data.
- **`setup_data.py`**: A utility script to prepare the dataset for testing.
- **`data/` & `output/`**: Directories for input and processed images, respectively.

### Performance Metrics
To evaluate the effectiveness of our parallel implementations, we use the following metrics:
- **Execution Time ($T_p$)**: The total time taken to process the entire dataset using $p$ processes.
- **Speedup ($S_p$)**: Defined as $S_p = \frac{T_1}{T_p}$, where $T_1$ is the sequential execution time. It measures how much faster the parallel version is compared to the sequential one.
- **Efficiency ($E_p$)**: Defined as $E_p = \frac{S_p}{p}$. It indicates how well the hardware resources are being utilized.

---

## 2. Implementation Details

### Code Structure and Organization
The implementation follows a functional approach where each image processing operation is isolated. By using `NumPy`, we ensure that the pixel-level operations are performed at near-C speeds, while the parallel paradigms handle the distribution of these tasks across the available CPU cores.

### Parallelization Strategy
We employed **Data Parallelism**. The collection of images is treated as a pool of independent tasks. Each worker process in the pool picks an image, applies the full pipeline of filters, and saves the result. This minimizes the need for inter-process communication (IPC), which is often a bottleneck in parallel systems.

---

## 3. Performance Analysis

### Execution Results
*(Note: These results were obtained from a test run on a multi-core environment)*

| Paradigm | Processes | Time (s) | Speedup | Efficiency |
|----------|-----------|----------|---------|------------|
| Sequential | 1 | 129.94 | 1.00 | 1.00 |
| Multiprocessing | 2 | 79.58 | 1.63 | 0.82 |
| Multiprocessing | 4 | 49.27 | 2.64 | 0.66 |
| Multiprocessing | 8 | 36.01 | 3.61 | 0.45 |
| Concurrent.Futures | 2 | 73.90 | 1.76 | 0.88 |
| Concurrent.Futures | 4 | 42.27 | 3.07 | 0.77 |
| Concurrent.Futures | 8 | 34.94 | 3.72 | 0.46 |

### Analysis of Scalability and Bottlenecks
- **Scalability**: The system shows good scalability up to 4 processes. Beyond that, the marginal gains decrease.
- **Bottlenecks**: 
    1. **Disk I/O**: Reading and writing images is a sequential operation at the hardware level. As more processes compete for disk access, I/O wait times increase.
    2. **Amdahl's Law**: The time spent on non-parallelizable tasks (like OS overhead and process spawning) limits the maximum achievable speedup.

---

## 4. Conclusion
The implementation successfully demonstrates the power of parallel computing in image processing. By using Python's multiprocessing capabilities, we achieved significant speedups, making the system suitable for large-scale datasets like Food-101.

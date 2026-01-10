import os
import pandas as pd
import matplotlib.pyplot as plt
import src.image_processor as processor

def run_benchmarks():
    data_dir = "data"
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    image_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    process_counts = [1, 2, 4, 8]
    results = []

    print(f"Starting benchmarks with {len(image_paths)} images...")

    # Sequential baseline
    print("Running Sequential...")
    t_seq = processor.run_sequential(image_paths, output_dir)
    results.append({
        "Paradigm": "Sequential",
        "Processes": 1,
        "Time": t_seq,
        "Speedup": 1.0,
        "Efficiency": 1.0
    })

    # Multiprocessing benchmarks
    for n in process_counts:
        if n == 1: continue # Already covered by sequential-like or just run it
        print(f"Running Multiprocessing with {n} processes...")
        t = processor.run_multiprocessing(image_paths, output_dir, n)
        speedup = t_seq / t
        efficiency = speedup / n
        results.append({
            "Paradigm": "Multiprocessing",
            "Processes": n,
            "Time": t,
            "Speedup": speedup,
            "Efficiency": efficiency
        })

    # Concurrent.Futures benchmarks
    for n in process_counts:
        if n == 1: continue
        print(f"Running Concurrent.Futures with {n} processes...")
        t = processor.run_concurrent_futures(image_paths, output_dir, n)
        speedup = t_seq / t
        efficiency = speedup / n
        results.append({
            "Paradigm": "Concurrent.Futures",
            "Processes": n,
            "Time": t,
            "Speedup": speedup,
            "Efficiency": efficiency
        })

    df = pd.DataFrame(results)
    df.to_csv("benchmark_results.csv", index=False)
    print("\nBenchmark results saved to benchmark_results.csv")
    print(df)
    return df

def plot_results(df):
    # Filter out Sequential for comparison plots if needed, or keep it as 1 process
    
    plt.figure(figsize=(12, 5))

    # Execution Time Plot
    plt.subplot(1, 2, 1)
    for paradigm in ["Multiprocessing", "Concurrent.Futures"]:
        data = df[df["Paradigm"] == paradigm]
        plt.plot(data["Processes"], data["Time"], marker='o', label=paradigm)
    
    # Add sequential point
    seq_time = df[df["Paradigm"] == "Sequential"]["Time"].values[0]
    plt.scatter([1], [seq_time], color='red', label='Sequential', zorder=5)
    
    plt.title("Execution Time vs Process Count")
    plt.xlabel("Number of Processes")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)

    # Speedup Plot
    plt.subplot(1, 2, 2)
    for paradigm in ["Multiprocessing", "Concurrent.Futures"]:
        data = df[df["Paradigm"] == paradigm]
        plt.plot(data["Processes"], data["Speedup"], marker='o', label=paradigm)
    
    # Ideal speedup line
    plt.plot([1, 8], [1, 8], 'k--', label="Ideal Speedup")
    
    plt.title("Speedup vs Process Count")
    plt.xlabel("Number of Processes")
    plt.ylabel("Speedup")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("performance_analysis.png")
    print("Plots saved to performance_analysis.png")

if __name__ == "__main__":
    df = run_benchmarks()
    plot_results(df)

import psutil
import time
import numpy as np

# Monitoring duration in seconds
monitor_duration = 300  # 5 minutes
monitor_interval = 1    # 1 second intervals

# Get total memory in MB
total_memory_mb = psutil.virtual_memory().total / (1024 * 1024)

# Initialize lists for storing CPU and memory usage
cpu_usage = []
memory_usage = []

# For tracking top processes during monitoring
process_cpu_usage = []
process_memory_usage = []

print("Monitoring system for 5 minutes...")

# Monitor for the duration
for _ in range(monitor_duration):
    cpu_usage.append(psutil.cpu_percent())
    memory_info = psutil.virtual_memory()
    memory_usage.append(memory_info.percent)

    # Capture all current processes
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        process_list.append(proc.info)
    
    process_cpu_usage.append(sorted(process_list, key=lambda p: p['cpu_percent'], reverse=True)[:10])
    process_memory_usage.append(sorted(process_list, key=lambda p: p['memory_percent'], reverse=True)[:10])

    time.sleep(monitor_interval)

# Calculating CPU and Memory Stats
cpu_max = max(cpu_usage)
cpu_min = min(cpu_usage)
cpu_avg = np.mean(cpu_usage)
cpu_median = np.median(cpu_usage)

memory_max = max(memory_usage)
memory_min = min(memory_usage)
memory_avg = np.mean(memory_usage)
memory_median = np.median(memory_usage)

memory_max_mb = (memory_max / 100) * total_memory_mb
memory_min_mb = (memory_min / 100) * total_memory_mb
memory_avg_mb = (memory_avg / 100) * total_memory_mb
memory_median_mb = (memory_median / 100) * total_memory_mb

# Print CPU and Memory Stats
print("\nCPU Usage over 5 minutes:")
print(f"Max CPU: {cpu_max}%")
print(f"Min CPU: {cpu_min}%")
print(f"Average CPU: {cpu_avg}%")
print(f"Median CPU: {cpu_median}%")

print("\nMemory Usage over 5 minutes:")
print(f"Max Memory: {memory_max}% ({memory_max_mb:.2f} MB)")
print(f"Min Memory: {memory_min}% ({memory_min_mb:.2f} MB)")
print(f"Average Memory: {memory_avg}% ({memory_avg_mb:.2f} MB)")
print(f"Median Memory: {memory_median}% ({memory_median_mb:.2f} MB)")

# Function to get the median and max for a process
def get_process_stats(process_usage, key):
    median = np.median([p[key] for p in process_usage])
    maximum = max([p[key] for p in process_usage])
    return median, maximum

# Calculate top 10 memory-consuming processes
print("\nTop 10 memory-consuming processes (Memory % and MB):")
for i, proc in enumerate(process_memory_usage[-1]):
    memory_mb = (proc['memory_percent'] / 100) * total_memory_mb
    print(f"{i + 1}. {proc['name']} (PID: {proc['pid']}) - Memory: {proc['memory_percent']}% ({memory_mb:.2f} MB)")

# Calculate top 10 CPU-consuming processes
print("\nTop 10 CPU-consuming processes:")
for i, proc in enumerate(process_cpu_usage[-1]):
    print(f"{i + 1}. {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']}%")


import psutil
import time
import numpy as np
import csv
import io

def monitor_cpu_memory(duration=300):
    cpu_usage = []
    memory_usage = []

    print(f"Monitoring system for {duration // 60} minutes...\n")

    for _ in range(duration):
        cpu_usage.append(psutil.cpu_percent(interval=1))
        memory_info = psutil.virtual_memory()
        memory_usage.append(memory_info.percent)
    
    max_cpu = np.max(cpu_usage)
    min_cpu = np.min(cpu_usage)
    avg_cpu = np.mean(cpu_usage)
    median_cpu = np.median(cpu_usage)
    
    max_memory = np.max(memory_usage)
    min_memory = np.min(memory_usage)
    avg_memory = np.mean(memory_usage)
    median_memory = np.median(memory_usage)

    total_memory = memory_info.total / (1024 ** 2)  # Convert to MB

    print(f"CPU Usage over 5 minutes:")
    print(f"Max CPU: {max_cpu:.1f}%")
    print(f"Min CPU: {min_cpu:.1f}%")
    print(f"Average CPU: {avg_cpu:.1f}%")
    print(f"Median CPU: {median_cpu:.1f}%\n")
    
    print(f"Memory Usage over 5 minutes:")
    print(f"Max Memory: {max_memory:.1f}% ({max_memory * total_memory / 100:.2f} MB)")
    print(f"Min Memory: {min_memory:.1f}% ({min_memory * total_memory / 100:.2f} MB)")
    print(f"Average Memory: {avg_memory:.1f}% ({avg_memory * total_memory / 100:.2f} MB)")
    print(f"Median Memory: {median_memory:.1f}% ({median_memory * total_memory / 100:.2f} MB)\n")

    # Top 10 Memory-consuming processes
    processes_memory = [(proc.info['pid'], proc.info['name'], proc.info['memory_percent']) 
                        for proc in psutil.process_iter(['pid', 'name', 'memory_percent'])]
    processes_memory = sorted(processes_memory, key=lambda p: p[2], reverse=True)[:10]

    print(f"Top 10 memory-consuming processes (Memory % and MB):")
    for pid, name, memory_percent in processes_memory:
        memory_used_mb = memory_percent * total_memory / 100
        print(f"{name} (PID: {pid}) - Memory: {memory_percent:.1f}% ({memory_used_mb:.2f} MB)")

    # Top 10 CPU-consuming processes
    processes_cpu = [(proc.info['pid'], proc.info['name'], proc.info['cpu_percent']) 
                     for proc in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
    processes_cpu = sorted(processes_cpu, key=lambda p: p[2], reverse=True)[:10]

    print(f"\nTop 10 CPU-consuming processes:")
    for pid, name, cpu_percent in processes_cpu:
        print(f"{name} (PID: {pid}) - CPU: {cpu_percent:.1f}%")

    # Disk storage usage
    disk_usage = psutil.disk_usage('/')
    disk_total_gb = disk_usage.total / (1024 ** 3)
    disk_used_gb = disk_usage.used / (1024 ** 3)
    disk_free_gb = disk_usage.free / (1024 ** 3)
    disk_percent = disk_usage.percent

    print(f"\nDisk Storage Information:")
    print(f"Total Disk Space: {disk_total_gb:.2f} GB")
    print(f"Used Disk Space: {disk_used_gb:.2f} GB")
    print(f"Available Disk Space: {disk_free_gb:.2f} GB")
    print(f"Disk Usage: {disk_percent:.1f}%\n")

    # Prepare CSV output
    csv_output = io.StringIO()
    writer = csv.writer(csv_output)

    # Write headers
    writer.writerow(['Max CPU (%)', 'Min CPU (%)', 'Avg CPU (%)', 'Median CPU (%)', 
                     'Max Memory (%)', 'Min Memory (%)', 'Avg Memory (%)', 'Median Memory (%)', 
                     'Total Memory (MB)', 'Disk Total (GB)', 'Disk Used (GB)', 'Disk Free (GB)', 'Disk Usage (%)'])
    writer.writerow([f"{max_cpu:.1f}", f"{min_cpu:.1f}", f"{avg_cpu:.1f}", f"{median_cpu:.1f}", 
                     f"{max_memory:.1f}", f"{min_memory:.1f}", f"{avg_memory:.1f}", f"{median_memory:.1f}", 
                     f"{total_memory:.1f}", f"{disk_total_gb:.2f}", f"{disk_used_gb:.2f}", f"{disk_free_gb:.2f}", f"{disk_percent:.1f}"])

    # Add top 10 memory-consuming processes to CSV
    writer.writerow([])
    writer.writerow(['Top 10 Memory-consuming Processes', 'PID', 'Memory (%)', 'Memory (MB)'])
    for pid, name, memory_percent in processes_memory:
        memory_used_mb = memory_percent * total_memory / 100
        writer.writerow([name, pid, f"{memory_percent:.1f}", f"{memory_used_mb:.2f}"])

    # Add top 10 CPU-consuming processes to CSV
    writer.writerow([])
    writer.writerow(['Top 10 CPU-consuming Processes', 'PID', 'CPU (%)'])
    for pid, name, cpu_percent in processes_cpu:
        writer.writerow([name, pid, f"{cpu_percent:.1f}"])

    # Print CSV to screen (at the end)
    print("\nCSV Output:\n")
    print(csv_output.getvalue())

if __name__ == "__main__":
    monitor_cpu_memory()

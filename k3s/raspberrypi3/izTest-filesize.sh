#!/bin/bash

# Initialize total file size
total_size=0

# Add directories and files to the array
pathCount=(
    "/edge/"
    "/lib/systemd/system/coredns.service"
    "/lib/systemd/system/coredns-starter.service"
)

# Function to calculate file sizes
calculate_size() {
    local path=$1
    # Check if the path is a directory
    if [ -d "$path" ]; then
        # Use du to calculate the size of the directory and its contents in bytes
        dir_size=$(du -sb "$path" | awk '{print $1}')
        total_size=$((total_size + dir_size))
    elif [ -f "$path" ]; then
        # If it's a file, get the file size in bytes
        file_size=$(stat -c %s "$path")
        total_size=$((total_size + file_size))
    else
        echo "Warning: $path is not a valid file or directory."
    fi
}

# Loop through all paths in the pathCount array
for path in "${pathCount[@]}"; do
    calculate_size "$path"
done

# Convert the total size from bytes to gigabytes for a more readable format
total_size_gb=$(echo "scale=2; $total_size / (1024 * 1024 * 1024)" | bc)

# Print total file size in gigabytes
echo "Total file size: $total_size_gb GB"

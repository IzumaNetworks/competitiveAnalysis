#!/usr/bin/env bash

# First-time setup
first_time_test() {
    sudo swapoff -a
    sudo apt update
    sudo apt install -y emacs curl python3-pip
    sudo systemctl enable ssh
    sudo sed -i 's/^\(CONF_SWAPSIZE=\).*/\10/' /etc/dphys-swapfile
    sudo sed -i 's/$/ cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory/' /boot/firmware/cmdline.txt
    sudo touch /var/run/first_time_test_done
}
#!/bin/bash

# Function to get the IP address of the physical network interface
get_physical_ip() {
    physical_ip=$(ip -o -4 addr show eth0 | awk '{print $4}' | cut -d/ -f1)
    echo "${physical_ip}"
}

# Second run
second_go() {
    fetchIP=$(get_physical_ip)
    echo "IP address: ${fetchIP}"
    curl -sfL https://get.k3s.io | sh -
    sudo systemctl status k3s.service

}

# Check if first-time setup is needed
if [[ ! -f /var/run/first_time_test_done ]]; then
    echo "Running first-time setup..."
    first_time_test
    sudo reboot
else
    second_go
fi

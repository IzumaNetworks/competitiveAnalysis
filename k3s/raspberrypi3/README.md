# K3s on RPI B4+

# prereq

- Install PIos with with the (pi OS installer)[https://www.raspberrypi.com/software/]
  - choose: Raspberry PI OS Other -> PI OS Lite (64)
  - burn to an SD card
- Get ssh access working.  PI os is annoying in that you need a monitor and keyboard first...
  - sudo systemctl enable ssh
  - sudo systemctl start ssh

# Install k3s (single node)

- scp setupk3s.sh to the pi
- run it
- reboot
- run it again

# Tests

## 1 Boot time

In order to conduct this test, we installed k3s onto a raspberry pi 3b+ following the instructions provided on the web.   We installed Izuma Edge Yocto build for RP3b+ onto an adjacent and equivalent Raspberry pi 3b+ and timed their boot time to login prompt, from a cold start, then followed from a warm start (with a sudo init 6).

### k3s

Hook up a monitor as the recommended setup involves a screen and keyboard.  Press power and your stopwatch at the same time.  Monitor the screen until you see a login prompt.

### Izuma Edge

Hook up a serial port to the RPI.  Press power and your stopwatch at the same time.  Because were using a serial port, you need press enter every second or so after 20 seconds to reproduce the results.  Around 26 seconds you should get the login prompt.

## memory footprint

System memory is vital for an edge machine.  The more free memory the more room to run customer applications.  Its very important to control memory for edge services.

### k3s

Before starting / installing k3s, use htop to establish the baseline for memory.


### Izuma Edge

Built into Izuma Edge is a program that calcuates used memory.  Simply run the command:
```sudo edge-info -m```
this will results in the following memory footprint output:

```bash
Key Process Memory Information (MB)
  Stats in megabytes (MB)	Pss	Shared	Rss	Virtual
  - edge-core (592):		3.7	2.9	6.3	80.0
  - edge-proxy (597):		36.5	1.4	37.9	1237.6
  - maestro (609):		18.6	1.0	19.6	1357.5
  - fluentbit (608):		5.6	5.3	10.0	147.3
  - edge-kubelet (605):		64.1	1.3	65.4	1604.0
  - kube-router (614):		45.3	.9	46.2	1383.9
  - docker (590):		73.2	1.6	74.8	1402.6

System Memory
  				Totals		Percentage
  - Used/Total:			277/933 MB	29.68%
  - Key Processes:		247.0 MB	26.47%
  - Volatile logging:		1 MB		.10%
  - True Available Mem:		656 MB		70.31%
```

## CPU and memory avaialbity  anlysis

There are 4 stages that we want to test to understand the differences between k3s and Izuma Edge. Each stage is necessary to properly understand what is happening to the system and the impacts of the services.
Stage 1: baseline.  This is the operating system running on the device without actually runiing the edge software.
Stage 2: Edge software.  The software we are running on the 



Before we load the system, we need to establish the baseline.  How much of the CPU is being consumed by the application and how much is available for use by the containers.  to estblish a baseline, we will log memory and cpu utilization and produce a chart of maximum, minimum and medium. 



### k3s
```bash
sudo apt install python3-pip
sudo apt install -y python3-psutil
sudo apt install -y python3-numpy
```
secure copy the the program in this folder `monitor.py` to the machine and run it.  It will run for 5 minutes and then output the results.


```bash
Monitoring system for 5 minutes...

CPU Usage over 5 minutes:
Max CPU: 9.7%
Min CPU: 1.6%
Average CPU: 2.3193333333333332%
Median CPU: 2.1%

Memory Usage over 5 minutes:
Max Memory: 19.7%
Min Memory: 19.2%
Average Memory: 19.420666666666666%
Median Memory: 19.5%

Top 10 Memory Consuming Processes (Median, Max):
python3: Median Memory: 3.41%, Max Memory: 3.45%
NetworkManager: Median Memory: 2.04%, Max Memory: 2.04%
exim4: Median Memory: 1.71%, Max Memory: 1.71%
systemd-journald: Median Memory: 1.54%, Max Memory: 1.54%
ModemManager: Median Memory: 1.20%, Max Memory: 1.20%
systemd: Median Memory: 1.15%, Max Memory: 1.22%
wpa_supplicant: Median Memory: 1.10%, Max Memory: 1.10%
sshd: Median Memory: 0.90%, Max Memory: 1.03%
systemd-logind: Median Memory: 0.77%, Max Memory: 0.77%
systemd-timesyncd: Median Memory: 0.74%, Max Memory: 0.74%

Top 10 CPU Consuming Processes (Median, Max):
python3: Median CPU: 8.30%, Max CPU: 13.20%
kworker/2:1H-kblockd: Median CPU: 0.90%, Max CPU: 0.90%
kworker/u8:1-ext4-rsv-conversion: Median CPU: 0.90%, Max CPU: 0.90%
rcu_preempt: Median CPU: 0.90%, Max CPU: 0.90%
kworker/0:2-events_power_efficient: Median CPU: 0.90%, Max CPU: 0.90%
kworker/1:3-events_freezable_power_: Median CPU: 0.90%, Max CPU: 0.90%
kworker/0:2-events: Median CPU: 0.90%, Max CPU: 0.90%
kworker/u13:2-brcmf_wq/mmc1:0001:1: Median CPU: 0.90%, Max CPU: 0.90%
brcmf_wdog/mmc1:0001:1: Median CPU: 0.90%, Max CPU: 0.90%
kworker/2:1-events: Median CPU: 0.90%, Max CPU: 0.90%
```

### Izuma Edge

Install pyton.
```bash
python3 -m ensurepip --upgrade
python3 -m pip install psutil
python3 -m pip install numpy
python3 -m pip install --upgrade pip
```

secure copy the the program in this folder `monitor.py` to the machine and run it.  It will run for 5 minutes and then output the results.
and run the program
```bash
fio@raspberrypi3-64:~$ python3 monitor.py
Monitoring system for 5 minutes...

CPU Usage over 5 minutes:
Max CPU: 42.1%
Min CPU: 3.4%
Average CPU: 5.864333333333334%
Median CPU: 5.4%

Memory Usage over 5 minutes:
Max Memory: 30.6%
Min Memory: 30.3%
Average Memory: 30.453%
Median Memory: 30.4%

Top 10 Memory Consuming Processes (Median, Max):
dockerd: Median Memory: 8.12%, Max Memory: 8.12%
kubelet: Median Memory: 7.22%, Max Memory: 7.26%
containerd: Median Memory: 5.58%, Max Memory: 5.58%
kube-router: Median Memory: 4.98%, Max Memory: 4.98%
edge-proxy: Median Memory: 4.25%, Max Memory: 4.30%
python3: Median Memory: 2.61%, Max Memory: 2.66%
maestro: Median Memory: 2.06%, Max Memory: 2.06%
NetworkManager: Median Memory: 1.16%, Max Memory: 1.16%
systemd: Median Memory: 1.12%, Max Memory: 1.24%
td-agent-bit: Median Memory: 1.10%, Max Memory: 1.11%

Top 10 CPU Consuming Processes (Median, Max):
python3: Median CPU: 10.70%, Max CPU: 13.10%
kubelet: Median CPU: 5.30%, Max CPU: 23.60%
parsec: Median CPU: 0.90%, Max CPU: 1.80%
dockerd: Median CPU: 0.90%, Max CPU: 7.20%
rcu_preempt: Median CPU: 0.90%, Max CPU: 0.90%
kworker/2:0-events: Median CPU: 0.90%, Max CPU: 0.90%
kworker/0:0-events: Median CPU: 0.90%, Max CPU: 0.90%
kworker/3:2-events: Median CPU: 0.90%, Max CPU: 0.90%
kworker/1:0-events: Median CPU: 0.90%, Max CPU: 0.90%
kworker/3:1H-mmc_complete: Median CPU: 0.90%, Max CPU: 0.90%
```


## Change the IP address

Machines should support changing / floating ip addresses.  When machines are deployed outside of your network, outside a subnet that you control, the machine software needs to be robust enough to support ip addresses changing; because the machine is out of your physical control.

### k3s

change the static or dhcp server such that the machine gets a new ip address on the same subnet as before.  Ensure k3s can come up
**results** Failed.  k3s will not start under a new IP address

### Izuma Edge

change the static or dhcp server such that the machine gets a new ip address on the same subnet as before.  Ensure k3s can come up
**results** success.  Izuma Edge always calls back to the cloud and establishes connection.

## Install hardware behind basic NAT and Firewall

Machines are placed all over the world behind many different networks.  They should be able to connect back to your management plane without additional software

### k3s

Place behind a firewall.  It will not be able to connect to your management infrastructure.  It will require additional technology to manage this node.

### Izuma Edge

Izuma Edge has built in edge proxy tunneling technology.  You can deploy an Izuma Edge node anywhere that can access the internet.  It will connect to the Kubernetes control plane, through complex packet inspecting firewalls and extreme NAT environments.

# Analysis

## Results

Up front, I will provide the results of the test.  This was conducted head to head with like Raspberry PI 3b+ machines, which is a constrained device with a process and memory that you would typically find in a modern building controller, car head unit, or dedicated processor environement.  For reach test conducted, you will find in the test section above.


| Description                               |  k3s  |     Izuma Edge     |
| :------------------------------------------ | :-----: | :------------------: |
| Boot time (cold start)                    |  38s  |        26s        |
| Boot time (restart)                       | 2m 8s |        32s        |
| Memory consumed (true)                    |       |        260M        |
| (Before Edge SW) Memory consumed (free -h)|  97MB |       NA*       |
| (Edge SW) Memory consumed (free -h)       |       |       199MB       |
| Memory avaiable for customer applications |       |    656 (70.31%)    |
| (Before Edge SW) Top cpu consumer         |       |    656 (70.31%)    |
| Survive IP address change                 |  :x:  | :white_check_mark: |
| Operate behind a simple firewall          |  :x:  | :white_check_mark: |
| Operate behind a complex firewall         |  :x:  | :white_check_mark: |

* Izuma Edge Yocto OS always contains the Edge Software
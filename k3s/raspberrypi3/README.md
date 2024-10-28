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

# Results

Up front, I will provide the results of the test.  This was conducted head to head with like Raspberry PI 3b+ machines, which is a constrained device with a process and memory that you would typically find in a modern building controller, car head unit, or dedicated processor environement.  For reach test conducted, you will find in the test section above.


| Description                                  |    k3s    |     Izuma Edge     |
| :--------------------------------------------- | :---------: | :------------------: |
| System starting memory (hardware)            |  1028MB  |       1028MB       |
| Boot time (cold start)                       |    38s    |        26s        |
| Boot time (restart)                          |   2m 8s   |        32s        |
| Memory avaiable w/o edgeSW (no containers)   |  773 MB    |       741 MB       |
| Memory available w edgeSW (no containers)    |   232 MB   |       681 MB       |
| Memory taken up by edgeSW (no containers)    |   501 MB  |       80 MB       |
| Disk space used w/o edgeSW (no containers)   |  2.3 GB   |       714 MB       |
| Disk space used w edgeSW (no containers)    |   3.6 GB   |       976 MB       |
| Disk space taken up by edgeSW (no containers)   | 1.3 GB  |      262 MB        |
| CPU Idle Min/Max/Avg (5 min capture)             | 1% / 25% / 5% |    .8% / 14.1% / 3.2%    |
| Memory consumed Idle Min/Max (5 min capture) | 75% / 75% |     31% / 31%     |
| Survive IP address change                    |    :x:    | :white_check_mark: |
| Operate behind a simple firewall             |    :x:    | :white_check_mark: |
| Operate behind a complex firewall            |    :x:    | :white_check_mark: |

* Izuma Edge Yocto OS always contains the Edge Software.  TODO: build without Izuma Edge

# Tests

## 1 Boot time

In order to conduct this test, we installed k3s onto a raspberry pi 3b+ following the instructions provided on the web.   We installed Izuma Edge Yocto build for RP3b+ onto an adjacent and equivalent Raspberry pi 3b+ and timed their boot time to login prompt, from a cold start, then followed from a warm start (with a sudo init 6).

### k3s

Hook up a monitor as the recommended setup involves a screen and keyboard.  Press power and your stopwatch at the same time.  Monitor the screen until you see a login prompt.

### Izuma Edge

Hook up a serial port to the RPI.  Press power and your stopwatch at the same time.  Because were using a serial port, you need press enter every second or so after 20 seconds to reproduce the results.  Around 26 seconds you should get the login prompt.

## 2 CPU and memory availability  analysis

There are 4 stages that we want to test to understand the differences between k3s and Izuma Edge. Each stage is necessary to properly understand what is happening to the system and the impacts of the services.
Stage 1: baseline.  This is the operating system running on the device without actually running the edge software.
Stage 2: Edge software.  The software ran to provide Edge functionality.  For the k3s case, this is all of the k3s binaries.  For the Izuma Edge case, this is all of the binaries needed to run izuma edge.
Stage 3: Edge software with one hello world container deployed.
Stage 4: Deploy (n) containers until the system becomes non-responsive.

### Stage 1: baseline w/o edge software

Install everything needed up to the point just before installing the edge software. (e.g. update the OS etc).  Take a baseline survey of the system health using the provided python monitoring script `monitor.py`.  Note, installation of the python varies between Izuma Edge and k3s due to base OS differences.  See section below

#### k3s

1. Python installation & test script:

```bash
sudo apt install python3-pip
sudo apt install -y python3-psutil
sudo apt install -y python3-numpy
```

secure copy the the program in this folder `monitor.py` to the machine and run it.  It will run for 5 minutes and then output the results.
2. Run the test and publish the results

```bash
travis@raspberrypi:~ $ python monitor.py
Monitoring system for 5 minutes...

CPU Usage over 5 minutes:
Max CPU: 4.8%
Min CPU: 0.0%
Average CPU: 0.1%
Median CPU: 0.0%

Memory Usage over 5 minutes:
Max Memory: 18.4% (166.95 MB)
Min Memory: 17.8% (161.50 MB)
Average Memory: 18.1% (163.78 MB)
Median Memory: 18.1% (164.23 MB)

Top 10 memory-consuming processes (Memory % and MB):
python (PID: 1105) - Memory: 3.4% (30.41 MB)
NetworkManager (PID: 520) - Memory: 2.1% (18.75 MB)
exim4 (PID: 927) - Memory: 1.7% (15.59 MB)
systemd-journald (PID: 242) - Memory: 1.6% (14.12 MB)
systemd (PID: 1) - Memory: 1.2% (11.05 MB)
ModemManager (PID: 530) - Memory: 1.2% (10.88 MB)
wpa_supplicant (PID: 523) - Memory: 1.1% (9.87 MB)
systemd (PID: 1055) - Memory: 1.1% (9.87 MB)
sshd (PID: 1051) - Memory: 1.0% (9.50 MB)
sshd (PID: 602) - Memory: 0.9% (8.38 MB)

Top 10 CPU-consuming processes:
systemd (PID: 1) - CPU: 0.0%
kthreadd (PID: 2) - CPU: 0.0%
pool_workqueue_release (PID: 3) - CPU: 0.0%
kworker/R-rcu_g (PID: 4) - CPU: 0.0%
kworker/R-rcu_p (PID: 5) - CPU: 0.0%
kworker/R-slub_ (PID: 6) - CPU: 0.0%
kworker/R-netns (PID: 7) - CPU: 0.0%
kworker/0:0H-events_highpri (PID: 9) - CPU: 0.0%
kworker/u8:0-ext4-rsv-conversion (PID: 11) - CPU: 0.0%
kworker/R-mm_pe (PID: 12) - CPU: 0.0%

Disk Storage Information:
Total Disk Space: 14.05 GB
Used Disk Space: 2.20 GB
Available Disk Space: 11.12 GB
Disk Usage: 16.5%


CSV Output:

Max CPU (%),Min CPU (%),Avg CPU (%),Median CPU (%),Max Memory (%),Min Memory (%),Avg Memory (%),Median Memory (%),Total Memory (MB),Disk Total (GB),Disk Used (GB),Disk Free (GB),Disk Usage (%)
4.8,0.0,0.1,0.0,18.4,17.8,18.1,18.1,907.3,14.05,2.20,11.12,16.5

Top 10 Memory-consuming Processes,PID,Memory (%),Memory (MB)
python,1105,3.4,30.41
NetworkManager,520,2.1,18.75
exim4,927,1.7,15.59
systemd-journald,242,1.6,14.12
systemd,1,1.2,11.05
ModemManager,530,1.2,10.88
wpa_supplicant,523,1.1,9.87
systemd,1055,1.1,9.87
sshd,1051,1.0,9.50
sshd,602,0.9,8.38

Top 10 CPU-consuming Processes,PID,CPU (%)
systemd,1,0.0
kthreadd,2,0.0
pool_workqueue_release,3,0.0
kworker/R-rcu_g,4,0.0
kworker/R-rcu_p,5,0.0
kworker/R-slub_,6,0.0
kworker/R-netns,7,0.0
kworker/0:0H-events_highpri,9,0.0
kworker/u8:0-ext4-rsv-conversion,11,0.0
kworker/R-mm_pe,12,0.0
```

3. capture a memory footprint with free -h
travis@raspberrypi:~ $ free -m
               total        used        free      shared  buff/cache   available
Mem:             907         134         449           1         375         773
Swap:            199           0         199


4. Capture an output of the file system used with the following command

```bash
travis@raspberrypi:/ $ sudo du -cksh *
0	bin
105M	boot
0	dev
5.0M	etc
60K	home
0	lib
16K	lost+found
4.0K	media
4.0K	mnt
12K	opt
0	proc
16K	root
1.1M	run
0	sbin
4.0K	srv
0	sys
56K	tmp
1.9G	usr
330M	var
2.3G	total
```

### Izuma Edge

Download and burn Izuma Edge software for the RPI B3+.  Because this image is a tailored image for a RPI based on linux micro platform, Izuma Edge is pre installed, and runs on boot.  To accommodate this we built  build a custom version without our Edge software.

1. burn the custom image onto a SD card, install it in the RPI and boot to a linux prompt
2. Python installation

```bash
python3 -m ensurepip --upgrade
python3 -m pip install psutil
python3 -m pip install numpy
python3 -m pip install --upgrade pip
```

3. secure copy the the program in this folder `monitor.py` to the machine and run it.  It will run for 5 minutes and then output the results.
4. Run the test and publish the results

```bash
fio@raspberrypi3-64:~$ python3 monitor.py
Monitoring system for 5 minutes...

CPU Usage over 5 minutes:
Max CPU: 9.2%
Min CPU: 0.0%
Average CPU: 0.3%
Median CPU: 0.0%

Memory Usage over 5 minutes:
Max Memory: 18.8% (171.33 MB)
Min Memory: 18.8% (171.33 MB)
Average Memory: 18.8% (171.33 MB)
Median Memory: 18.8% (171.33 MB)

Top 10 memory-consuming processes (Memory % and MB):
dockerd (PID: 651) - Memory: 7.3% (66.32 MB)
containerd (PID: 610) - Memory: 5.5% (49.95 MB)
python3 (PID: 876) - Memory: 2.7% (24.62 MB)
NetworkManager (PID: 592) - Memory: 1.2% (10.54 MB)
systemd (PID: 1) - Memory: 1.1% (10.48 MB)
systemd-resolved (PID: 499) - Memory: 1.1% (9.59 MB)
systemd (PID: 789) - Memory: 1.0% (9.04 MB)
systemd-journald (PID: 418) - Memory: 0.9% (8.15 MB)
wpa_supplicant (PID: 627) - Memory: 0.9% (8.07 MB)
sshd (PID: 861) - Memory: 0.8% (7.65 MB)

Top 10 CPU-consuming processes:
systemd (PID: 1) - CPU: 0.0%
kthreadd (PID: 2) - CPU: 0.0%
rcu_gp (PID: 3) - CPU: 0.0%
rcu_par_gp (PID: 4) - CPU: 0.0%
mm_percpu_wq (PID: 8) - CPU: 0.0%
rcu_tasks_kthre (PID: 9) - CPU: 0.0%
rcu_tasks_rude_ (PID: 10) - CPU: 0.0%
rcu_tasks_trace (PID: 11) - CPU: 0.0%
ksoftirqd/0 (PID: 12) - CPU: 0.0%
rcu_preempt (PID: 13) - CPU: 0.0%

Disk Storage Information:
Total Disk Space: 13.94 GB
Used Disk Space: 0.69 GB
Available Disk Space: 12.63 GB
Disk Usage: 5.2%


CSV Output:

Max CPU (%),Min CPU (%),Avg CPU (%),Median CPU (%),Max Memory (%),Min Memory (%),Avg Memory (%),Median Memory (%),Total Memory (MB),Disk Total (GB),Disk Used (GB),Disk Free (GB),Disk Usage (%)
9.2,0.0,0.3,0.0,18.8,18.8,18.8,18.8,911.3,13.94,0.69,12.63,5.2

Top 10 Memory-consuming Processes,PID,Memory (%),Memory (MB)
dockerd,651,7.3,66.32
containerd,610,5.5,49.95
python3,876,2.7,24.62
NetworkManager,592,1.2,10.54
systemd,1,1.1,10.48
systemd-resolved,499,1.1,9.59
systemd,789,1.0,9.04
systemd-journald,418,0.9,8.15
wpa_supplicant,627,0.9,8.07
sshd,861,0.8,7.65

Top 10 CPU-consuming Processes,PID,CPU (%)
systemd,1,0.0
kthreadd,2,0.0
rcu_gp,3,0.0
rcu_par_gp,4,0.0
mm_percpu_wq,8,0.0
rcu_tasks_kthre,9,0.0
rcu_tasks_rude_,10,0.0
rcu_tasks_trace,11,0.0
ksoftirqd/0,12,0.0
rcu_preempt,13,0.0
```
5. Capture the memory footprint with free -h
```bash
fio@raspberrypi3-64:/$ free -h
               total        used        free      shared  buff/cache   available
Mem:           911Mi       101Mi       229Mi        36Mi       579Mi       741Mi
Swap:          889Mi          0B       889Mi
```

5. Capture an output of the file system used with the following command

```bash
fio@raspberrypi3-64:/$ sudo du -cksh *
0	bin
14.0M	boot
0	dev
24.0K	edge
2.4M	etc
0	home
0	lib
0	media
0	mnt
0	opt
0	ostree
0	proc
9.6M	run
0	sbin
0	srv
0	sys
688.2M	sysroot
0	tmp
714.2M	total
```

### Stage 2: baseline w/edge software Idle

Install the edge software. Measure.

#### k3s

Upload the script `setupk3s.sh` to the target raspberry PI.  Run it.  Note, you need to run it twice as the script sets certain boot prarameters.

1. run setupk3s.sh
2. script will automatically reboot
3. run setupk3s.sh again
4. script will leave you in a `systemctl status k3s.service`
5. after completion, ensure everything is working with a `kubectl get nodes`.  If it doesn't, reboot one more time.  continue after you have `kubectl get nodes` working.
6. measure with our monitor.py script.  Here is an instantiation  of this along with the results

```bash
travis@raspberrypi:~ $ python monitor.py
Monitoring system for 5 minutes...

CPU Usage over 5 minutes:
Max CPU: 25.6%
Min CPU: 1.0%
Average CPU: 5.0%
Median CPU: 4.6%

Memory Usage over 5 minutes:
Max Memory: 76.3% (692.29 MB)
Min Memory: 75.5% (685.03 MB)
Average Memory: 76.1% (690.16 MB)
Median Memory: 76.1% (690.47 MB)

Top 10 memory-consuming processes (Memory % and MB):
k3s-server (PID: 724) - Memory: 45.1% (409.37 MB)
containerd (PID: 955) - Memory: 7.9% (71.75 MB)
traefik (PID: 2662) - Memory: 4.1% (36.88 MB)
metrics-server (PID: 2208) - Memory: 3.6% (32.45 MB)
python (PID: 19702) - Memory: 3.3% (30.26 MB)
coredns (PID: 2223) - Memory: 2.2% (20.27 MB)
exim4 (PID: 926) - Memory: 1.5% (14.00 MB)
local-path-provisioner (PID: 2152) - Memory: 1.3% (11.36 MB)
sshd (PID: 19681) - Memory: 1.0% (8.75 MB)
containerd-shim-runc-v2 (PID: 1778) - Memory: 0.8% (7.00 MB)

Top 10 CPU-consuming processes:
systemd (PID: 1) - CPU: 0.0%
kthreadd (PID: 2) - CPU: 0.0%
pool_workqueue_release (PID: 3) - CPU: 0.0%
kworker/R-rcu_g (PID: 4) - CPU: 0.0%
kworker/R-rcu_p (PID: 5) - CPU: 0.0%
kworker/R-slub_ (PID: 6) - CPU: 0.0%
kworker/R-netns (PID: 7) - CPU: 0.0%
kworker/0:0H-kblockd (PID: 9) - CPU: 0.0%
kworker/u8:0-ext4-rsv-conversion (PID: 11) - CPU: 0.0%
kworker/R-mm_pe (PID: 12) - CPU: 0.0%

Disk Storage Information:
Total Disk Space: 14.05 GB
Used Disk Space: 3.19 GB
Available Disk Space: 10.13 GB
Disk Usage: 24.0%


CSV Output:

Max CPU (%),Min CPU (%),Avg CPU (%),Median CPU (%),Max Memory (%),Min Memory (%),Avg Memory (%),Median Memory (%),Total Memory (MB),Disk Total (GB),Disk Used (GB),Disk Free (GB),Disk Usage (%)
25.6,1.0,5.0,4.6,76.3,75.5,76.1,76.1,907.3,14.05,3.19,10.13,24.0

Top 10 Memory-consuming Processes,PID,Memory (%),Memory (MB)
k3s-server,724,45.1,409.37
containerd,955,7.9,71.75
traefik,2662,4.1,36.88
metrics-server,2208,3.6,32.45
python,19702,3.3,30.26
coredns,2223,2.2,20.27
exim4,926,1.5,14.00
local-path-provisioner,2152,1.3,11.36
sshd,19681,1.0,8.75
containerd-shim-runc-v2,1778,0.8,7.00

Top 10 CPU-consuming Processes,PID,CPU (%)
systemd,1,0.0
kthreadd,2,0.0
pool_workqueue_release,3,0.0
kworker/R-rcu_g,4,0.0
kworker/R-rcu_p,5,0.0
kworker/R-slub_,6,0.0
kworker/R-netns,7,0.0
kworker/0:0H-kblockd,9,0.0
kworker/u8:0-ext4-rsv-conversion,11,0.0
kworker/R-mm_pe,12,0.0
```

7.. Measure with free -h
```bash
total        used        free      shared  buff/cache   available
Mem:           907Mi       676Mi       151Mi       2.0Mi       131Mi       231Mi
Swap:             0B          0B          0B
```

8. Measure with du -cksh
``` bash
travis@raspberrypi:/ $ sudo du -cksh *
0	bin
105M	boot
0	dev
5.0M	etc
440K	home
0	lib
16K	lost+found
4.0K	media
4.0K	mnt
12K	opt
0	proc
24K	root
158M	run
0	sbin
4.0K	srv
0	sys
60K	tmp
1.9G	usr
1.5G	var
3.6G	total
```

### Izuma Edge

1. Deploy the Izuma Edge image by buring the SD card.
2. ensure Izuma Edge is connected by running edge-info.  Look for the connected status at the bottom

```bash
fio@raspberrypi3-64:~$ edge-info


Edge Information utility version 2.2.0

System Information
  - Uptime:			9h 57m 44s
  - Users:			1 users
  - Load (1,5,15-min avg):	0.12, 0.10, 0.09
  - Queued Tasks:		1/209
  - IP Addresses:		172.17.0.1
				172.28.28.72
				172.21.1.0

Geographic Information
  - Public IP:			72.177.90.56
  - City:			Austin
  - Region:			Texas
  - Country:			US
  - Postal:			78746
  - Lat/Long:			30.2971,-97.8181
  - organization:		AS11427 Charter Communications Inc
\u001b[0m

Firmware Version Information
  - Pelion Edge Version:	2.6.0-WiP
    - edge-core			0.21.0
  - OS:				LMP (64 bit)
  - OS Version:			Linux-microPlatform 4.0.5
  - OS Machine:			raspberrypi3-64
  - Kernel Version:		5.10.83-lmp-standard

Hardware Information
  - Hardware name:		Raspberry Pi 3 Model B Plus Rev 1.3
  - Physical Memory:		933 MB
  - Temperatures:
    - thermal zone0:		45.1 C
  - CPU Count:			4
  - CPU Stats:			       Current         Minimum         Maximum
    - CPU0:			      1100 Mhz         600 Mhz        1400 Mhz
    - CPU1:			      1100 Mhz         600 Mhz        1400 Mhz
    - CPU2:			      1000 Mhz         600 Mhz        1400 Mhz
    - CPU3:			      1100 Mhz         600 Mhz        1400 Mhz

Account Information
  - AccountID:			0192af77b74bb606f785dd2600000000
  - Device ID:			0192b7b59d94122f8542fe1f00000000
  - LwM2M Service:		coaps://tcp-lwm2m.us-east-1.mbedcloud.com:5684
  - Gateway Service:		https://gateways.us-east-1.mbedcloud.com
  - K8s Service:		https://edge-k8s.us-east-1.mbedcloud.com
  - Container Service:		https://containers.us-east-1.mbedcloud.com
  - Status:			connected
```

3. Measure with our monitor.py script.  Here is an instantiation  of this along with the results

```bash
fio@raspberrypi3-64:~$ python3 monitor.py
Monitoring system for 5 minutes...

CPU Usage over 5 minutes:
Max CPU: 14.1%
Min CPU: 0.8%
Average CPU: 3.2%
Median CPU: 2.6%

Memory Usage over 5 minutes:
Max Memory: 31.6% (287.98 MB)
Min Memory: 31.1% (283.43 MB)
Average Memory: 31.3% (285.12 MB)
Median Memory: 31.4% (286.16 MB)

Top 10 memory-consuming processes (Memory % and MB):
dockerd (PID: 686) - Memory: 8.2% (74.32 MB)
kubelet (PID: 2454) - Memory: 7.5% (68.03 MB)
containerd (PID: 618) - Memory: 5.6% (50.93 MB)
kube-router (PID: 2446) - Memory: 5.0% (45.72 MB)
edge-proxy (PID: 2449) - Memory: 4.7% (42.50 MB)
python3 (PID: 90743) - Memory: 2.7% (24.73 MB)
maestro (PID: 2459) - Memory: 2.1% (19.24 MB)
systemd-journald (PID: 417) - Memory: 1.8% (16.56 MB)
td-agent-bit (PID: 2732) - Memory: 1.5% (14.01 MB)
systemd (PID: 1) - Memory: 1.3% (11.71 MB)

Top 10 CPU-consuming processes:
systemd (PID: 1) - CPU: 0.0%
kthreadd (PID: 2) - CPU: 0.0%
rcu_gp (PID: 3) - CPU: 0.0%
rcu_par_gp (PID: 4) - CPU: 0.0%
mm_percpu_wq (PID: 8) - CPU: 0.0%
rcu_tasks_kthre (PID: 9) - CPU: 0.0%
rcu_tasks_rude_ (PID: 10) - CPU: 0.0%
rcu_tasks_trace (PID: 11) - CPU: 0.0%
ksoftirqd/0 (PID: 12) - CPU: 0.0%
rcu_preempt (PID: 13) - CPU: 0.0%

Disk Storage Information:
Total Disk Space: 13.89 GB
Used Disk Space: 0.90 GB
Available Disk Space: 12.37 GB
Disk Usage: 6.8%


CSV Output:

Max CPU (%),Min CPU (%),Avg CPU (%),Median CPU (%),Max Memory (%),Min Memory (%),Avg Memory (%),Median Memory (%),Total Memory (MB),Disk Total (GB),Disk Used (GB),Disk Free (GB),Disk Usage (%)
14.1,0.8,3.2,2.6,31.6,31.1,31.3,31.4,911.3,13.89,0.90,12.37,6.8

Top 10 Memory-consuming Processes,PID,Memory (%),Memory (MB)
dockerd,686,8.2,74.32
kubelet,2454,7.5,68.03
containerd,618,5.6,50.93
kube-router,2446,5.0,45.72
edge-proxy,2449,4.7,42.50
python3,90743,2.7,24.73
maestro,2459,2.1,19.24
systemd-journald,417,1.8,16.56
td-agent-bit,2732,1.5,14.01
systemd,1,1.3,11.71

Top 10 CPU-consuming Processes,PID,CPU (%)
systemd,1,0.0
kthreadd,2,0.0
rcu_gp,3,0.0
rcu_par_gp,4,0.0
mm_percpu_wq,8,0.0
rcu_tasks_kthre,9,0.0
rcu_tasks_rude_,10,0.0
rcu_tasks_trace,11,0.0
ksoftirqd/0,12,0.0
rcu_preempt,13,0.0
```
4. Measure with free -h
```bash
fio@raspberrypi3-64:~$ free -h
               total        used        free      shared  buff/cache   available
Mem:           911Mi       187Mi       380Mi       9.0Mi       343Mi       681Mi
Swap:          889Mi          0B       889Mi
```

5. Measure with du -cksh *
```bash
0	bin
15M	boot
0	dev
169M	edge
2.5M	etc
0	home
0	lib
0	media
0	mnt
0	opt
0	ostree
0	proc
57M	run
0	sbin
0	srv
0	sys
734M	sysroot
0	tmp
976M	total
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

## Test responsiveness using basic commands with time

### Stage 1

run kubectl get nodes

### k3s

```bash
travis@raspberrypi:~ $ time kubectl get nodes
NAME          STATUS   ROLES                  AGE   VERSION
raspberrypi   Ready    control-plane,master   12m   v1.30.5+k3s1

real	0m11.901s
user	0m0.793s
sys	0m0.645s
travis@raspberrypi:~ $ time kubectl get nodes
NAME          STATUS   ROLES                  AGE   VERSION
raspberrypi   Ready    control-plane,master   12m   v1.30.5+k3s1

real	0m6.275s
user	0m0.683s
sys	0m0.579s
travis@raspberrypi:~ $ time kubectl get nodes
NAME          STATUS   ROLES                  AGE   VERSION
raspberrypi   Ready    control-plane,master   13m   v1.30.5+k3s1

real	0m36.072s
user	0m0.993s
sys	0m1.048s
travis@raspberrypi:~ $
```

### Izuma Edge

```bash
cypressMini:.kube travis$ time kubectl get nodes
NAME                               STATUS   ROLES    AGE    VERSION
0192af8a7e69122f8542fe1f00000000   Ready    <none>   39h    v1.13.2-argus
0192b50426f8ea3517f169ed00000000   Ready    <none>   14h    v1.13.2-argus
0192b50daa46ea3517f169ed00000000   Ready    <none>   14h    v1.13.2-argus
0192b7b59d94122f8542fe1f00000000   Ready    <none>   112m   v1.13.2-argus

real	0m0.392s
user	0m0.046s
sys	0m0.052s
cypressMini:.kube travis$ time kubectl get nodes
NAME                               STATUS   ROLES    AGE    VERSION
0192af8a7e69122f8542fe1f00000000   Ready    <none>   39h    v1.13.2-argus
0192b50426f8ea3517f169ed00000000   Ready    <none>   14h    v1.13.2-argus
0192b50daa46ea3517f169ed00000000   Ready    <none>   14h    v1.13.2-argus
0192b7b59d94122f8542fe1f00000000   Ready    <none>   112m   v1.13.2-argus

real	0m0.243s
user	0m0.057s
sys	0m0.027s
cypressMini:.kube travis$ time kubectl get nodes
NAME                               STATUS   ROLES    AGE    VERSION
0192af8a7e69122f8542fe1f00000000   Ready    <none>   39h    v1.13.2-argus
0192b50426f8ea3517f169ed00000000   Ready    <none>   14h    v1.13.2-argus
0192b50daa46ea3517f169ed00000000   Ready    <none>   14h    v1.13.2-argus
0192b7b59d94122f8542fe1f00000000   Ready    <none>   112m   v1.13.2-argus

real	0m0.221s
user	0m0.043s
sys	0m0.019s
```

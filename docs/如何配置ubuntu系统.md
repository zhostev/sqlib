# 如何配置ubuntu系统进行量化交易？

## 前述

最近家里的服务器系统启动不起来，索性进行重装，另外又买了一块硬盘。硬件是dell的5820，另外多加了一个3090的显卡。硬盘是一块4T的硬盘，一块是2T的硬盘，内存64G。

看一下是否需要进行配置

```
sudo apt list --upgradable
```

```
Listing... Done
gjs/jammy-updates 1.72.4-0ubuntu0.22.04.1 amd64 [upgradable from: 1.72.2-0ubuntu2]
libgjs0g/jammy-updates 1.72.4-0ubuntu0.22.04.1 amd64 [upgradable from: 1.72.2-0ubuntu2]
```

执行

```
df -h	
```

```
Filesystem                                        Size  Used Avail Use% Mounted on
tmpfs                                             6.3G  2.4M  6.3G   1% /run
rpool/ROOT/ubuntu_jaoz0k                          3.6T  3.6G  3.6T   1% /
tmpfs                                              32G     0   32G   0% /dev/shm
tmpfs                                             5.0M  4.0K  5.0M   1% /run/lock
rpool/ROOT/ubuntu_jaoz0k/var/games                3.6T  128K  3.6T   1% /var/games
rpool/ROOT/ubuntu_jaoz0k/var/mail                 3.6T  128K  3.6T   1% /var/mail
rpool/ROOT/ubuntu_jaoz0k/srv                      3.6T  128K  3.6T   1% /srv
rpool/ROOT/ubuntu_jaoz0k/var/spool                3.6T  128K  3.6T   1% /var/spool
rpool/ROOT/ubuntu_jaoz0k/var/snap                 3.6T  1.5M  3.6T   1% /var/snap
rpool/ROOT/ubuntu_jaoz0k/var/www                  3.6T  128K  3.6T   1% /var/www
rpool/ROOT/ubuntu_jaoz0k/var/lib                  3.6T  2.5G  3.6T   1% /var/lib
rpool/USERDATA/idea_h1o6tw                        3.6T  3.2M  3.6T   1% /home/idea
rpool/USERDATA/root_h1o6tw                        3.6T  256K  3.6T   1% /root
rpool/ROOT/ubuntu_jaoz0k/var/log                  3.6T  2.7M  3.6T   1% /var/log
rpool/ROOT/ubuntu_jaoz0k/usr/local                3.6T  128K  3.6T   1% /usr/local
rpool/ROOT/ubuntu_jaoz0k/var/lib/AccountsService  3.6T  128K  3.6T   1% /var/lib/AccountsService
rpool/ROOT/ubuntu_jaoz0k/var/lib/apt              3.6T  103M  3.6T   1% /var/lib/apt
rpool/ROOT/ubuntu_jaoz0k/var/lib/dpkg             3.6T   33M  3.6T   1% /var/lib/dpkg
rpool/ROOT/ubuntu_jaoz0k/var/lib/NetworkManager   3.6T  256K  3.6T   1% /var/lib/NetworkManager
bpool/BOOT/ubuntu_jaoz0k                          1.8G  294M  1.5G  17% /boot
/dev/sdb1                                         511M   15M  497M   3% /boot/efi
tmpfs                                             6.3G  172K  6.3G   1% /run/user/1000
/dev/sdc2                                         1.8T   36K  1.7T   1% /media/idea/e0f5c1d2-8ba8-46b4-b30b-2b99df927a0d
/dev/sdc1                                         488M   24K  452M   1% /media/idea/d973fdc8-8f7f-4a16-b1fb-dff5d4976c9a
/dev/sda1                                         293G   28K  278G   1% /media/idea/Backup
```

安装编辑器

```
sudo apt install vim
```

## 第一：安装JDK

```
lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.3 LTS
Release:        22.04
Codename:       jammy
```

```
java
Command 'java' not found, but can be installed with:
sudo apt install default-jre              # version 2:1.11-72build2, or
sudo apt install openjdk-11-jre-headless  # version 11.0.20.1+1-0ubuntu1~22.04
sudo apt install openjdk-17-jre-headless  # version 17.0.8.1+1~us1-0ubuntu1~22.04
sudo apt install openjdk-18-jre-headless  # version 18.0.2+9-2~22.04
sudo apt install openjdk-19-jre-headless  # version 19.0.2+7-0ubuntu3~22.04
sudo apt install openjdk-8-jre-headless   # version 8u382-ga-1~22.04.1
```

```
sudo apt install openjdk-11-jre-headless
```

```
java --version
openjdk 11.0.20.1 2023-08-24
OpenJDK Runtime Environment (build 11.0.20.1+1-post-Ubuntu-0ubuntu122.04)
OpenJDK 64-Bit Server VM (build 11.0.20.1+1-post-Ubuntu-0ubuntu122.04, mixed mode, sharing)
```

安装成功

安装javac

```
javac
Command 'javac' not found, but can be installed with:
sudo apt install default-jdk              # version 2:1.11-72build2, or
sudo apt install openjdk-11-jdk-headless  # version 11.0.20.1+1-0ubuntu1~22.04
sudo apt install openjdk-17-jdk-headless  # version 17.0.8.1+1~us1-0ubuntu1~22.04
sudo apt install openjdk-18-jdk-headless  # version 18.0.2+9-2~22.04
sudo apt install openjdk-19-jdk-headless  # version 19.0.2+7-0ubuntu3~22.04
sudo apt install openjdk-8-jdk-headless   # version 8u382-ga-1~22.04.1
sudo apt install ecj                      # version 3.16.0-1
```

## 第二：安装nvidia

```
nvidia-smi
Command 'nvidia-smi' not found, but can be installed with:
sudo apt install nvidia-utils-390         # version 390.157-0ubuntu0.22.04.2, or
sudo apt install nvidia-utils-418-server  # version 418.226.00-0ubuntu5~0.22.04.1
sudo apt install nvidia-utils-450-server  # version 450.248.02-0ubuntu0.22.04.1
sudo apt install nvidia-utils-470         # version 470.199.02-0ubuntu0.22.04.1
sudo apt install nvidia-utils-470-server  # version 470.199.02-0ubuntu0.22.04.1
sudo apt install nvidia-utils-525         # version 525.125.06-0ubuntu0.22.04.1
sudo apt install nvidia-utils-525-server  # version 525.125.06-0ubuntu0.22.04.1
sudo apt install nvidia-utils-535         # version 535.113.01-0ubuntu0.22.04.3
sudo apt install nvidia-utils-535-server  # version 535.104.12-0ubuntu0.22.04.2
sudo apt install nvidia-utils-510         # version 510.60.02-0ubuntu1
sudo apt install nvidia-utils-510-server  # version 510.47.03-0ubuntu3
```

查看基本信息

```
lspci | grep -i nvidia
0000:b3:00.0 VGA compatible controller: NVIDIA Corporation GA102 [GeForce RTX 3090] (rev a1)
0000:b3:00.1 Audio device: NVIDIA Corporation GA102 High Definition Audio Controller (rev a1)
```

```
uname -m && cat /etc/*release
x86_64
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=22.04
DISTRIB_CODENAME=jammy
DISTRIB_DESCRIPTION="Ubuntu 22.04.3 LTS"
PRETTY_NAME="Ubuntu 22.04.3 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
```

### 1 安装g++，gcc

```
sudo apt install build-essential
```

```
gcc --version
gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

```
sudo apt-get install manpages-dev
```

安装完成

```
 sudo apt-get install linux-headers-$(uname -r)
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
linux-headers-6.2.0-35-generic is already the newest version (6.2.0-35.35~22.04.1).
linux-headers-6.2.0-35-generic set to manually installed.
0 upgraded, 0 newly installed, 0 to remove and 2 not upgraded.
```

### 2、网络安装cuda

```
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.1-1_all.deb
```

```
sudo dpkg -i cuda-keyring_1.1-1_all.deb
```

**更新Apt软件源缓存：**

```
sudo apt-get update
```

```
sudo apt-get install cuda-toolkit
```

```
sudo apt-get install nvidia-gds
```

### 3、安装驱动drivers

```
ubuntu-drivers devices
```

```
ubuntu-drivers devices
== /sys/devices/pci0000:b2/0000:b2:00.0/0000:b3:00.0 ==
modalias : pci:v000010DEd00002204sv00001028sd00003880bc03sc00i00
vendor   : NVIDIA Corporation
model    : GA102 [GeForce RTX 3090]
manual_install: True
driver   : nvidia-driver-530 - third-party non-free
driver   : nvidia-driver-470 - third-party non-free
driver   : nvidia-driver-535-server - distro non-free
driver   : nvidia-driver-525 - third-party non-free
driver   : nvidia-driver-535 - third-party non-free
driver   : nvidia-driver-510 - third-party non-free
driver   : nvidia-driver-535-open - distro non-free
driver   : nvidia-driver-525-server - distro non-free
driver   : nvidia-driver-545 - third-party non-free recommended
driver   : nvidia-driver-520 - third-party non-free
driver   : nvidia-driver-515 - third-party non-free
driver   : nvidia-driver-470-server - distro non-free
driver   : nvidia-driver-525-open - distro non-free
driver   : nvidia-driver-535-server-open - distro non-free
driver   : xserver-xorg-video-nouveau - distro free builtin
```

```
sudo apt install nvidia-driver-545
```

```
nvidia-smi
```

Tue Oct 24 23:37:28 2023                                                                                                                                            

+---------------------------------------------------------------------------------------+                                                                           

| NVIDIA-SMI 545.23.06              Driver Version: 545.23.06    CUDA Version: 12.3     |                                                                           

|-----------------------------------------+----------------------+----------------------+                                                                           

| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |                                                                           

| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |                                                                           

|                                         |                      |               MIG M. |                                                                           

|=========================================+======================+======================|                                                                           

|   0  NVIDIA GeForce RTX 3090        Off | 00000000:B3:00.0 Off |                  N/A |                                                                           

| 30%   46C    P0             119W / 350W |      4MiB / 24576MiB |     12%      Default |                                                                           

|                                         |                      |                  N/A |                                                                           

+-----------------------------------------+----------------------+----------------------+                                                                           

​                                                                                                                                                                    

+---------------------------------------------------------------------------------------+                                                                           

| Processes:                                                                            |                                                                           

|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |                                                                           

|        ID   ID                                                             Usage      |                                                                           

|=======================================================================================|                                                                           

|  No running processes found                                                           |                                                                           

+---------------------------------------------------------------------------------------+    

## 第三、安装conda

```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

1. 将miniconda加入PATH路径

打开~/.bashrc文件，在文件末尾加入如下内容：

> export PATH="/home/idea/miniconda3/bin:$PATH"

1. 关闭当前的命令行窗口，重新打开后即可使用miniconda

```
source .bashrc
```

## 第四、安装pytorch

安装虚拟环境

```
conda create -n sqlib  python=3.8
```

安装pytorch

```
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```


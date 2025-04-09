# SFTP Virtual Machines and Log Report System

This repository provides a self-contained virtual environment with multiple Alpine Linux-based SFTP servers. Each machine automatically sends files to other nodes via SFTP, logs the interactions, performs basic security audits, and allows generating reports via a Python web application.

## Repository Structure

- **`Vagrant-SFTPs/`**  
  Contains Vagrant and provisioning scripts for spinning up any number of Alpine Linux 3.19 VMs with:
  - SFTP servers
  - SSH key-based access
  - Scheduled Bash cronjob (runs every 5 minutes)
  - `rkhunter` security auditing

- **`python-report/`**  
  A Dockerized Python app stack including:
  - **Log Collector**: Connects to each SFTP host, parses logs and aggregates data
  - **Web App**: Displays a summary for management with graphs and tables
  - **Data Volume**: Logs and reports are stored in a local Docker volume

---

## Usage

### 1. Prerequisites

- [Vagrant](https://www.vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/)
- [Docker](https://www.docker.com/)

> All virtual machines are based on **Alpine Linux 3.19**  
> SSH keys are generated and distributed automatically

---

### 2. Configure the Vagrant Project (Optional)

Inside `Vagrant-SFTPs/Vagrantfile`, you can modify:

- `MACHINE_COUNT` — number of VMs to create (default: 3)
- `BASE_IP` — the base IP for the VM subnet (e.g. `192.168.0.100`)

VMs will then be assigned incrementally from the base (e.g. `.111`, `.112`, etc.)

---

### 3. Deploy the Virtual Machines
```
cd Vagrant-SFTPs
vagrant up
```
### 4. Run the Python Reporting App
```
cd python-report
docker-compose up --build -d
```
The web app becomes accessible at:
http://<host-ip>:5000

All collected data is stored in a volume in the local project directory

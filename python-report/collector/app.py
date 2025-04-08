#!/usr/bin/env python3
import os
import paramiko
import time
from datetime import datetime

# Configuration
HOSTS = ['192.168.0.111', '192.168.0.112', '192.168.0.113']
CREDS = {'username': 'vagrant', 'password': 'vagrant'}
REMOTE_PATH = '/home/sftpuser/upload'
LOCAL_LOG = '/home/python-log-collector-logs/log'
CHECK_INTERVAL = 300  # seconds

def ensure_directory_exists(path):
    """Create directory structure if it doesn't exist"""
    os.makedirs(os.path.dirname(path), exist_ok=True)

def get_existing_logs():
    """Read already processed filenames"""
    if not os.path.exists(LOCAL_LOG):
        return set()

    with open(LOCAL_LOG, 'r') as f:
        return {line.strip() for line in f if line.strip()}

def ssh_scan_host(host, existing_files):
    """Connect to host and scan for new files"""
    try:
        # Connection check
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, **CREDS, timeout=5)

        # SFTP check
        sftp = client.open_sftp()
        try:
            files = sftp.listdir(REMOTE_PATH)
        except FileNotFoundError:
            print(f"[{host}] Upload directory not found")
            return []

        new_files = []
        for f in files:
            if f not in existing_files and not f.startswith('.'):
                new_files.append(f)

        return new_files

    except Exception as e:
        print(f"[{host}] Connection failed: {str(e)}")
        return []
    finally:
        try: client.close()
        except: pass

def update_log_file(new_files):
    """Append new files to log"""
    with open(LOCAL_LOG, 'a') as f:
        for file in new_files:
            f.write(f"{file}\n")

def main():
    ensure_directory_exists(LOCAL_LOG)

    while True:
        print(f"\n=== Scan started at {datetime.now().isoformat()} ===")
        existing_files = get_existing_logs()
        all_new_files = []

        for host in HOSTS:
            new_files = ssh_scan_host(host, existing_files)
            if new_files:
                print(f"[{host}] Found new files: {', '.join(new_files)}")
                all_new_files.extend(new_files)
            else:
                print(f"[{host}] No new files found")

        if all_new_files:
            update_log_file(all_new_files)
            print(f"Logged {len(all_new_files)} new files to {LOCAL_LOG}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")

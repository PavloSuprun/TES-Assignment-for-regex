#!/bin/sh

MACHINES_COUNT=3
BASE_IP="192.168.0.110"
CURRENT_IP=$(ip -o -4 addr show eth1 | awk '{print $4}' | cut -d'/' -f1)
CURRENT_HOST=$(hostname)

i=1
while [ $i -le $MACHINES_COUNT ]; do
    last_octet=$(echo "$BASE_IP" | cut -d'.' -f4)
    first_three=$(echo "$BASE_IP" | cut -d'.' -f1-3)
    host_ip="$first_three.$((last_octet + i))"

    if [ "$host_ip" = "$CURRENT_IP" ]; then
        echo "[INFO] Skipping local host $host_ip"
        i=$((i + 1))
        continue
    fi

    timestamp=$(date '+%Y-%m-%d_%H-%M-%S')
    filename="file_created_by_${CURRENT_IP}_$timestamp.txt"
    content="File was created by $CURRENT_HOST at $timestamp"

    echo "[INFO] Creating file $filename on $host_ip"
    tempfile="/home/sftpuser/upload/$filename"
    echo "$content" > "$tempfile"

    sudo -u sftpuser sftp -o StrictHostKeyChecking=no -b - "sftpuser@$host_ip:/home/sftpuser/upload/" <<EOF
put "$tempfile"
EOF

    rm "$tempfile"
    i=$((i + 1))
done

#!/bin/bash

. /tmp/shared.sh

# Temporary directory for keys
TMP_DIR="/tmp/ssh_keys_exchange"
mkdir -p "$TMP_DIR"

# Collect all public keys
for ((i=1; i<=$MACHINES_COUNT; i++)); do
    host_ip=$(echo "$BASE_IP" | awk -F. -v i=$i '{printf "%s.%s.%s.%d\n", $1, $2, $3, $4+i}')
    echo "[INFO] Fetching key from $host_ip..."
    
    sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no "$USER@$host_ip" "cat /home/$USER/.ssh/id_rsa.pub" > "$TMP_DIR/host_$i.pub"
done

cat "$TMP_DIR"/*.pub > "$TMP_DIR/authorized_keys"

# Distribute combined keys to all hosts
for ((i=1; i<=$MACHINES_COUNT; i++)); do
    host_ip=$(echo "$BASE_IP" | awk -F. -v i=$i '{printf "%s.%s.%s.%d\n", $1, $2, $3, $4+i}')
    echo "[INFO] Distributing authorized_keys to $host_ip..."
    
    sshpass -p "$PASS" scp -o StrictHostKeyChecking=no "$TMP_DIR/authorized_keys" "$USER@$host_ip:/home/$USER/.ssh/authorized_keys"
    sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no "$USER@$host_ip" "chmod 600 /home/$USER/.ssh/authorized_keys && chown $USER:$GROUP /home/$USER/.ssh/authorized_keys"
done

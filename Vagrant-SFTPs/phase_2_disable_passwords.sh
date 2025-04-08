#!/bin/bash

. /tmp/shared.sh

for ((i=1; i<=$MACHINES_COUNT; i++)); do
  last_octet="${BASE_IP##*.}"
  host_ip="${BASE_IP%.*}.$((last_octet + i))"

  echo "[INFO] Disabling password auth on $host_ip"

  sshpass -p "vagrant" ssh -o StrictHostKeyChecking=no "vagrant@$host_ip" << EOF
    echo -e "\nMatch User sftpuser\n    PasswordAuthentication no" | sudo tee -a /etc/ssh/sshd_config > /dev/null
    sudo service sshd restart
EOF
done

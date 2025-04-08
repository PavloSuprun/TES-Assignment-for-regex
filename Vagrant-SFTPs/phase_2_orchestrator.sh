#!/bin/bash

sed -i 's/\r$//' /tmp/shared.sh
. /tmp/shared.sh

echo "[ORCHESTRATOR] Starting key exchange phase..."
chmod +x /tmp/phase_2_exchange_keys.sh
/tmp/phase_2_exchange_keys.sh

echo "[ORCHESTRATOR] Key exchange complete. Disabling password access..."
chmod +x /tmp/phase_2_disable_passwords.sh
/tmp/phase_2_disable_passwords.sh

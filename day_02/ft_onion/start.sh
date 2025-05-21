#!/bin/bash

echo "Starting SSH..."
/usr/sbin/sshd

echo "Starting Tor..."
tor &

echo "Waiting for Tor to generate onion hostname..."
while [ ! -f /var/lib/tor/hidden_service/hostname ]; do
    sleep 1
done

ONION_ADDRESS=$(cat /var/lib/tor/hidden_service/hostname)
echo "Onion service available at: http://${ONION_ADDRESS}"

echo "Starting Nginx..."
nginx -g "daemon off;"

#!/usr/bin/env bash
wpa_supplicant_location=/etc/wpa_supplicant/wpa_supplicant.conf
network="telenet-E291DB2-guest"
wireless_if="wlan0"

if ip link show ${wireless_if}; then
    if ! grep -q "$network" ${wpa_supplicant_location}
    echo "network={
    ssid=$network
    key_mgmt=NONE
    }" >> ${wpa_supplicant_location}
    counter=0
    while ! ip -br -4 address show dev ${wireless_if} scope global | awk '{split($3,a,"/"); print a[1]}' | grep -q "[0-2][0-9][0-9]\.[0-2][0-9][0-9]\.[0-2][0-9][0-9]\.[0-2][0-9][0-9]"; do
        counter=$((counter+1))
        sleep 5
        if [[ $counter -gt 10 ]]; then
            exit 1
        fi
    done
    #TODO perform POST call to authenticate to captive portal
fi

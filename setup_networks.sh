#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

apt-get update
apt-get install -y jq

./wifi_connect.sh

interfaces=$(find /sys/class/net -type l -not -lname '*virtual*' -printf '%f\n' | grep -v "eth0")

while read -r link; do
    bridgename="dckr-$link"
    echo "Removing old network $bridgename"
    docker network rm $bridgename
    echo "Adding new network $bridgename"
    bridge=$(docker network create --attachable --opt "com.docker.network.bridge.name=$bridgename" --opt "com.docker.network.bridge.enable_ip_masquerade=false" $bridgename)
    echo "Fetching interface $link's IPv4 address"
    if_ip=$(ip -br -4 address show dev $link scope global | awk '{split($3,a,"/"); print a[1]}')
    echo "Fetching $bridgename's ip"
    bridge_ip=$(docker network inspect $bridge | jq '.[0].IPAM.Config[0].Subnet')
    echo "Modifying iptables rules for $bridgename"
    iptables -t nat -A POSTROUTING -s $bridge_ip ! -o $bridgename -j SNAT --to-source $if_ip
    echo "Created bridge $bridgename for interface $link with bridge ip $bridge_ip and interface ip $if_ip"
done <<< "$interfaces"



#!/usr/bin/env bash

interfaces=$(find /sys/class/net -type l -not -lname '*virtual*' -printf '%f\n' | grep -v "eth0")

while read -r link; do
    bridge=$(docker network create --attachable --opt "com.docker.network.bridge.name=bridge-docker-$link" --opt "com.docker.network.bridge.enable_ip_masquerade=false" bridge-docker-$link)
    if_ip=ip -br -4 address show dev $link scope global | awk '{split($3,a,"/"); print a[1]}'
    bridge_ip=$(docker network inspect $bridge | jq '.[0].IPAM.Config[0].Subnet')
    iptables -t nat -A POSTROUTING -s $bridge_ip ! -o bridge-docker-$link -j SNAT --to-source $if_ip
    echo "Created bridge bridge-docker-$link for interface $link with bridge ip $bridge_ip and interface ip $if_ip"
done <<< "$interfaces"



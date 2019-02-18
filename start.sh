#!/usr/bin/env bash
while ! wget -q --spider google.com; do
    sleep 10
done
python3 download.py &
python3 browse.py
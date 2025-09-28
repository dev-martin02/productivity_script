#!/bin/bash

# List of websites to bloc
SITES=(
    "youtube.com"
    "www.youtube.com"
)

# Get root privileges
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root."
    exit 1
fi

if [ "$1" == "block" ]; then
# Loop through blocked sites and add them to hosts file
    for site in "${SITES[@]}"; do
        if grep -q "$site" /etc/hosts; then
            echo "$site is already blocked."
        else
            echo "Blocking $site..."
            echo "127.0.0.1 $site" >> /etc/hosts
        fi
    done
    echo "All sites have been blocked."
elif [ "$1"  == "unblock" ]; then
    # Loop through unblocked sites and remove them from hosts file
    for site in "${SITES[@]}"; do
        if grep -q $site /etc/hosts; then
            echo "Unblocking $site..."
            sed -i "/$site/d" /etc/hosts
        else
            echo "$site is already unblocked."
        fi
    done

    echo "All sites have been unblocked."
    fi


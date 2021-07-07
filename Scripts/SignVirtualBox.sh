#!/bin/bash

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root"
  exit 1
fi

for modfile in "$(dirname "$(modinfo -n vboxdrv)")"/*.ko
do
  echo "Signing $modfile"
  /usr/src/kernels/"$(uname -r)"/scripts/sign-file sha256 /root/signed-modules/MOK.priv /root/signed-modules/MOK.der "$modfile"
done
modprobe vboxdrv
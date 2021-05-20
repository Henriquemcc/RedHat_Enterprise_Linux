#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

dnf --assumeyes update --refresh
dnf --assumeyes install mokutil
mkdir /root/signed-modules
cd /root/signed-modules || exit 1
openssl req -new -x509 -newkey rsa:2048 -keyout MOK.priv -outform DER -out MOK.der -nodes -days 36500 -subj "/CN=VirtualBox/"
chmod 600 MOK.priv
mokutil --import MOK.der
cd /usr/bin || exit 1
echo "#!/bin/bash" >> sign_virtualBox.sh
echo "for modfile in \$(dirname \"\$(modinfo -n vboxdrv)\")/*.ko; do" >> sign_virtualBox.sh
echo "echo \"Signing \$modfile\"" >> sign_virtualBox.sh
echo "/usr/src/kernels/\"\$(uname -r)\"/scripts/sign-file sha256 /root/signed-modules/MOK.priv /root/signed-modules/MOK.der \"\$modfile\"" >> sign_virtualBox.sh
echo "done" >> sign_virtualBox.sh
chmod 700 sign_virtualBox.sh
./sign_virtualBox.sh

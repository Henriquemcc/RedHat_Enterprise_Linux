#!/bin/bash

function instalar_pre-requisitos() {
  sudo dnf -y groupinstall 'Development Tools'
  sudo dnf --assumeyes install gcc.x86_64 libX11-devel.x86_64 libX11-devel.i686 freetype-devel.x86_64 freetype-devel.i686 zlib-devel.x86_64 zlib-devel.i686 libxcb-devel.x86_64 libxcb-devel.i686 libxslt-devel.x86_64 libxslt-devel.i686 libgcrypt-devel.x86_64 libgcrypt-devel.i686 libxml2-devel.x86_64 libxml2-devel.i686 gnutls-devel.x86_64 gnutls-devel.i686 libpng-devel.x86_64 libpng-devel.i686 libjpeg-turbo-devel.x86_64 libjpeg-turbo-devel.i686 libtiff-devel.x86_64 libtiff-devel.i686 dbus-devel.x86_64 dbus-devel.i686 fontconfig-devel.x86_64 fontconfig-devel.i686 glibc-devel.i686 libgcc.i686 libstdc++-devel.i686 ncurses-devel.i686 cabextract
}

function limpar_pasta_tmp() {
  gio trash "/tmp/wine-wine-6.13"
}

function baixar_codigo_fonte_wine() {
  wget --no-clobber "https://github.com/wine-mirror/wine/archive/refs/tags/wine-6.13.tar.gz" -O "/tmp/wine-6.13.tar.gz"
  tar -xvzf "/tmp/wine-6.13.tar.gz" -C "/tmp"
}

function compilar_e_instalar_wine_x86_64() {
  limpar_pasta_tmp
  baixar_codigo_fonte_wine
  cd "/tmp/wine-wine-6.13/" || exit 1
  ./configure --enable-win64
  make
  sudo make install
}

function compilar_e_instalar_wine_x86_32() {
  limpar_pasta_tmp
  baixar_codigo_fonte_wine
  cd "/tmp/wine-wine-6.13/" || exit 1
  ./configure
  make
  sudo make install
}

function instalar_winetricks() {
  sudo wget "https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks" -O "/bin/winetricks"
}

function instalar_recursos_adicionais() {
  winetricks corefonts
}

function main() {
  compilar_e_instalar_wine_x86_32
  instalar_winetricks
  instalar_recursos_adicionais
}

main

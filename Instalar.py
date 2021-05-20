import os
import sys

import requests

from adapter import Wifi
from adapter.Dnf import Dnf
from adapter.Flatpak import Flatpak
from adapter.Pip import Pip
from adapter.Shell import Shell, AcaoQuandoOcorrerErro
from adapter.Snap import Snap
from adapter.SubscriptionManager import SubscriptionManager
from adapter.VisualStudioCode import VisualStudioCode
from controller.ControladorDeCredenciais import ControladorDeCredenciais

__controlador_credenciais = ControladorDeCredenciais("Credenciais.bin")

subscription_manager = SubscriptionManager()
gerenciador_dnf = Dnf()
gerenciador_snap = Snap()
gerenciador_pip = Pip()
gerenciador_flatpak = Flatpak()
gerenciador_visual_studio_code = VisualStudioCode()


def conectar_na_rede_wifi():
    Wifi.conectar_rede_wifi(
        __controlador_credenciais.credencial_rede_wifi.usuario,
        __controlador_credenciais.credencial_rede_wifi.senha
    )


def registrar_red_hat():
    subscription_manager.register(
        __controlador_credenciais.credencial_conta_red_hat.usuario,
        __controlador_credenciais.credencial_conta_red_hat.senha)


def instalar_pacotes_dnf():
    subscription_manager.habilitar_codeready_builder()
    subscription_manager.habilitar_baseos_rpms()
    subscription_manager.habilitar_appstream_rpms()
    gerenciador_dnf.habilitar_fedora_epel()
    gerenciador_dnf.habilitar_rpm_fusion()
    gerenciador_dnf.config_manager_add_repo(
        [
            "https://developer.download.nvidia.com/compute/cuda/repos/rhel8/x86_64/cuda-rhel8.repo",
            "https://cli.github.com/packages/rpm/gh-cli.repo"
        ]
    )
    gerenciador_dnf.upgrade()

    # Driver da Nvidia
    gerenciador_dnf.module_install("nvidia-driver")

    gerenciador_dnf.install(
        [

            # Programas externos
            "https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm",
            "https://github.com/peazip/PeaZip/releases/download/7.7.1/peazip-7.7.1.LINUX.GTK2-1.x86_64.rpm",
            requests.get(
                "https://teams.microsoft.com/downloads/desktopurl?env=production&plat=linux&arch=x64&download=true&linuxArchiveType=rpm").url,
            "https://download.teamviewer.com/download/linux/teamviewer.x86_64.rpm",

            # Libreoffice
            "libreoffice-writer", "libreoffice-calc", "libreoffice-impress", "libreoffice-math", "libreoffice-draw",
            "libreoffice-langpack-pt-BR", "libreoffice-langpack-en", "unoconv",

            # Impressora HP
            "hplip",

            # KVM
            "qemu-kvm", "libvirt",

            # Sistemas de arquivos não nativos do linux
            "ntfs-3g", "exfat-utils", "fuse", "fuse-exfat",

            # Ferramentas de desenvolvimento
            "java-latest-openjdk-devel", "java-1.8.0-openjdk-devel", "golang", "gcc", "dotnet-sdk-5.0",
            "aspnetcore-runtime-5.0", "dotnet-runtime-5.0", "git", "git-lfs", "gh",

            # Outros programas
            "stacer", "qt5-qtcharts", "vlc", "qt5-qtsvg", "youtube-dl.noarch", "snapd", "flatpak", "transmission",
            "ffmpeg", "steam.i686", "VirtualBox", "mokutil", "fdupes", "dnf-automatic", "gnome-tweaks", "dconf-editor"
        ]
    )


def instalar_pacotes_snap():
    gerenciador_snap.instalar_snapd()
    gerenciador_snap.install([
        "keepassxc --devmode",
        "spotify",
        "code --classic",
        "intellij-idea-community --classic",
        "pycharm-community --classic",
        "flutter --classic",
        "kotlin --classic",
        "skype --classic",
        "clion --classic",
        "rider --classic"
    ])


def instalar_pacotes_pip():
    gerenciador_pip.install("protonvpn-cli")


def instalar_pacotes_flatpak():
    gerenciador_flatpak.instalar_flatpak()
    gerenciador_flatpak.habilitar_flathub()
    gerenciador_flatpak.install(
        [
            "https://dl.flathub.org/repo/appstream/com.google.AndroidStudio.flatpakref",
            "https://dl.flathub.org/repo/appstream/com.discordapp.Discord.flatpakref"
        ]
    )


def instalar_extensoes_visual_studio_code():
    gerenciador_visual_studio_code.install_extension(
        [
            # Tradução do VS Code em Português
            "ms-ceintl.vscode-language-pack-pt-br",

            # Linguagem C/C++
            "ms-vscode.cpptools",
            "ms-vscode.cmake-tools",
            "austin.code-gnu-global",

            # Linguagem C#
            "ms-dotnettools.csharp",

            # Linguagem Java
            "vscjava.vscode-java-debug",
            "vscjava.vscode-maven",
            "vscjava.vscode-java-dependency",
            "vscjava.vscode-java-pack",
            "vscjava.vscode-java-test",
            "redhat.java",

            # Linguagem Rust
            "matklad.rust-analyzer",
            "vadimcn.vscode-lldb",
            "rust-lang.rust",

            # Linguagem Go
            "golang.Go",

            # HTML, CSS e Javascript
            "ecmel.vscode-html-css",
            "firefox-devtools.vscode-firefox-debug",
            "msjsdiag.debugger-for-chrome",
            "dbaeumer.vscode-eslint",

            # Tema do VS Code
            "GitHub.github-vscode-theme",

            # Markdown
            "DavidAnson.vscode-markdownlint",

            # Powershell
            " ms-vscode.PowerShell",

            # Indentação de código
            "NathanRidley.autotrim",
            "esbenp.prettier-vscode",

            # AI-assisted IntelliSense
            "VisualStudioExptTeam.vscodeintellicode"
        ]
    )

    shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
    shell.executar("echo 'fs.inotify.max_user_watches=524288' | sudo tee --append /etc/sysctl.conf")
    shell.executar("sudo sysctl -p")
    shell.executar("git config --global core.editor \"code --wait\"")


def instalar_rust_lang():
    shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
    shell.executar("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")


def configurar_java():
    shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)

    # Criando comando java8 e javac8
    shell.executar("sudo ln -s /usr/lib/jvm/java-1.8.0/bin/java /bin/java8")
    shell.executar("sudo ln -s /usr/lib/jvm/java-1.8.0/bin/javac /bin/javac8")

    with open("java.desktop", "w") as arquivo_atalho:
        arquivo_atalho.writelines(
            ["[Desktop Entry]\n", "Name=Java Runtime Environment\n", "Comment=Java Runtime Environment\n",
             "GenericName=Java\n", "Keywords=java\n", "Exec=java -jar %f\n", "Terminal=false\n",
             "X-MultipleArgs=false\n", "Type=Application\n", "MimeType=application/x-java-archive\n",
             "StartupNotify=true\n", "Icon=java-1.8.0-openjdk\n"])
        arquivo_atalho.close()

    shell.executar("sudo chmod 777 ./java.desktop")
    shell.executar("sudo cp --force ./java.desktop /usr/share/applications/java.desktop")
    shell.executar("sudo chmod 777 /usr/share/applications/java.desktop")
    shell.executar("gio trash ./java.desktop")

    with open("java8.desktop", "w") as arquivo_atalho:
        arquivo_atalho.writelines(
            ["[Desktop Entry]\n", "Name=Java Runtime Environment 8\n", "Comment=Java Runtime Environment 8\n",
             "GenericName=Java8\n", "Keywords=java8\n", "Exec=java8 -jar %f\n", "Terminal=false\n",
             "X-MultipleArgs=false\n", "Type=Application\n", "MimeType=application/x-java-archive\n",
             "StartupNotify=true\n", "Icon=java-1.8.0-openjdk\n"])
        arquivo_atalho.close()

    shell.executar("sudo chmod 777 ./java8.desktop")
    shell.executar("sudo cp --force ./java8.desktop /usr/share/applications/java8.desktop")
    shell.executar("sudo chmod 777 /usr/share/applications/java8.desktop")
    shell.executar("gio trash ./java8.desktop")


def configurar_adb():
    Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10) \
        .executar("sudo ln --symbolic ~/Android/Sdk/platform-tools/adb /bin/adb")


def configurar_virtualbox():
    with open("sign-virtual-box", "w") as arquivo_assinar_modulos_virtualbox:
        arquivo_assinar_modulos_virtualbox.writelines(
            ["#!/bin/bash\n", "for modfile in $(dirname $(modinfo -n vboxdrv))/*.ko; do\n",
             "  echo \"Signing $modfile\"\n", "  /usr/src/kernels/$(uname -r)/scripts/sign-file sha256 \\\n",
             "                                /root/signed-modules/MOK.priv \\\n",
             "                                /root/signed-modules/MOK.der \"$modfile\"\n", "done\n"])
        arquivo_assinar_modulos_virtualbox.close()

    gerenciador_dnf.install("mokutil")

    shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
    shell.executar(
        [
            "sudo mkdir /root/signed-modules",
            "sudo openssl req -new -x509 -newkey rsa:2048 -keyout /root/signed-modules/MOK.priv -outform DER -out /root/signed-modules/MOK.der -nodes -days 36500 -subj '/CN=VirtualBox/'",
            "sudo chmod 600 /root/signed-modules/MOK.priv", "sudo mokutil --import /root/signed-modules/MOK.der"
                                                            "sudo chmod 700 /root/signed-modules/sign-virtual-box",
            "sudo /root/signed-modules/sign-virtual-box",
            "sudo modprobe vboxdrv",
            "sudo cp ./sign-virtual-box /root/signed-modules/sign-virtual-box",
            "sudo chmod 700 /root/signed-modules/sign-virtual-box",
            "sudo /root/signed-modules/sign-virtual-box",
            "sudo modprobe vboxdrv",
            "gio trash ./sign-virtual-box"
        ]
    )


def main():
    euid = os.geteuid()
    if euid == 0:
        conectar_na_rede_wifi()
        registrar_red_hat()
        instalar_pacotes_dnf()
        instalar_pacotes_snap()
        instalar_pacotes_pip()
        instalar_pacotes_flatpak()
        configurar_java()
        configurar_adb()
        configurar_virtualbox()
    else:
        print("Este script não está rodando como root")
        shell = Shell(acao_quando_ocorrer_erro=AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR)
        localizacao_executavel_python = sys.executable
        localizacao_arquivo_python = os.path.abspath(__file__)
        shell.executar("sudo '{}' '{}'".format(localizacao_executavel_python, localizacao_arquivo_python))
        instalar_extensoes_visual_studio_code()
        instalar_rust_lang()


if __name__ == '__main__':
    main()

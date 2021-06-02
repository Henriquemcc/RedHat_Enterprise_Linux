import io
import os
import shutil
import sys

import requests

from adapter import Wifi
from adapter.Dnf import Dnf
from adapter.Flatpak import Flatpak
from adapter.Shell import Shell, AcaoQuandoOcorrerErro
from adapter.Snap import Snap
from adapter.SubscriptionManager import SubscriptionManager
from controller.ControladorDeCredenciais import ControladorDeCredenciais

__controlador_credenciais = ControladorDeCredenciais()
subscription_manager = SubscriptionManager()
gerenciador_dnf = Dnf()
gerenciador_snap = Snap()
gerenciador_flatpak = Flatpak()


def conectar_na_rede_wifi():
    """
    Conecta á rede wifi.
    """
    Wifi.conectar_rede_wifi(
        __controlador_credenciais.credencial_rede_wifi.usuario,
        __controlador_credenciais.credencial_rede_wifi.senha
    )


def registrar_red_hat():
    """
    Registra instalação á conta da Red Hat.
    """
    subscription_manager.register(
        __controlador_credenciais.credencial_conta_red_hat.usuario,
        __controlador_credenciais.credencial_conta_red_hat.senha)


def instalar_pacotes_dnf():
    """
    Adiciona repositórios, atualiza e instala os pacotes DNF.
    """
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
                "https://teams.microsoft.com/downloads/desktopurl?env=production&plat=linux&arch=x64&download=true"
                "&linuxArchiveType=rpm").url,
            "https://download.teamviewer.com/download/linux/teamviewer.x86_64.rpm",

            # Libreoffice
            "libreoffice-writer", "libreoffice-calc", "libreoffice-impress", "libreoffice-math", "libreoffice-draw",
            "libreoffice-langpack-pt-BR", "libreoffice-langpack-en", "unoconv",

            # Impressora HP
            "hplip",

            # Driver da placa de som
            "alsa-firmware", "pipewire", "pipewire-pulseaudio",

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
    """
    Instala o gerenciador de pacotes Snap e os pacotes Snap.
    """
    Snap.instalar_snapd()
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


def instalar_pacotes_flatpak():
    """
    Instala o gerenciador de pacotes Flatpak, instala o Flathub e os pacotes Flatpak
    """
    Flatpak.instalar_flatpak()
    gerenciador_flatpak.instalar_flatpak()
    gerenciador_flatpak.habilitar_flathub()
    gerenciador_flatpak.install(
        [
            "https://dl.flathub.org/repo/appstream/com.google.AndroidStudio.flatpakref",
            "https://dl.flathub.org/repo/appstream/com.discordapp.Discord.flatpakref",
            "https://dl.flathub.org/repo/appstream/org.audacityteam.Audacity.flatpakref"
        ]
    )


def configurar_java():
    """
    Configura o compilador e á máquina virtual Java.
    """
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

    shell.executar("sudo chmod 777 ./java8.desktop")
    shell.executar("sudo cp --force ./java8.desktop /usr/share/applications/java8.desktop")
    shell.executar("sudo chmod 777 /usr/share/applications/java8.desktop")
    shell.executar("gio trash ./java8.desktop")


def configurar_virtualbox():
    """
    Configura o VirtualBox.
    """
    gerenciador_dnf.install("mokutil")

    shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
    shell.executar("sudo bash ./Scripts/SignVirtualboxModules.sh")


def configurar_script_de_atualizacao():
    """
    Configura o script de atualização de pacotes do sistema.
    """
    shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
    shell.executar("sudo cp ./Scripts/Update.sh /usr/bin/update")


def configurar_grub():
    """
    Configura o Grub
    """

    caminho_absoluto_configuracao_grub = "/etc/default/grub"
    caminho_absoluto_configuracao_grub_backup = "/etc/default/grub.old"

    try:
        shutil.copy(caminho_absoluto_configuracao_grub, caminho_absoluto_configuracao_grub_backup)
    except Exception as e:
        print(e)
        return

    grub_default_saved_param = "GRUB_DEFAULT=saved"
    grub_savedefault_true_param = "GRUB_SAVEDEFAULT=true"

    with open(caminho_absoluto_configuracao_grub, "r+") as arquivo:
        linhas = arquivo.readlines()
        if not any(grub_default_saved_param in linha for linha in linhas):
            arquivo.seek(0, io.SEEK_END)
            arquivo.write("{}\n".format(grub_default_saved_param))
        if not any(grub_savedefault_true_param in linha for linha in linhas):
            arquivo.seek(0, io.SEEK_END)
            arquivo.write("{}\n".format(grub_savedefault_true_param))

    shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
    # shell.executar("sudo grub2-set-default saved")
    shell.executar("sudo grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg")


def main():
    """
    Método principal.
    """
    conectar_na_rede_wifi()
    registrar_red_hat()
    instalar_pacotes_dnf()
    instalar_pacotes_snap()
    instalar_pacotes_flatpak()
    configurar_java()
    configurar_virtualbox()
    configurar_script_de_atualizacao()
    #configurar_grub()


if __name__ == '__main__':

    # Verificando se eh root
    if os.geteuid() == 0:
        main()
    else:
        # Executando como root
        print("Este script não está rodando como root.")
        print("Realizando a elevação de privilégio...")
        __shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
        caminho_absoluto_deste_arquivo_python = os.path.abspath(__file__)
        caminho_absoluto_deste_interpretador_python = sys.executable
        __shell.executar("sudo {} {}".format(caminho_absoluto_deste_interpretador_python,
                                             caminho_absoluto_deste_arquivo_python))

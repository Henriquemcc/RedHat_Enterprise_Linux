import os
import shutil
import sys

import requests

import Tools.Backup
from adapter import Wifi
from adapter.Dnf import Dnf
from adapter.Flatpak import Flatpak
from adapter.Pip import Pip
from adapter.Shell import Shell, AcaoQuandoOcorrerErro
from adapter.Snap import Snap
from adapter.SubscriptionManager import SubscriptionManager
from controller.ControladorDeCredenciais import ControladorDeCredenciais

__controlador_credenciais = ControladorDeCredenciais()
subscription_manager = SubscriptionManager()
gerenciador_dnf = Dnf()
gerenciador_snap = Snap()
gerenciador_flatpak = Flatpak()
gerenciador_pip = Pip()
diretorio_atual = os.getcwd()


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


def configurar_pacotes_dnf():
    """
    Adiciona repositórios, atualiza e instala os pacotes DNF e remove pacotes inúteis.
    """

    # Adicionando repositórios
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

    # Atualizando pacotes
    gerenciador_dnf.upgrade()

    # Driver da Nvidia
    gerenciador_dnf.module_install("nvidia-driver")

    gerenciador_dnf.install(
        [

            # Programas externos
            #   PowerShell 7.1.3
            "https://github.com/PowerShell/PowerShell/releases/download/v7.1.3/powershell-7.1.3-1.centos.8.x86_64.rpm",

            #   Google Chrome
            "https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm",

            #   Peazip 8.0.0
            "https://github.com/peazip/PeaZip/releases/download/8.0.0/peazip-8.0.0.LINUX.GTK2-1.x86_64.rpm",

            #   Microsoft Teams
            requests.get(
                "https://teams.microsoft.com/downloads/desktopurl?env=production&plat=linux&arch=x64&download=true"
                "&linuxArchiveType=rpm").url,

            #   CloudFlare DNS CLient
            "https://pkg.cloudflareclient.com/cloudflare-release-el8.rpm",

            # R Studio
            "https://download1.rstudio.org/desktop/centos8/x86_64/rstudio-1.4.1717-x86_64.rpm",

            # Libreoffice
            "libreoffice-writer", "libreoffice-calc", "libreoffice-impress", "libreoffice-math", "libreoffice-draw",
            "libreoffice-langpack-pt-BR", "libreoffice-langpack-en", "unoconv",

            # Impressora HP
            "hplip",

            # Driver da placa de som
            "alsa-firmware", "pipewire", "pipewire-pulseaudio",

            # Suporte a arquivos 7zip
            "p7zip-plugins", "p7zip",

            # KVM
            "qemu-kvm", "libvirt",

            # Sistemas de arquivos não nativos do linux
            "ntfs-3g", "exfat-utils", "fuse", "fuse-exfat",

            # Extensões do Gnome shell
            "gnome-shell-extension-updates-dialog", "gnome-shell-extension-dash-to-dock",

            # Ferramentas de desenvolvimento
            "java-latest-openjdk-devel", "java-1.8.0-openjdk-devel", "golang", "gcc", "dotnet-sdk-5.0",
            "aspnetcore-runtime-5.0", "dotnet-runtime-5.0", "git", "git-lfs", "gh",

            # Outros programas
            "stacer", "qt5-qtcharts", "vlc", "qt5-qtsvg", "youtube-dl.noarch", "snapd", "flatpak", "transmission",
            "ffmpeg", "steam.i686", "VirtualBox", "mokutil", "fdupes", "dnf-automatic", "gnome-tweaks", "dconf-editor",
            "cloudflare-warp",

            # Reportar erro automaticamente
            "abrt-desktop", "abrt-java-connector",
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
        "skype --classic"
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
            "https://dl.flathub.org/repo/appstream/org.audacityteam.Audacity.flatpakref",
            "https://dl.flathub.org/repo/appstream/org.signal.Signal.flatpakref"
        ]
    )


def instalar_pacotes_pip():
    """
    Instala o gerenciador de pacotes Pip e os pacotes Pip.
    """
    Pip.instalar_pip()
    gerenciador_pip.install("protonvpn-cli")


def configurar_java():
    """
    Configura o compilador e á máquina virtual Java.
    """

    # Instalando o Java
    gerenciador_dnf.install(["java-latest-openjdk-devel", "java-1.8.0-openjdk-devel"])

    # Criando o comando java8
    origem = os.path.join("/usr", "lib", "jvm", "java-1.8.0", "bin", "java")
    destino = os.path.join("/bin", "java8")
    try:
        os.symlink(origem, destino)
    except Exception as e:
        print(e)

    # Criando o comando javac8
    origem = os.path.join("/usr", "lib", "jvm", "java-1.8.0", "bin", "javac")
    destino = os.path.join("/bin", "javac8")
    try:
        os.symlink(origem, destino)
    except Exception as e:
        print(e)

    # Copiando o arquivo java.desktop
    origem = os.path.join(diretorio_atual, "Shortcuts", "java.desktop")
    destino = os.path.join("/usr", "share", "applications", "java.desktop")
    try:
        shutil.copy(origem, destino)
        os.chmod(destino, 0o0777)
    except Exception as e:
        print(e)

    # Copiando o arquivo java8.desktop
    origem = os.path.join(diretorio_atual, "Shortcuts", "java8.desktop")
    destino = os.path.join("/usr", "share", "applications", "java8.desktop")
    try:
        shutil.copy(origem, destino)
        os.chmod(destino, 0o0777)
    except Exception as e:
        print(e)


def configurar_script_de_atualizacao():
    """
    Configura o script de atualização de pacotes do sistema.
    """

    origem = os.path.join(diretorio_atual, "Scripts", "Update.sh")
    destino = os.path.join("/usr", "bin", "update")
    try:
        shutil.copy(origem, destino)
        os.chmod(destino, 0o0777)
    except Exception as e:
        print(e)


def configurar_virtualbox():
    """
    Configura módulos do kernel para o VirtualBox
    """

    # Instalando prerrequisitos
    gerenciador_dnf.install(["VirtualBox", "mokutil", "akmod-VirtualBox", "kernel-devel", "VirtualBox-kmodsrc.noarch", "kmod-VirtualBox.x86_64"])

    # Criando o diretório signed-modules
    diretorio_signed_modules = os.path.join("/root", "signed-modules")
    try:
        os.makedirs(diretorio_signed_modules)
    except Exception as e:
        print(e)

    # Gerando os arquivos MOK.priv e MOK.der
    shell = Shell(AcaoQuandoOcorrerErro.IGNORAR)
    arquivo_mok_priv = os.path.join(diretorio_signed_modules, "MOK.priv")
    arquivo_mok_der = os.path.join(diretorio_signed_modules, "MOK.der")
    shell.executar(
        "sudo openssl req -new -x509 -newkey rsa:2048 -keyout {} -outform DER -out {} -nodes -days 36500 -subj \"/CN=VirtualBox/\"".format(
            arquivo_mok_priv, arquivo_mok_der))
    try:
        os.chmod(arquivo_mok_priv, 0o0600)
    except Exception as e:
        print(e)

    # Executando o mokutil para importar o arquivo MOK.der
    shell.executar("sudo mokutil --import {}".format(arquivo_mok_der))

    # Copiando o arquivo SignVirtualBox.sh
    origem = os.path.join(diretorio_atual, "Scripts", "SignVirtualBox.sh")
    destino = os.path.join("/root", "signed-modules", "SignVirtualBox.sh")
    try:
        shutil.copy(origem, destino)
        os.chmod(destino, 0o0755)
    except Exception as e:
        print(e)

    # Criando o link
    link = os.path.join("/bin", "SignVirtualBox")
    try:
        os.symlink(destino, link)
        os.chmod(link, 0o0755)
    except Exception as e:
        print(e)


def configurar_firewall():
    """
    Configura o firewall.
    """

    # Instalando o Firewall
    gerenciador_dnf.install("firewalld")

    # Bloqueando o acesso externo ao cockpit
    shell = Shell(AcaoQuandoOcorrerErro.IGNORAR)
    shell.executar("sudo firewall-cmd --remove-service=cockpit --permanent")


def configurar_open_ssh_server():
    """
    Configura o Open SSH Server
    """

    # Instalando o Open SSH Server
    gerenciador_dnf.install("openssh-server")

    # Fazendo o backup do arquivo de configuração do servidor open ssh.
    Tools.Backup.backup_file(os.path.join("/etc", "ssh"), "sshd_config")

    # Alternado o arquivo de configuração do servidor open ssh.
    linhas_arquivo = []
    pub_key_authentication_yes_str = False
    password_authentication_no_str = False
    with open(os.path.join("/etc", "ssh", "sshd_config"), "r+") as sshd_config:
        linhas_arquivo = sshd_config.readlines()

        index = 0
        while index < len(linhas_arquivo):
            if linhas_arquivo[index] == "#PubkeyAuthentication yes":
                linhas_arquivo[index] = "PubkeyAuthentication yes"
                pub_key_authentication_yes_str = True
                break
            index += 1

        index = 0
        while index < len(linhas_arquivo):
            if linhas_arquivo[index] == "PasswordAuthentication yes":
                linhas_arquivo[index] = "PasswordAuthentication no"
                password_authentication_no_str = True
                break
            index += 1

    if pub_key_authentication_yes_str and password_authentication_no_str:
        with open(os.path.join("/etc", "ssh", "sshd_config"), "w") as sshd_config:
            for linha in linhas_arquivo:
                sshd_config.write("{}\n".format(linha))


def configurar_automatic_bug_reporting_tool():
    """
    Configura o Automatic Bug Reporting Tool
    """
    gerenciador_dnf.install(["abrt-desktop", "abrt-java-connector"])
    shell = Shell(AcaoQuandoOcorrerErro.IGNORAR)
    shell.executar("sudo systemctl enable abrtd.service")
    shell.executar("sudo systemctl start abrtd.service")


def main():
    """
    Método principal.
    """
    conectar_na_rede_wifi()
    registrar_red_hat()
    configurar_pacotes_dnf()
    instalar_pacotes_snap()
    instalar_pacotes_flatpak()
    instalar_pacotes_pip()
    configurar_java()
    configurar_script_de_atualizacao()
    configurar_virtualbox()
    configurar_firewall()
    configurar_automatic_bug_reporting_tool()


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

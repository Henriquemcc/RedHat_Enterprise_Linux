import enum
import subprocess
import platform

import requests

arquitetura = platform.processor()


class AcaoExecutadaQuandoOcorrerErro(enum.Enum):
    """
	Enum das ações a serem executadas caso ocorra algum erro
	"""

    # Aborta quando ocorrer erro
    ABORTAR = 0

    # Repete o comando quando ocorrer erro até o numero máximo de repetições. Quando o número máximo de repetições é
    # atingido o programa aborta
    REPETIR_E_ABORTAR = 1

    # Repete o comando quando ocorrer erro até o numero máximo de repetições. Quando o número máximo de repetições é
    # atingido o programa ignora o erro executando o próximo comando.
    REPETIR_E_IGNORAR = 2

    # Ignora o erro, seguindo para o próximo comando.
    IGNORAR = 3


def verificar_versao_sistema_operacional():
    """
	Verifica a versão do sistema operacional em que este script está rodando
	:return:
	"""
    distribuicao_linux = platform.dist()
    if distribuicao_linux[0] != 'redhat' or float(distribuicao_linux[1]) < 8.3 or float(distribuicao_linux[1]) >= 9.0 or \
            distribuicao_linux[2] != 'Ootpa':
        raise OSError("Versão de sistema operacional incompatível")


def executar_comando_shell(comando_shell, no_erro: AcaoExecutadaQuandoOcorrerErro,
                           numero_maximo_de_vezes_para_repetir: int = 0):
    """
    Executa um comando shell ou uma lista de comandos shell
    :param comando_shell: Comando shell ou lista de comandos
    shell a serem executados
    :param no_erro: O que deve ser feito caso algum erro ocorra
    :param numero_maximo_de_vezes_para_repetir: Caso o parâmetro no_erro for igual a REPETIR_E_ABORTAR ou
    REPETIR_E_IGNORAR, este parâmetro deverá ser passado indicando o número máximo de vezes que o programa deve repetir
    o comando shell caso ele resulte em erro
    """

    if type(comando_shell) is str:
        if no_erro == AcaoExecutadaQuandoOcorrerErro.ABORTAR:
            subprocess.run(comando_shell, shell=True, check=True)
        elif no_erro == AcaoExecutadaQuandoOcorrerErro.IGNORAR:
            try:
                subprocess.run(comando_shell, shell=True, check=True)
            except subprocess.CalledProcessError as erro:
                print(erro)
        elif no_erro == AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR or no_erro == AcaoExecutadaQuandoOcorrerErro.REPETIR_E_IGNORAR:
            for i in range(0, numero_maximo_de_vezes_para_repetir):
                try:
                    subprocess.run(comando_shell, shell=True, check=True)
                    break
                except subprocess.CalledProcessError as erro:
                    print(erro)
                    if no_erro == AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR and i == numero_maximo_de_vezes_para_repetir - 1:
                        raise erro
    elif type(comando_shell) is list:
        for i in comando_shell:
            executar_comando_shell(i, no_erro, numero_maximo_de_vezes_para_repetir)
    else:
        raise ValueError("O parâmetro comando_shell só pode ser dos tipos str e list.")


def instalar_programas_flatpak():
    """
	Instala os programas que utilizam o gerenciador de pacotes flatpak
	:return:
	"""
    comandos = \
        [
            "sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo",
            "sudo flatpak install --assumeyes flathub com.google.AndroidStudio"
        ]
    executar_comando_shell(comandos, AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def instalar_programas_snap():
    """
	Instala os programas que utilizam o gerenciador de pacotes snap
	:return:
	"""
    executar_comando_shell(
        [
            "sudo snap install spotify",
            "sudo snap install skype --classic",
            "sudo snap install intellij-idea-community --classic",
            "sudo snap install code --classic",
            "sudo snap install keepassxc --devmode",
            "sudo snap install pycharm-community --classic",
            "sudo snap install clion --classic",
            "sudo snap install rider --classic",
            "sudo snap install flutter --classic",
        ],
        AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def instalar_programas_pip():
    """
	Instala os programas que utilizam o gerenciador de pacotes python3 pip
	:return:
	"""
    executar_comando_shell("sudo pip3 install protonvpn-cli pycurl", AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR,
                           5)


def instalar_rust_lang():
    """
    Instala o compilador da linguagem Rust
    :return:
    """
    executar_comando_shell("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh;",
                           AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def configurar_visual_studio_code():
    """
    Configurar o Visual Studio Code
    :return:
    """

    executar_comando_shell(
        [
            "echo 'fs.inotify.max_user_watches=524288' | sudo tee --append /etc/sysctl.conf;",
            "sudo sysctl -p;",
            "git config --global core.editor \"code --wait\";"
        ],
        AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def instalar_extensoes_visual_studio_code():
    """
    Instala as extensões do Visual Studio Code
    :return
    """

    executar_comando_shell(
        [
            # Tradução do VS Code em Português
            "code --install-extension ms-ceintl.vscode-language-pack-pt-br;",

            # Linguagem C/C++
            "code --install-extension ms-vscode.cpptools;",
            "code --install-extension ms-vscode.cmake-tools;",
            "code --install-extension austin.code-gnu-global;",

            # Linguagem C#
            "code --install-extension ms-dotnettools.csharp;",

            # Linguagem Java
            "code --install-extension vscjava.vscode-java-debug;",
            "code --install-extension vscjava.vscode-maven;",
            "code --install-extension vscjava.vscode-java-dependency;",
            "code --install-extension vscjava.vscode-java-pack;",
            "code --install-extension vscjava.vscode-java-test;",
            "code --install-extension redhat.java;",

            # Linguagem Rust
            "code --install-extension matklad.rust-analyzer;",
            "code --install-extension vadimcn.vscode-lldb;",
            "code --install-extension rust-lang.rust;",

            # Linguagem Go
            "code --install-extension golang.Go;",

            # HTML, CSS e Javascript
            "code --install-extension ecmel.vscode-html-css;",
            "code --install-extension firefox-devtools.vscode-firefox-debug;",
            "code --install-extension msjsdiag.debugger-for-chrome;",
            "code --install-extension dbaeumer.vscode-eslint;",

            # Tema do VS Code
            "code --install-extension GitHub.github-vscode-theme;",

            # Markdown
            "code --install-extension DavidAnson.vscode-markdownlint;",

            # Powershell
            "code --install-extension ms-vscode.PowerShell;",

            # Indentação de código
            "code --install-extension NathanRidley.autotrim;",
            "code --install-extension esbenp.prettier-vscode;",

            # AI-assisted IntelliSense
            "code --install-extension VisualStudioExptTeam.vscodeintellicode;"
        ],
        AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def atualizar():
    """
	Atualiza os pacotes do sistema operacional.
	:return:
	"""
    executar_comando_shell("sudo dnf --assumeyes upgrade", AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def instalar_programas_dnf():
    """
	Instala os programas que utilizam o gerenciador de pacotes dnf
	:return:
	"""

    # Habilitando repositórios
    habilitar_repositorio_code_ready()
    habilitar_repositorio_baseos_rpms()
    habilitar_repositorio_appstream_rpms()
    habilitar_repositorio_fedora_epel()
    habilitar_repositorio_rpm_fusion()

    # Baixando e instalando programas RPM
    programas_rpm_baixados_da_internet = \
        [
            "https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm",
            "https://github.com/peazip/PeaZip/releases/download/7.7.1/peazip-7.7.1.LINUX.GTK2-1.x86_64.rpm",
            "{}".format(requests.get("https://teams.microsoft.com/downloads/desktopurl?env=production&plat=linux&arch=x64&download=true&linuxArchiveType=rpm").url),
        ]

    for i in programas_rpm_baixados_da_internet:
        executar_comando_shell("sudo dnf --assumeyes install {}".format(i))

    print("Instalando os programas")
    programas = \
        [
            # Libreoffice
            "libreoffice-writer.x86_64",
            "libreoffice-calc.x86_64",
            "libreoffice-impress.x86_64",
            "libreoffice-math.x86_64",
            "libreoffice-draw.x86_64",
            "libreoffice-langpack-pt-BR.x86_64",
            "libreoffice-langpack-en.x86_64",
            "unoconv.noarch",

            # Impressora HP
            "hplip.x86_64",

            # KVM
            "qemu-kvm",
            "libvirt",

            # Sistemas de arquivos não nativos do linux
            "ntfs-3g.x86_64",
            "exfat-utils fuse",
            "fuse-exfat",

            # Ferramentas de desenvolvimento
            "java-latest-openjdk-devel.x86_64",
            "java-1.8.0-openjdk-devel.x86_64",
            "golang.x86_64",
            "gcc.x86_64",
            "dotnet-sdk-5.0.x86_64",
            "aspnetcore-runtime-5.0",
            "dotnet-runtime-5.0",
            "git.x86_64",
            "git-lfs.x86_64",

            # Outros programas
            "stacer",
            "vlc",
            "youtube-dl.noarch",
            "snapd",
            "flatpak",
            "transmission.x86_64",
            "ffmpeg",
            "steam.i686",
            "wine.x86_64",
            "VirtualBox.x86_64",

        ]

    comando = "sudo dnf --assumeyes install"
    for programa in programas:
        comando += " {}".format(programa)
    executar_comando_shell(comando, AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)

def habilitar_repositorio_appstream_rpms():
    """
    Habilita o repositório rhel 8 for appstream
    """
    executar_comando_shell("sudo subscription-manager repos --enable=rhel-8-for-{}-appstream-rpms".format(arquitetura),
                           AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def habilitar_repositorio_baseos_rpms():
    """
    Habilita o repositório rhel 8 baseos
    """
    executar_comando_shell("sudo subscription-manager repos --enable=rhel-8-for-{}-baseos-rpms".format(arquitetura),
                           AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def habilitar_repositorio_code_ready():
    """
    Habilita o repositório codeready builder for rhel 8
    """
    executar_comando_shell(
        "sudo subscription-manager repos --enable=codeready-builder-for-rhel-8-{}-rpms".format(arquitetura),
        AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def habilitar_repositorio_rpm_fusion():
    """
    Habilita repositório RPM Fusion
    """
    executar_comando_shell(
        [
            "sudo dnf --assumeyes install --nogpgcheck https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm",
            "sudo dnf --assumeyes install --nogpgcheck https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-8.noarch.rpm"
        ]
        , AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)
    habilitar_repositorio_code_ready()
    executar_comando_shell(
        [
            "sudo dnf --assumeyes groupupdate core",
            "sudo dnf --assumeyes groupupdate multimedia --setop=\"install_weak_deps=False\" --exclude=PackageKit-gstreamer-plugin",
            "sudo dnf --assumeyes groupupdate sound-and-video",
            "sudo dnf install --assumeyes rpmfusion-free-release-tainted",
            "sudo dnf install --assumeyes rpmfusion-nonfree-release-tainted"
        ], AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def instalar_driver_nvidia():
    """
    Instala os drivers de vídeo da Nvidia
    """
    habilitar_repositorio_appstream_rpms()
    habilitar_repositorio_baseos_rpms()
    habilitar_repositorio_code_ready()

    executar_comando_shell(
        [
            # "sudo subscription-manager repos --enable=rhel-8-for-{}-appstream-rpms".format(arquitetura),
            # "sudo subscription-manager repos --enable=rhel-8-for-{}-baseos-rpms".format(arquitetura),
            # "sudo subscription-manager repos --enable=codeready-builder-for-rhel-8-{}-rpms".format(arquitetura),
            "sudo dnf --assumeyes config-manager --add-repo=https://developer.download.nvidia.com/compute/cuda/repos/rhel8/{}/cuda-rhel8.repo".format(
                arquitetura),
            "sudo dnf --assumeyes module install nvidia-driver:latest-dkms"
        ],
        AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def habilitar_repositorio_fedora_epel():
    """
    Habilita o repositório fedora epel
    """
    executar_comando_shell(
        "sudo dnf --assumeyes install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm",
        AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)
    habilitar_repositorio_code_ready()


def instalar_free_file_sync():
    """
	Instala o programa Free File Sync
	:return:
	"""
    executar_comando_shell(
        [
            "wget https://freefilesync.org/download/FreeFileSync_11.6_Linux.tar.gz",
            "tar -xvzf ./FreeFileSync_11.6_Linux.tar.gz",
            "./FreeFileSync_11.6_Linux/FreeFileSync_11.6_Install.run",
        ],
        AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)


def criar_atalho_para_o_java_jre():

        with open("java.desktop", "w") as atalho:
            atalho.write("[Desktop Entry]\n")
            atalho.write("Name=Java Runtime Environment\n")
            atalho.write("Comment=Java Runtime Environment\n")
            atalho.write("GenericName=Java\n")
            atalho.write("Keywords=java\n")
            atalho.write("Exec=java -jar %f\n")
            atalho.write("Terminal=false\n")
            atalho.write("X-MultipleArgs=false\n")
            atalho.write("Type=Application\n")
            atalho.write("MimeType=application/x-java-archive\n")
            atalho.write("StartupNotify=true\n")

        executar_comando_shell("sudo cp ./java.desktop /usr/share/applications/java.desktop", AcaoExecutadaQuandoOcorrerErro.REPETIR_E_ABORTAR, 5)



def main():
    """
	Função principal
	:return:
	"""
    parte = 0
    total = 11

    # Verificando a versão do sistema operacional
    parte += 1
    print("(", parte, "/", total, ")", "Verificando versão do sistema operacional")
    verificar_versao_sistema_operacional()

    # Atualizando o sistema
    parte += 1
    print("(", parte, "/", total, ")", "Atualizando o sistema")
    atualizar()

    # Instalando drivers da Nvidia
    parte += 1
    print("(", parte, "/", total, ")", "Instalando o driver da Nvidia")
    instalar_driver_nvidia()

    # Instalando programas pelo pip
    parte += 1
    print("(", parte, "/", total, ")", "Instalando programas pelo gerenciador de pacotes python pip")
    instalar_programas_pip()

    # Instalando programas pelo dnf
    parte += 1
    print("(", parte, "/", total, ")", "Instalando programas pelo gerenciador de pacotes dnf")
    instalar_programas_dnf()

    # Instalando programas pelo flatpak
    parte += 1
    print("(", parte, "/", total, ")", "Instalando programas pelo gerenciador de pacotes flatpak")
    instalar_programas_flatpak()

    # Instalando programas pelo snap
    parte += 1
    print("(", parte, "/", total, ")", "Instalando programas pelo gerenciador de pacotes snap")
    instalar_programas_snap()

    # Instalando o compilador de Rust Lang
    parte += 1
    print("(", parte, "/", total, ")", "Instalando o compilador de Rust Lang")
    instalar_rust_lang()

    # Configurando o Visual Studio Code
    parte += 1
    print("(", parte, "/", total, ")", "Configurando o Visual Studio Code")
    configurar_visual_studio_code()
    instalar_extensoes_visual_studio_code()

    # # Definindo variáveis de ambiente
    # parte += 1
    # print("(", parte, "/", total, ")", "Definindo variáveis de ambiente")
    # definir_variaveis_ambiente()

    # Criando atalho do Java
    parte += 1
    print("(", parte, "/", total, ")", "Criando atalho do Java")
    criar_atalho_para_o_java_jre()

    # Free File Sync
    parte += 1
    print("(", parte, "/", total, ")", "Instalando o Free File Sync")
    instalar_free_file_sync()

    # Exibindo mensagem de instalação concluída
    print("Instalação concluída!")


if __name__ == "__main__":
    main()

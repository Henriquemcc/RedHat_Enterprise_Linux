import io
import os
from os.path import expanduser

from adapter.Pip import Pip
from adapter.Shell import Shell, AcaoQuandoOcorrerErro
from adapter.VisualStudioCode import VisualStudioCode

gerenciador_pip = Pip()
gerenciador_visual_studio_code = VisualStudioCode()


def instalar_pacotes_pip():
    """
    Instala o gerenciador de pacotes Pip e os pacotes Pip.
    """
    Pip.instalar_pip()
    gerenciador_pip.install("protonvpn-cli")


def configurar_gnome():
    """
    Configura o Gnome personalizando as configurações.
    """
    shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)

    # Desabilitando hot corners:
    # https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/using_the_desktop_environment_in_rhel_8/getting-started-with-gnome_using-the-desktop-environment-in-rhel-8#disabling-the-hot-corner-functionality-for-a-single-user_disabling-the-hot-corner-functionality-on-gnome-shell
    shell.executar("gsettings set org.gnome.desktop.interface enable-hot-corners false")

    # Mostrar segundos
    shell.executar("gsettings set org.gnome.desktop.interface clock-show-seconds true")

    # Mostrar dia da semana
    shell.executar("gsettings set org.gnome.desktop.interface clock-show-weekday true")

    # Mostrar porcentagem da bateria
    shell.executar("gsettings set org.gnome.desktop.interface show-battery-percentage true")

    # Habilitar atualização de fuso horário
    shell.executar("gsettings set org.gnome.desktop.datetime automatic-timezone true")

    # Desabilitar autorun
    shell.executar("gsettings set org.gnome.desktop.media-handling autorun-never true")

    # Habilitar o fractional scaling
    shell.executar("gsettings set org.gnome.mutter experimental-features \"['scale-monitor-framebuffer']\"")


def configurar_diretorio_home_bin():
    """
    Configura o diretório ~/bin adicionando ele ao .bashrc
    """
    diretorio_home = expanduser("~")
    path_bash_rc = "{}/.bashrc".format(diretorio_home)
    export_bin_string = "export PATH=\"$HOME/bin:$PATH\""
    # Verificando se o arquivo contem o export path
    with open(path_bash_rc, "r+") as arquivo:
        linhas = arquivo.readlines()
        if not any(export_bin_string in linha for linha in linhas):
            arquivo.seek(0, io.SEEK_END)
            arquivo.write("{}\n".format(export_bin_string))


def configurar_adb():
    """
    Configura o Android ADB.
    """
    configurar_diretorio_home_bin()
    diretorio_home = expanduser("~")
    path_adb = "{}/Android/Sdk/platform-tools/adb".format(diretorio_home)
    path_pasta_atalho = "{}/bin".format(diretorio_home)
    path_atalho = "{}/adb".format(path_pasta_atalho)

    try:
        os.mkdir(path_pasta_atalho)
    except FileExistsError as e:
        print(e)

    shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
    shell.executar("ln --symbolic {} {}".format(path_adb, path_atalho))


def instalar_extensoes_visual_studio_code():
    """
    Instala as extensões do Visual Studio Code.
    """
    VisualStudioCode.instalar_visual_studio_code()
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
    """
    Instala o compilador e o gerenciador de dependências da linguagem de programação Rust.
    """
    shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
    shell.executar("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
    shell.executar("source $HOME/.cargo/env")


def main():
    """
    Método principal.
    """
    instalar_pacotes_pip()
    configurar_adb()
    configurar_gnome()
    instalar_extensoes_visual_studio_code()
    instalar_rust_lang()


if __name__ == '__main__':
    main()

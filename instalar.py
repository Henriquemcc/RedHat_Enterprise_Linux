"""
Este programa em Python serve para instalar os meus programas na minha estação de trabalho com o sistema operacional Red Hat Enterprise Linux
"""


def importar():
	"""
	Instala e importa as bibliotecas necessárias para este código rodar
	"""
	for repeticao in range(0, 2):
		try:
			import enum
			import platform
			import subprocess
			import requests
			import distro
			import os
			break
		except ImportError as e:
			instalar_pacotes_pip("distro")
			if repeticao == 1:
				raise e


importar()

# Inútil, mas necessário para o PyCharm não colorir meu código de vermelho
import enum
import os
import platform
import subprocess

import distro
import requests

# Obtendo a arquitetura do processador
arquitetura = platform.processor()

# Criando uma lista de strings para armazenar os comandos que deverão ser executados ao reiniciar o sistema
comandos_shell_serem_executados_depois_de_reiniciar = []

# Nome do arquivo de credenciais da Red Hat
nome_arquivo_credenciais_red_hat = "RedHatCredentials.cfg"


class AcaoQuandoOcorrerErro(enum.Enum):
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


def executar_comando_shell(comando_shell, no_erro: AcaoQuandoOcorrerErro = AcaoQuandoOcorrerErro.REPETIR_E_ABORTAR,
                           numero_maximo_de_vezes_para_repetir: int = 5):
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
		if no_erro == AcaoQuandoOcorrerErro.ABORTAR:
			subprocess.run(comando_shell, shell=True, check=True)
		elif no_erro == AcaoQuandoOcorrerErro.IGNORAR:
			try:
				subprocess.run(comando_shell, shell=True, check=True)
			except subprocess.CalledProcessError as erro:
				print(erro)
		elif no_erro == AcaoQuandoOcorrerErro.REPETIR_E_ABORTAR or no_erro == AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR:
			for repeticao in range(0, numero_maximo_de_vezes_para_repetir):
				try:
					subprocess.run(comando_shell, shell=True, check=True)
					break
				except subprocess.CalledProcessError as erro:
					print(erro)
					if no_erro == AcaoQuandoOcorrerErro.REPETIR_E_ABORTAR and repeticao == numero_maximo_de_vezes_para_repetir - 1:
						raise erro
	elif type(comando_shell) is list:
		for repeticao in comando_shell:
			executar_comando_shell(repeticao, no_erro, numero_maximo_de_vezes_para_repetir)
	else:
		raise ValueError("O parâmetro comando_shell só pode ser dos tipos str e list.")


def verificar_versao_sistema_operacional():
	"""
	Verifica a versão do sistema operacional em que este script está rodando
	"""
	if distro.name() != 'Red Hat Enterprise Linux' or distro.codename() != 'Ootpa' or float(
			distro.version()) < 8.3 or float(distro.version()) >= 9.0:
		raise OSError("Versão de sistema operacional incompatível")
	print("OK")


def registrar_red_hat():
	"""
	Registra o sistema na conta Red Hat para poder utilizar os repositórios da Red Hat
	"""
	existe = os.path.exists(nome_arquivo_credenciais_red_hat)
	with open(nome_arquivo_credenciais_red_hat, "r+") as credenciais_red_hat:
		if existe:
			usuario = credenciais_red_hat.readline()
			senha = credenciais_red_hat.readline()
		else:
			print("O arquivo de credenciais da Red Hat {} não existe".format(nome_arquivo_credenciais_red_hat))
			print("Criando o arquivo de credenciais da Red Hat:")
			usuario = input("Usuário: ")
			senha = input("Senha: ")
			credenciais_red_hat.writelines([usuario, senha])
		credenciais_red_hat.close()

	executar_comando_shell("sudo subscription-manager register --username {} --password {}".format(usuario, senha),
	                       AcaoQuandoOcorrerErro.IGNORAR)


def instalar_programas_flatpak():
	"""
	Instala os programas que utilizam o gerenciador de pacotes flatpak
	"""
	comandos = ["sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo",
	            "sudo flatpak install --assumeyes flathub com.google.AndroidStudio"]
	executar_comando_shell(comandos)


def instalar_pacotes_snap(pacotes, parametros: str = None):
	"""
	Instala os pacotes utilizando o gerenciador de pacotes snap
	:param pacotes: Pacotes que serão instalados
	:param parametros: parâmetros extras para a instalação dos pacotes
	"""
	if type(pacotes) is str:
		for repeticao in range(0, 2):
			# Instalando pacotes e em caso de erro tentando instalar o snapd e repetindo a instalação dos pacotes
			try:
				if parametros is None:
					executar_comando_shell("sudo snap install {}".format(pacotes),
					                       AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR)
				else:
					executar_comando_shell("sudo snap install {} {}".format(pacotes, parametros),
					                       AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR)
				break
			except Exception as e:
				instalar_snapd()
				if repeticao == 1:
					raise e

	elif type(pacotes) is list:
		for pacote in pacotes:
			instalar_pacotes_snap(pacote, parametros)


def instalar_programas_snap():
	"""
	Instala os programas que utilizam o gerenciador de pacotes snap
	"""

	instalar_pacotes_snap("keepassxc", "--devmode")
	instalar_pacotes_snap("spotify")
	instalar_pacotes_snap(
		["code", "intellij-idea-community", "pycharm-community", "flutter", "kotlin", "skype", "clion", "rider"],
		"--classic")


def instalar_pacotes_pip(pacotes):
	"""
	Instala os pacotes utilizando o gerenciador de pacotes python pip
	:param pacotes: Pacotes que serão instalados
	"""
	if type(pacotes) is str:
		for repeticao in range(0, 2):
			try:
				executar_comando_shell("sudo pip3 install {}".format(pacotes))
				break
			except Exception as e:
				instalar_pacotes_dnf("python3-pip.noarch")
				if repeticao == 1:
					raise e

	elif type(pacotes) is list:
		for pacote in pacotes:
			instalar_pacotes_pip(pacote)


def instalar_programas_pip():
	"""
	Instala os programas que utilizam o gerenciador de pacotes python3 pip
	"""
	instalar_pacotes_pip(["protonvpn-cli", "pycurl"])


def instalar_rust_lang():
	"""
	Instala o compilador da linguagem Rust
	"""
	executar_comando_shell("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh;")


def configurar_visual_studio_code():
	"""
	Configurar o Visual Studio Code
	"""
	executar_comando_shell(
		["echo 'fs.inotify.max_user_watches=524288' | sudo tee --append /etc/sysctl.conf;", "sudo sysctl -p;",
		 "git config --global core.editor \"code --wait\";"])


def instalar_extensoes_visual_studio_code():
	"""
	Instala as extensões do Visual Studio Code
	"""

	executar_comando_shell([  # Tradução do VS Code em Português
		"code --install-extension ms-ceintl.vscode-language-pack-pt-br;",

		# Linguagem C/C++
		"code --install-extension ms-vscode.cpptools;", "code --install-extension ms-vscode.cmake-tools;",
		"code --install-extension austin.code-gnu-global;",

		# Linguagem C#
		"code --install-extension ms-dotnettools.csharp;",

		# Linguagem Java
		"code --install-extension vscjava.vscode-java-debug;", "code --install-extension vscjava.vscode-maven;",
		"code --install-extension vscjava.vscode-java-dependency;",
		"code --install-extension vscjava.vscode-java-pack;", "code --install-extension vscjava.vscode-java-test;",
		"code --install-extension redhat.java;",

		# Linguagem Rust
		"code --install-extension matklad.rust-analyzer;", "code --install-extension vadimcn.vscode-lldb;",
		"code --install-extension rust-lang.rust;",

		# Linguagem Go
		"code --install-extension golang.Go;",

		# HTML, CSS e Javascript
		"code --install-extension ecmel.vscode-html-css;",
		"code --install-extension firefox-devtools.vscode-firefox-debug;",
		"code --install-extension msjsdiag.debugger-for-chrome;", "code --install-extension dbaeumer.vscode-eslint;",

		# Tema do VS Code
		"code --install-extension GitHub.github-vscode-theme;",

		# Markdown
		"code --install-extension DavidAnson.vscode-markdownlint;",

		# Powershell
		"code --install-extension ms-vscode.PowerShell;",

		# Indentação de código
		"code --install-extension NathanRidley.autotrim;", "code --install-extension esbenp.prettier-vscode;",

		# AI-assisted IntelliSense
		"code --install-extension VisualStudioExptTeam.vscodeintellicode;"])


def atualizar():
	"""
	Atualiza os pacotes do sistema operacional.
	"""
	executar_comando_shell("sudo dnf --assumeyes upgrade --refresh")


def instalar_pacotes_dnf(pacotes):
	"""
	Instala pacotes utilizando o DNF.
	:param pacotes: Lista de pacotes a serem instalados
	"""
	if type(pacotes) is str:
		executar_comando_shell("sudo dnf --assumeyes install {}".format(pacotes),
		                       AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR)

	elif type(pacotes) is list:
		for pacote in pacotes:
			instalar_pacotes_dnf(pacote)


def instalar_programas_dnf():
	"""
	Instala os programas que utilizam o gerenciador de pacotes dnf
	"""

	# Habilitando repositórios
	habilitar_repositorio_code_ready()
	habilitar_repositorio_baseos_rpms()
	habilitar_repositorio_appstream_rpms()
	habilitar_repositorio_fedora_epel()
	habilitar_repositorio_rpm_fusion()
	atualizar()

	print("Instalando os programas")
	programas = [

		# Programas externos
		"https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm",
		"https://github.com/peazip/PeaZip/releases/download/7.7.1/peazip-7.7.1.LINUX.GTK2-1.x86_64.rpm", "{}".format(
			requests.get(
				"https://teams.microsoft.com/downloads/desktopurl?env=production&plat=linux&arch=x64&download=true&linuxArchiveType=rpm").url),
		"https://download.teamviewer.com/download/linux/teamviewer.x86_64.rpm",

		# Libreoffice
		"libreoffice-writer.x86_64", "libreoffice-calc.x86_64", "libreoffice-impress.x86_64", "libreoffice-math.x86_64",
		"libreoffice-draw.x86_64", "libreoffice-langpack-pt-BR.x86_64", "libreoffice-langpack-en.x86_64",
		"unoconv.noarch",

		# Impressora HP
		"hplip.x86_64",

		# KVM
		"qemu-kvm", "libvirt",

		# Sistemas de arquivos não nativos do linux
		"ntfs-3g.x86_64", "exfat-utils fuse", "fuse-exfat",

		# Ferramentas de desenvolvimento
		"java-latest-openjdk-devel.x86_64", "java-1.8.0-openjdk-devel.x86_64", "golang.x86_64", "gcc.x86_64",
		"dotnet-sdk-5.0.x86_64", "aspnetcore-runtime-5.0", "dotnet-runtime-5.0", "git.x86_64", "git-lfs.x86_64",

		# Outros programas
		"stacer", "qt5-qtcharts.x86_64", "vlc", "qt5-qtsvg.x86_64", "youtube-dl.noarch", "snapd", "flatpak",
		"transmission.x86_64", "ffmpeg", "steam.i686", "wine.x86_64", "VirtualBox.x86_64", "mokutil.x86_64", "fdupes",
		"dnf-automatic"

	]

	instalar_pacotes_dnf(programas)


def habilitar_repositorio_appstream_rpms():
	"""
	Habilita o repositório rhel 8 for appstream
	"""
	executar_comando_shell("sudo subscription-manager repos --enable=rhel-8-for-{}-appstream-rpms".format(arquitetura))


def habilitar_repositorio_baseos_rpms():
	"""
	Habilita o repositório rhel 8 baseos
	"""
	executar_comando_shell("sudo subscription-manager repos --enable=rhel-8-for-{}-baseos-rpms".format(arquitetura))


def habilitar_repositorio_code_ready():
	"""
	Habilita o repositório codeready builder for rhel 8
	"""
	executar_comando_shell(
		"sudo subscription-manager repos --enable=codeready-builder-for-rhel-8-{}-rpms".format(arquitetura))


def habilitar_repositorio_rpm_fusion():
	"""
	Habilita repositório RPM Fusion
	"""
	executar_comando_shell([
		"sudo dnf --assumeyes install --nogpgcheck https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm",
		"sudo dnf --assumeyes install --nogpgcheck https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-8.noarch.rpm"])
	habilitar_repositorio_code_ready()
	executar_comando_shell(["sudo dnf --assumeyes groupupdate core",
	                        "sudo dnf --assumeyes groupupdate multimedia --setop=\"install_weak_deps=False\" --exclude=PackageKit-gstreamer-plugin",
	                        "sudo dnf --assumeyes groupupdate sound-and-video", ])
	instalar_pacotes_dnf(["rpmfusion-free-release-tainted", "rpmfusion-nonfree-release-tainted"])


def instalar_driver_nvidia():
	"""
	Instala os drivers de vídeo da Nvidia
	"""
	habilitar_repositorio_appstream_rpms()
	habilitar_repositorio_baseos_rpms()
	habilitar_repositorio_code_ready()
	executar_comando_shell([
		"sudo dnf --assumeyes config-manager --add-repo=https://developer.download.nvidia.com/compute/cuda/repos/rhel8/x86_64/cuda-rhel8.repo",
		"sudo dnf --assumeyes module install nvidia-driver", "sudo nvidia-modprobe"])


def habilitar_repositorio_fedora_epel():
	"""
	Habilita o repositório fedora epel
	"""
	instalar_pacotes_dnf("https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm")
	habilitar_repositorio_code_ready()


def criar_atalho_para_o_java_jre():
	"""
	Cria um atalho ao Java Runtime Environment para que ele possa ser executado ao clicar no nautilus em um arquivo .jar
	"""
	with open("java.desktop", "w") as arquivo_atalho:
		arquivo_atalho.writelines(
			["[Desktop Entry]\n", "Name=Java Runtime Environment\n", "Comment=Java Runtime Environment\n",
			 "GenericName=Java\n", "Keywords=java\n", "Exec=java -jar %f\n", "Terminal=false\n",
			 "X-MultipleArgs=false\n", "Type=Application\n", "MimeType=application/x-java-archive\n",
			 "StartupNotify=true\n", "Icon=java-1.8.0-openjdk\n"])
		arquivo_atalho.close()
	executar_comando_shell("sudo cp --force ./java.desktop /usr/share/applications/java.desktop")


def instalar_snapd():
	"""
	Instala o snapd, gerenciador de pacotes snap
	"""
	for repeticao in range(0, 2):
		try:
			instalar_pacotes_dnf("snapd")
			executar_comando_shell("sudo systemctl enable --now snapd.socket")
			executar_comando_shell("sudo ln -s /var/lib/snapd/snap /snap", AcaoQuandoOcorrerErro.IGNORAR)
			break
		except Exception as e:
			habilitar_repositorio_fedora_epel()
			if repeticao == 1:
				raise e


def configurar_adb():
	"""
	Configura o ADB para que ele possa ser executado a partir da linha de comando estando dentro de qualquer pasta
	"""
	executar_comando_shell("sudo ln --symbolic /home/henrique/Android/Sdk/platform-tools/adb /bin/adb",
	                       AcaoQuandoOcorrerErro.IGNORAR)


def assinar_modulos_kernel_virtualbox():
	"""
	Assina os módulos do virtualbox no kernel Linux para serem compatíveis com o SecureBoot
	"""
	instalar_pacotes_dnf("mokutil")
	executar_comando_shell("sudo mkdir /root/signed-modules", AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR)
	executar_comando_shell([
		"sudo openssl req -new -x509 -newkey rsa:2048 -keyout /root/signed-modules/MOK.priv -outform DER -out /root/signed-modules/MOK.der -nodes -days 36500 -subj '/CN=VirtualBox/'",
		"sudo chmod 600 /root/signed-modules/MOK.priv", "sudo mokutil --import /root/signed-modules/MOK.der"])

	with open("sign-virtual-box", "w") as arquivo_assinar_modulos_virtualbox:
		arquivo_assinar_modulos_virtualbox.writelines(
			["#!/bin/bash", "for modfile in $(dirname $(modinfo -n vboxdrv))/*.ko; do", "  echo \"Signing $modfile\"",
			 "  /usr/src/kernels/$(uname -r)/scripts/sign-file sha256 \\",
			 "                                /root/signed-modules/MOK.priv \\",
			 "                                /root/signed-modules/MOK.der \"$modfile\"", "done"])
		arquivo_assinar_modulos_virtualbox.close()
	executar_comando_shell(["sudo cp ./sign-virtual-box /root/signed-modules/sign-virtual-box",
	                        "sudo chmod 700 /root/signed-modules/sign-virtual-box"])

	comandos_shell_serem_executados_depois_de_reiniciar.append("sudo /root/signed-modules/sign-virtual-box")
	comandos_shell_serem_executados_depois_de_reiniciar.append("sudo modprobe vboxdrv")


def configurar_atualizacoes_automaticas():
	"""
	Configura as atualizações automáticas utilizando o DNF Automatic
	"""

	# Instalando o DNF Automatic
	instalar_pacotes_dnf("dnf-automatic")

	# Copiando arquivo do configuração do DNF Automatic para ser modificado
	executar_comando_shell(
		["sudo cp /etc/dnf/automatic.conf ./automatic.conf.original", "sudo chmod 666 ./automatic.conf.original"])

	# Modificando arquivo de configuração do DNF Automatic
	with open("automatic.conf.original", "r") as arquivo_original, open("automatic.conf.modificado",
	                                                                    "w") as arquivo_modificado:
		for linha in arquivo_original:
			if "apply_updates =" in linha:
				arquivo_modificado.write("apply_updates = yes")
			else:
				arquivo_modificado.write(linha)
		arquivo_original.close()
		arquivo_modificado.close()

	# Copiando arquivo de configuração do DNF Automatic modificado
	executar_comando_shell("sudo cp --force ./automatic.conf.modificado /etc/dnf/automatic.conf")

	# Habilitando DNF Automatic
	executar_comando_shell("sudo systemctl enable --now dnf-automatic-notifyonly.timer")

	# Movendo arquivos não mais necessários para a lixeira
	executar_comando_shell("gio trash ./automatic.conf.original ./automatic.conf.modificado")


def main():
	"""
	Função principal
	"""
	parte = 0
	total = 16

	# Verificando a versão do sistema operacional
	parte += 1
	print("(", parte, "/", total, ")", "Verificando versão do sistema operacional")
	verificar_versao_sistema_operacional()

	# Registrando sistema na Red Hat
	parte += 1
	print("(", parte, "/", total, ")", "Registrando Sistema na Red Hat")
	registrar_red_hat()

	# Atualizando o sistema
	parte += 1
	print("(", parte, "/", total, ")", "Atualizando o sistema")
	atualizar()

	# Instalando programas pelo pip
	parte += 1
	print("(", parte, "/", total, ")", "Instalando programas pelo gerenciador de pacotes python pip")
	instalar_programas_pip()

	# Instalando programas pelo dnf
	parte += 1
	print("(", parte, "/", total, ")", "Instalando programas pelo gerenciador de pacotes dnf")
	instalar_programas_dnf()

	# Configurando atualizações automáticas
	parte += 1
	print("(", parte, "/", total, ")", "Configurando atualizações automáticas")
	configurar_atualizacoes_automaticas()

	# Instalando programas pelo flatpak
	parte += 1
	print("(", parte, "/", total, ")", "Instalando programas pelo gerenciador de pacotes flatpak")
	instalar_programas_flatpak()

	# Instalando o snapd
	parte += 1
	print("(", parte, "/", total, ")", "Instalando o Snapd")
	instalar_snapd()

	# Instalando programas pelo snap
	parte += 1
	print("(", parte, "/", total, ")", "Instalando programas pelo gerenciador de pacotes snap")
	instalar_programas_snap()

	# Instalando drivers da Nvidia
	parte += 1
	print("(", parte, "/", total, ")", "Instalando o driver da Nvidia")
	instalar_driver_nvidia()

	# Instalando o compilador de Rust Lang
	parte += 1
	print("(", parte, "/", total, ")", "Instalando o compilador de Rust Lang")
	instalar_rust_lang()

	# Criando atalho do Java
	parte += 1
	print("(", parte, "/", total, ")", "Criando atalho do Java")
	criar_atalho_para_o_java_jre()

	# Adb
	parte += 1
	print("(", parte, "/", total, ")", "Configurando o ADB")
	configurar_adb()

	# Virtualbox
	parte += 1
	print("(", parte, "/", total, ")", "Assinando módulos do Virtualbox para o Kernel Linux em Secureboot")
	assinar_modulos_kernel_virtualbox()

	# Configurando o Visual Studio Code
	parte += 1
	print("(", parte, "/", total, ")", "Configurando o Visual Studio Code")
	configurar_visual_studio_code()
	instalar_extensoes_visual_studio_code()

	# Exibindo mensagem de instalação concluída
	print("Instalação concluída!")


if __name__ == "__main__":
	main()

from adapter.Shell import Shell, AcaoQuandoOcorrerErro
from adapter.SubscriptionManager import SubscriptionManager


class Dnf:
    """
    Classe que realiza a comunicação do código Python com o gerenciador de pacotes DNF.
    """

    def __init__(self):
        """
        Método construtor.
        """
        self.__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
        self.__subscription_manager = SubscriptionManager()

    def install(self, pacote):
        """
        Instala pacote(s) do gerenciador de pacotes DNF
        :param pacote: Pacote(s) a ser(em) instalado(s).
        """
        if type(pacote) is str:
            self.__shell.executar("sudo dnf --assumeyes install {}".format(pacote))
        elif type(pacote) is list:
            for p in pacote:
                self.install(p)

    def upgrade(self):
        """
        Atualiza pacote(s) do gerenciador de pacotes DNF.
        """
        self.__shell.executar("sudo dnf --assumeyes upgrade --refresh")

    def config_manager_add_repo(self, repo):
        """
        Adiciona repositório(s) ao gerenciador de pacotes DNF.
        :param repo: Repositório(s) a ser(em) adicionado(s).
        """
        if type(repo) is str:
            self.__shell.executar("sudo dnf --assumeyes config-manager --add-repo={}".format(repo))
        elif type(repo) is list:
            for r in repo:
                self.config_manager_add_repo(r)

    def module_install(self, module):
        """
        Instala módulo(s) do gerenciador de pacotes DNF.
        :param module: Módulo(s) a ser(em) instalados.
        """
        if type(module) is str:
            self.__shell.executar("sudo dnf --assumeyes module install {}".format(module))
        elif type(module) is list:
            for m in module:
                self.module_install(m)

    def group_update(self, group):
        """
        Atualiza pacote(s) de um ou mais grupo de pacotes DNF.
        :param group: Grupo(s) a serem atualizados.
        """
        if type(group) is str:
            self.__shell.executar("sudo dnf --assumeyes group update {}".format(group))
        elif type(group) is list:
            for g in group:
                self.group_update(g)

    def group_install(self, group):
        """
        Instala grupo(s) de pacotes do gerenciador de pacotes DNF.
        :param group: Grupo(s) de pacotes a ser(em) instalados.
        """
        if type(group) is str:
            self.__shell.executar("sudo dnf --assumeyes group install {}".format(group))
        elif type(group) is list:
            for g in group:
                self.group_install(g)

    def habilitar_fedora_epel(self):
        """
        Habilita o repositório Fedora EPEL.
        """
        self.install("https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm")
        self.__subscription_manager.habilitar_codeready_builder()

    def habilitar_rpm_fusion(self):
        """
        Habilita o repositório RPM Fusion.
        """
        self.install("https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm")
        self.install("https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-8.noarch.rpm")
        self.habilitar_fedora_epel()
        self.__subscription_manager.habilitar_codeready_builder()
        self.group_update("core")
        self.group_update("multimedia --setop=\"install_weak_deps=False\" --exclude=PackageKit-gstreamer-plugin")
        self.group_update("sound-and-video")
        self.install("rpmfusion-free-release-tainted")
        self.install("rpmfusion-nonfree-release-tainted")

    def configurar_atualizacoes_automaticas(self):
        """
        Configura as atualizações automáticas de pacotes do gerenciador DNF.
        """
        self.install("dnf-automatic")
        shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_ABORTAR, 1024)
        shell.executar("sudo cp /etc/dnf/automatic.conf ./automatic.conf.original")
        shell.executar("sudo chmod 666 ./automatic.conf.original")

        # Modificando arquivo de configuração do DNF Automatic
        with open("automatic.conf.original", "r") as arquivo_original, \
                open("automatic.conf.modificado", "w") as arquivo_modificado:
            for linha in arquivo_original:
                if "apply_updates =" in linha:
                    arquivo_modificado.write("apply_updates = yes")
                else:
                    arquivo_modificado.write(linha)
            arquivo_original.close()
            arquivo_modificado.close()

        # Copiando arquivo de configuração do DNF Automatic modificado
        shell.executar("sudo cp --force ./automatic.conf.modificado /etc/dnf/automatic.conf")

        # Habilitando DNF Automatic
        shell.executar("sudo systemctl enable --now dnf-automatic-notifyonly.timer")

        # Movendo arquivos não mais necessários para a lixeira
        shell.executar("gio trash ./automatic.conf.original ./automatic.conf.modificado")

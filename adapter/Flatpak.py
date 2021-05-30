from adapter.Dnf import Dnf
from adapter.Shell import Shell, AcaoQuandoOcorrerErro


class Flatpak:
    """
    Classe que realiza a comunicação do código Python com o gerenciador de pacotes Flatpak.
    """

    def __init__(self):
        """
        Método construtor.
        """
        self.__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)

    def install(self, package):
        """
        Instala pacote(s) Flatpak.
        :param package: Pacote(s) a ser(em) instalado(s).
        """
        if type(package) is str:
            self.__shell.executar("sudo flatpak install --system --assumeyes {}".format(package))
        elif type(package) is list:
            for p in package:
                self.install(p)

    def update(self):
        """
        Atualiza pacote(s) Flatpak.
        """
        self.__shell.executar("sudo flatpak update --assumeyes")

    def remote_add(self, repository):
        """
        Adiciona repositório(s) Flatpak.
        :param repository: Repositório(s) Flatpak a ser(em) adicionado(s).
        """
        if type(repository) is str:
            self.__shell.executar("sudo flatpak remote-add --if-not-exists {}".format(repository))
        elif type(repository) is list:
            for r in repository:
                self.remote_add(r)

    @staticmethod
    def instalar_flatpak():
        """
        Instala o gerenciador de pacotes flatpak.
        """
        Dnf().install("flatpak")

    def habilitar_flathub(self):
        """
        Habilita o repositório do Flathub.
        """
        self.remote_add("flathub https://flathub.org/repo/flathub.flatpakrepo")

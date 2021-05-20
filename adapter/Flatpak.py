from adapter.Dnf import Dnf
from adapter.Shell import Shell, AcaoQuandoOcorrerErro


class Flatpak:
    def __init__(self):
        self.__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)

    def install(self, package):
        if type(package) is str:
            self.__shell.executar("sudo flatpak install --system --assumeyes {}".format(package))
        elif type(package) is list:
            for p in package:
                self.install(p)

    def update(self):
        self.__shell.executar("sudo flatpak update --assumeyes")

    def remote_add(self, repository):
        if type(repository) is str:
            self.__shell.executar("sudo flatpak remote-add --if-not-exists {}".format(repository))
        elif type(repository) is list:
            for r in repository:
                self.remote_add(r)

    @staticmethod
    def instalar_flatpak():
        Dnf().install("flatpak")

    def habilitar_flathub(self):
        self.remote_add("flathub https://flathub.org/repo/flathub.flatpakrepo")

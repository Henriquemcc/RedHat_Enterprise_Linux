from adapter.Dnf import Dnf
from adapter.Shell import AcaoQuandoOcorrerErro, Shell


class Snap:

    def __init__(self):
        self.__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)

    def install(self, pacote):
        if type(pacote) is str:
            self.__shell.executar("sudo snap install {}".format(pacote))
        elif type(pacote) is list:
            for p in pacote:
                self.install(p)

    def refresh(self):
        self.__shell.executar("sudo snap refresh")

    def instalar_snapd(self):
        dnf = Dnf()
        dnf.habilitar_fedora_epel()
        dnf.install("snapd")
        self.__shell.executar("sudo systemctl enable --now snapd.socket")
        self.__shell.executar("sudo ln -s /var/lib/snapd/snap /snap")

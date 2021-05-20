from adapter.Dnf import Dnf
from adapter.Shell import Shell, AcaoQuandoOcorrerErro


class Pip:
    def __init__(self):
        self.__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)

    def install(self, pacote):
        if type(pacote) is str:
            self.__shell.executar("sudo pip3 install {}".format(pacote))
        elif type(pacote) is list:
            for p in pacote:
                self.install(p)

    @staticmethod
    def instalar_pip():
        Dnf().install("python3-pip")

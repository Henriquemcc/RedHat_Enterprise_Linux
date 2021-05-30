from adapter.Dnf import Dnf
from adapter.Shell import Shell, AcaoQuandoOcorrerErro


class Pip:
    """
    Classe que realiza a comunicação do código Python com o gerenciador de pacotes Pip.
    """

    def __init__(self):
        """
        Método construtor
        """
        self.__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)

    def install(self, pacote):
        """
        Instala pacote(s) do gerenciador de pacotes Pip.
        :param pacote: Pacote(s) a ser(em) instalado(s).
        """
        if type(pacote) is str:
            self.__shell.executar("pip3 install {}".format(pacote))
        elif type(pacote) is list:
            for p in pacote:
                self.install(p)

    @staticmethod
    def instalar_pip():
        """
        Instala o gerenciador de pacotes Pip.
        """
        Dnf().install("python3-pip")

from adapter.Shell import Shell, AcaoQuandoOcorrerErro
from adapter.Snap import Snap


class VisualStudioCode:
    """
    Classe que realiza a comunicação do código Python com o Visual Studio Code.
    """

    def __init__(self):
        """
        Método construtor.
        """
        self.__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)

    def install_extension(self, extension):
        """
        Instala extensão(ões) do Visual Studio Code.
        :param extension: Extensão(ões) a ser(em) instalada(s).
        """
        if type(extension) is str:
            self.__shell.executar("code --install-extension {}".format(extension))
        elif type(extension) is list:
            for e in extension:
                self.install_extension(e)

    @staticmethod
    def instalar_visual_studio_code():
        """
        Instala o Visual Studio Code.
        """
        Snap.instalar_snapd()
        gerenciador_snap = Snap()
        gerenciador_snap.install("code --classic")

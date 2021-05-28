from adapter.Dnf import Dnf
from adapter.Shell import AcaoQuandoOcorrerErro, Shell


class Snap:
    """
    Classe que realiza a comunicação do código Python com o gerenciador de pacotes Snap.
    """

    def __init__(self):
        """
        Método construtor.
        """
        self.__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)

    def install(self, pacote):
        """
        Instala pacote(s) Snap.
        :param pacote: Pacote(s) snap a ser(em) instalado(s).
        """
        if type(pacote) is str:
            self.__shell.executar("sudo snap install {}".format(pacote))
        elif type(pacote) is list:
            for p in pacote:
                self.install(p)

    def refresh(self):
        """
        Atualiza pacote(s) Snap.
        """
        self.__shell.executar("sudo snap refresh")

    @staticmethod
    def instalar_snapd():
        """
        Instala o gerenciador de pacotes Snap.
        """
        dnf = Dnf()
        dnf.habilitar_fedora_epel()
        dnf.install("snapd")
        shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
        shell.executar("sudo systemctl enable --now snapd.socket")
        shell.executar("sudo ln -s /var/lib/snapd/snap /snap")

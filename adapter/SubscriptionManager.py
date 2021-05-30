import platform

from adapter.Shell import Shell, AcaoQuandoOcorrerErro


class SubscriptionManager:
    """
    Classe que realiza a comunicação do código Python com o Red Hat Subscription Manager.
    """

    def __init__(self):
        """
        Método construtor.
        """
        self.__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
        self.__arquitetura = platform.processor()

    def repos_enable(self, repository):
        """
        Habilita repositório da Red Hat.
        :param repository: Repositório(s) a ser(em) adicionado(s)
        """
        if type(repository) is str:
            self.__shell.executar("sudo subscription-manager repos --enable={}".format(repository))
        elif type(repository) is list:
            for r in repository:
                self.repos_enable(r)

    def register(self, username, password):
        """
        Registra a instalação do Red Hat Enterprise Linux com a conta da Red Hat.
        :param username: Nome de usuário da conta da Red Hat.
        :param password: Senha da conta da Red Hat.
        """
        Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 5).executar(
            "sudo subscription-manager register --username {} --password {}".format(username, password))

    def habilitar_appstream_rpms(self):
        """
        Habilita o repositório AppStream RPMs.
        """
        self.repos_enable("rhel-8-for-{}-appstream-rpms".format(self.__arquitetura))

    def habilitar_baseos_rpms(self):
        """
        Habilita o repositório BaseOS RPMs.
        """
        self.repos_enable("rhel-8-for-{}-baseos-rpms".format(self.__arquitetura))

    def habilitar_codeready_builder(self):
        """
        Habilita o repositório CodeReady Builder.
        """
        self.repos_enable("codeready-builder-for-rhel-8-{}-rpms".format(self.__arquitetura))

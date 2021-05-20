import platform

from adapter.Shell import Shell, AcaoQuandoOcorrerErro


class SubscriptionManager:

    def __init__(self):
        self.__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)
        self.__arquitetura = platform.processor()

    def repos_enable(self, repository):
        if type(repository) is str:
            self.__shell.executar("sudo subscription-manager repos --enable={}".format(repository))
        elif type(repository) is list:
            for r in repository:
                self.repos_enable(r)

    def register(self, username, password):
        Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 5).executar(
            "sudo subscription-manager register --username {} --password {}".format(username, password))

    def habilitar_appstream_rpms(self):
        self.repos_enable("rhel-8-for-{}-appstream-rpms".format(self.__arquitetura))

    def habilitar_baseos_rpms(self):
        self.repos_enable("rhel-8-for-{}-baseos-rpms".format(self.__arquitetura))

    def habilitar_codeready_builder(self):
        self.repos_enable("codeready-builder-for-rhel-8-{}-rpms".format(self.__arquitetura))

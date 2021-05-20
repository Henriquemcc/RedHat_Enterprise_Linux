from adapter.Shell import Shell, AcaoQuandoOcorrerErro


class VisualStudioCode:

    def __init__(self):
        self.__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)

    def install_extension(self, extension):
        if type(extension) is str:
            self.__shell.executar("code --install-extension {}".format(extension))
        elif type(extension) is list:
            for e in extension:
                self.install_extension(e)

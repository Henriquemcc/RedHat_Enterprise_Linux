from adapter.Shell import Shell, AcaoQuandoOcorrerErro

__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)


def habilitar_wifi():
    __shell.executar("sudo nmcli radio wifi on")


def conectar_rede_wifi(usuario, senha):
    __shell.executar("sudo nmcli device wifi connect '{}' password '{}'".format(usuario, senha))

from adapter.Shell import Shell, AcaoQuandoOcorrerErro

__shell = Shell(AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR, 10)


def habilitar_wifi():
    """
    Habilita o Wifi do dispositivo.
    """
    __shell.executar("sudo nmcli radio wifi on")


def conectar_rede_wifi(ssid, senha):
    """
    Conecta o dispositivo a uma rede wifi.
    :param ssid: Service Set Identifier (Nome da rede).
    :param senha: Senha da rede.
    """
    __shell.executar("sudo nmcli device wifi connect '{}' password '{}'".format(ssid, senha))

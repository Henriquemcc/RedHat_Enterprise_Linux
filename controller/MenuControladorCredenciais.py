from boundary import MyIO
from controller.ControladorDeCredenciais import ControladorDeCredenciais
from model.Credencial import Credencial

__controlador_credenciais = ControladorDeCredenciais()


def __main():
    """
    Método construtor.
    """
    __imprimir_cabecalho("Controlador de Credenciais")
    __menu_principal()


def __imprimir_cabecalho(titulo: str):
    """
    Imprime o cabeçalho com um título
    :param titulo: Título a ser impresso junto com o cabeçalho.
    """
    print(
        "***********************************************************************************************************")
    print(titulo)
    print(
        "***********************************************************************************************************")


def __obter_opcao(limite, mensagem):
    """
    Obtém uma opção digitada pelo usuário.
    :param limite: Limite mínimo e máximo da opções.
    :param mensagem: Mensagem a ser impressa quando for perguntar quais as opções.
    :return: Opção selecionada pelo usuário.
    """
    while True:
        try:
            opcao = MyIO.read_integer(mensagem)
            if opcao not in limite:
                raise ValueError("{} is not in {}".format(opcao, limite))
            break
        except ValueError as e:
            print(e)
    return opcao


def __menu_principal():
    """
    Imprime o menu principal.
    """
    while True:
        __imprimir_cabecalho("Menu principal")
        mensagem = "0 - Sair\n"
        mensagem += "1 - Alterar credenciais\n"
        mensagem += "2 - Carregar credenciais\n"
        mensagem += "3 - Salvar credenciais\n"
        mensagem += "> "

        limite = range(0, 4)

        opcao = __obter_opcao(limite, mensagem)

        if opcao == 0:
            break
        elif opcao == 1:
            __menu_alterar_credenciais()
        elif opcao == 2:
            __controlador_credenciais.carregar()
        elif opcao == 3:
            __controlador_credenciais.salvar()


def __menu_alterar_credenciais():
    """
    Imprime o menu para alterar as credenciais.
    """
    while True:
        __imprimir_cabecalho("Menu de alteração de credenciais")
        mensagem = "0 - Sair\n"
        mensagem += "1 - Alterar credencial da rede wifi\n"
        mensagem += "2 - Alterar credencial da conta da Red Hat\n"
        mensagem += "> "

        limite = range(0, 3)

        opcao = __obter_opcao(limite, mensagem)

        if opcao == 0:
            break
        elif opcao == 1:
            if __controlador_credenciais.credencial_rede_wifi is None:
                __controlador_credenciais.credencial_rede_wifi = Credencial()
            __menu_alterar_credencial(__controlador_credenciais.credencial_rede_wifi,
                                      "Menu de alteração da credencial da rede do Wifi")
        elif opcao == 2:
            if __controlador_credenciais.credencial_conta_red_hat is None:
                __controlador_credenciais.credencial_conta_red_hat = Credencial()
            __menu_alterar_credencial(__controlador_credenciais.credencial_conta_red_hat,
                                      "Menu de alteração da credencial da conta da Red Hat")


def __menu_alterar_credencial(credencial: Credencial, titulo: str):
    """
    Imprime o menu para alterar uma credencial selecionada.
    :param credencial: Credencial que será modificada.
    :param titulo: Título do menu que será impresso no cabeçalho.
    """
    novo_nome_de_usuario = None
    nova_senha = None

    while True:
        __imprimir_cabecalho(titulo)
        mensagem = "0 - Sair\n"
        mensagem += "1 - Salvar e sair\n"

        if novo_nome_de_usuario is not None:
            mensagem += "2 - Usuário = {} -> {}\n".format(credencial.usuario, novo_nome_de_usuario)
        else:
            mensagem += "2 - Usuário = {}\n".format(credencial.usuario)

        if nova_senha is not None:
            mensagem += "3 - Senha = {} -> {}\n".format(credencial.senha, nova_senha)
        else:
            mensagem += "3 - Senha = {} \n".format(credencial.senha)
        mensagem += "> "
        limite = range(0, 4)

        opcao = __obter_opcao(limite, mensagem)

        if opcao == 0:
            break
        elif opcao == 1:
            if novo_nome_de_usuario is not None:
                credencial.usuario = novo_nome_de_usuario
            if nova_senha is not None:
                credencial.senha = nova_senha
            break
        elif opcao == 2:
            novo_nome_de_usuario = input("Nome de usuário: ")
        elif opcao == 3:
            nova_senha = input("Senha: ")


if __name__ == '__main__':
    __main()

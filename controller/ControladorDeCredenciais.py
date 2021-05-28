#!/usr/bin/python
import pickle

from boundary import MyIO
from model.Credencial import Credencial


class ControladorDeCredenciais:
    """
    Classe que controla as credenciais durante a instalação.
    """

    def __init__(self, nome_arquivo_credenciais):
        """
        Método construtor.
        :param nome_arquivo_credenciais: Nome do arquivo de credenciais.
        """
        self.__nome_arquivo_credenciais = nome_arquivo_credenciais
        self.__credencial_rede_wifi = Credencial()
        self.__credencial_conta_red_hat = Credencial()

        try:
            self.carregar()
        except Exception as e:
            print(e)

    def salvar(self):
        """
        Salva as credenciais no arquivo de credenciais.
        """
        with open(self.__nome_arquivo_credenciais, "wb") as arquivo_credenciais:
            pickle.dump(self.__credencial_rede_wifi, arquivo_credenciais)
            pickle.dump(self.__credencial_conta_red_hat, arquivo_credenciais)

    def carregar(self):
        """
        Carrega as credenciais do arquivo de credenciais.
        :return:
        """
        with open(self.__nome_arquivo_credenciais, "rb") as arquivo_credenciais:
            self.__credencial_rede_wifi = pickle.load(arquivo_credenciais)
            self.__credencial_conta_red_hat = pickle.load(arquivo_credenciais)

    @property
    def credencial_rede_wifi(self):
        """
        Método getter da credencial utilizada para conectar á rede wifi.
        :return: Credencial utilizada para conectar á rede wifi.
        """
        return self.__credencial_rede_wifi

    @credencial_rede_wifi.setter
    def credencial_rede_wifi(self, credencial: Credencial):
        """
        Método setter da credencial utilizada para conectar á rede wifi.
        :param credencial: Credencial para conectar á rede wifi.
        """
        if (credencial is not None) and type(credencial) is Credencial:
            self.__credencial_rede_wifi = credencial

    @property
    def credencial_conta_red_hat(self):
        """
        Método getter da credencial utilizada para associar a instalação á conta da Red Hat.
        :return: Credencial utilizada para conectar á conta da Red Hat.
        """
        return self.__credencial_conta_red_hat

    @credencial_conta_red_hat.setter
    def credencial_conta_red_hat(self, credencial: Credencial):
        """
        Método setter da credencial utilizada para associar a instalação á conta da Red Hat.
        :param credencial: Credencial utilizada para conectar á conta da Red Hat.
        """
        if (credencial is not None) and type(credencial) is Credencial:
            self.__credencial_conta_red_hat = credencial


class __MenuControladorCredenciais:
    """
    Classe que imprime o menu do console que auxilia no cadastro das credenciais.
    """

    def __init__(self):
        """
        Método construtor.
        """
        self.__imprimir_cabecalho("Controlador de Credenciais")
        self.__controlador_credenciais = ControladorDeCredenciais("../Credenciais.bin")
        self.__menu_principal()

    def __imprimir_cabecalho(self, titulo: str):
        """
        Imprime o cabeçalho com um título
        :param titulo: Título a ser impresso junto com o cabeçalho.
        """
        print(
            "***********************************************************************************************************")
        print(titulo)
        print(
            "***********************************************************************************************************")

    def __obterOpcao(self, limite, mensagem):
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

    def __menu_principal(self):
        """
        Imprime o menu principal.
        """
        while True:
            self.__imprimir_cabecalho("Menu principal")
            mensagem = "0 - Sair\n"
            mensagem += "1 - Alterar credenciais\n"
            mensagem += "2 - Carregar credenciais\n"
            mensagem += "3 - Salvar credenciais\n"
            mensagem += "> "

            limite = range(0, 4)

            opcao = self.__obterOpcao(limite, mensagem)

            if opcao == 0:
                break
            elif opcao == 1:
                self.__menu_alterar_credenciais()
            elif opcao == 2:
                self.__controlador_credenciais.carregar()
            elif opcao == 3:
                self.__controlador_credenciais.salvar()

    def __menu_alterar_credenciais(self):
        """
        Imprime o menu para alterar as credenciais.
        """
        while True:
            self.__imprimir_cabecalho("Menu de alteração de credenciais")
            mensagem = "0 - Sair\n"
            mensagem += "1 - Alterar credencial da rede wifi\n"
            mensagem += "2 - Alterar credencial da conta da Red Hat\n"
            mensagem += "> "

            limite = range(0, 3)

            opcao = self.__obterOpcao(limite, mensagem)

            if opcao == 0:
                break
            elif opcao == 1:
                if self.__controlador_credenciais.credencial_rede_wifi is None:
                    self.__controlador_credenciais.credencial_rede_wifi = Credencial()
                self.__menu_alterar_credencial(self.__controlador_credenciais.credencial_rede_wifi,
                                               "Menu de alteração da credencial da rede do Wifi")
            elif opcao == 2:
                if self.__controlador_credenciais.credencial_conta_red_hat is None:
                    self.__controlador_credenciais.credencial_conta_red_hat = Credencial()
                self.__menu_alterar_credencial(self.__controlador_credenciais.credencial_conta_red_hat,
                                               "Menu de alteração da credencial da conta da Red Hat")

    def __menu_alterar_credencial(self, credencial: Credencial, titulo: str):
        """
        Imprime o menu para alterar uma credencial selecionada.
        :param credencial: Credencial que será modificada.
        :param titulo: Título do menu que será impresso no cabeçalho.
        """
        novo_nome_de_usuario = None
        nova_senha = None

        while True:
            self.__imprimir_cabecalho(titulo)
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

            opcao = self.__obterOpcao(limite, mensagem)

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
    menu = __MenuControladorCredenciais()

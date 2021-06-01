#!/usr/bin/python
import pickle

from model.Credencial import Credencial

nome_padrao_arquivo_credenciais = "Credenciais.bin"


class ControladorDeCredenciais:
    """
    Classe que controla as credenciais durante a instalação.
    """

    def __init__(self, nome_arquivo_credenciais=nome_padrao_arquivo_credenciais):
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

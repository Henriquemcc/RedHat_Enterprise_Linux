import os
import shutil

import Tools.String


def __get_dot_old_file_name(nome_arquivo: str) -> str:
    """
    Obtém o nome do arquivo de backup evitando sobrescrever algum arquivo existente
    :param nome_arquivo: Nome do arquivo original.
    :return String com o novo nome para o arquivo
    """

    if ".old" in nome_arquivo:
        if Tools.String.string_ends_with_number(nome_arquivo):
            numero = Tools.String.string_get_real_number_at_the_end(nome_arquivo)
            novo_numero = numero + 1
            if numero.is_integer():
                numero = int(numero)
            if novo_numero.is_integer():
                novo_numero = int(novo_numero)
            nome_arquivo_dividido = nome_arquivo.rsplit(str(numero))
            return "{}{}{}".format(nome_arquivo_dividido[0], str(novo_numero), nome_arquivo_dividido[1])
        else:
            numero = 0
            novo_numero = numero + 1
            return "{}{}".format(nome_arquivo, novo_numero)
    else:
        return "{}.old".format(nome_arquivo)


def get_new_backup_file_name(caminho_pasta_pai: str, nome_arquivo: str) -> str:
    """
    Obtém um novo nome de um arquivo de backup garantindo que ele não exista anteriormente.
    :param caminho_pasta_pai: Caminho da pasta onde este arquivo está armazenado.
    :param nome_arquivo: Nome do arquivo original.
    :return: Novo nome de arquivo
    """
    while os.path.isfile(os.path.join(caminho_pasta_pai, nome_arquivo)):
        nome_arquivo = __get_dot_old_file_name(nome_arquivo)

    return nome_arquivo


def backup_file(caminho_pasta_pai: str, nome_arquivo: str):
    """
    Cria um backup de um arquivo no mesmo diretório garantindo que o nome do arquivo de backup seja único para evitar sobrescrita.
    :param caminho_pasta_pai: Caminho da pasta onde este arquivo está armazenado.
    :param nome_arquivo: Nome do arquivo original.
    """
    caminho_arquivo_origem = os.path.join(caminho_pasta_pai, nome_arquivo)
    nome_arquivo_backup = get_new_backup_file_name(caminho_pasta_pai, nome_arquivo)
    caminho_arquivo_destino = os.path.join(caminho_pasta_pai, nome_arquivo_backup)
    shutil.copy2(caminho_arquivo_origem, caminho_arquivo_destino)
